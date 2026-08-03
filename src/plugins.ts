import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type {
  AgentEntry,
  CommandEntry,
  PluginInfo,
  SkillEntry,
} from "./types.js";
import {
  deriveCategory,
  extractKeywords,
  parseFrontmatter,
  summarize,
} from "./parse.js";

/**
 * Discovers installed Claude Code plugins and scans the skills, agents and
 * commands they contribute.
 *
 * Layout on disk:
 *   ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/{skills,agents,commands}
 *
 * A plugin can have several versions cached side by side, so the active one is
 * resolved from installed_plugins.json when possible and from the highest
 * semver otherwise. Only plugins listed as enabled in settings.json are used.
 */

const CLAUDE_DIR = path.join(os.homedir(), ".claude");
const PLUGINS_DIR = path.join(CLAUDE_DIR, "plugins");
const CACHE_DIR = path.join(PLUGINS_DIR, "cache");
const INSTALLED_MANIFEST = path.join(PLUGINS_DIR, "installed_plugins.json");
const GLOBAL_SETTINGS = path.join(CLAUDE_DIR, "settings.json");

/** Collected non-fatal problems, surfaced by the caller instead of thrown. */
export interface ScanWarning {
  readonly scope: string;
  readonly message: string;
}

function readJson(filePath: string, warnings: ScanWarning[]): unknown | null {
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf-8"));
  } catch (err) {
    warnings.push({
      scope: path.basename(filePath),
      message: `unreadable JSON: ${err instanceof Error ? err.message : String(err)}`,
    });
    return null;
  }
}

/**
 * Plugin keys that are switched on in the user's global settings.
 * Returns null when no enabledPlugins map exists — then every cached plugin
 * is considered active.
 */
function readEnabledPluginKeys(
  fallbackSettings: string,
  warnings: ScanWarning[]
): ReadonlySet<string> | null {
  for (const file of [GLOBAL_SETTINGS, fallbackSettings]) {
    const settings = readJson(file, warnings) as
      | { enabledPlugins?: Record<string, boolean> }
      | null;
    const enabled = settings?.enabledPlugins;
    if (!enabled || typeof enabled !== "object") continue;

    return Object.freeze(
      new Set(
        Object.entries(enabled)
          .filter(([, on]) => on === true)
          .map(([key]) => key)
      )
    );
  }
  return null;
}

/** installPath per "<plugin>@<marketplace>" key, from the install manifest. */
function readInstalledPaths(
  warnings: ScanWarning[]
): ReadonlyMap<string, string> {
  const manifest = readJson(INSTALLED_MANIFEST, warnings) as {
    plugins?: Record<string, Array<{ installPath?: string }>>;
  } | null;

  const paths = new Map<string, string>();
  for (const [key, installs] of Object.entries(manifest?.plugins ?? {})) {
    const installPath = installs?.[0]?.installPath;
    if (installPath) paths.set(key, installPath);
  }
  return paths;
}

function compareSemver(a: string, b: string): number {
  const parse = (v: string): readonly number[] =>
    v.split(".").map((part) => Number.parseInt(part, 10) || 0);
  const [pa, pb] = [parse(a), parse(b)];
  const len = Math.max(pa.length, pb.length);
  for (let i = 0; i < len; i++) {
    const diff = (pa[i] ?? 0) - (pb[i] ?? 0);
    if (diff !== 0) return diff;
  }
  return 0;
}

function listDirs(dir: string): readonly string[] {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isDirectory() && !e.name.startsWith("."))
    .map((e) => e.name);
}

/**
 * Resolves every enabled plugin to exactly one version directory.
 */
export function discoverPlugins(
  fallbackSettings: string,
  warnings: ScanWarning[]
): readonly PluginInfo[] {
  if (!fs.existsSync(CACHE_DIR)) {
    warnings.push({
      scope: "plugins",
      message: `no plugin cache at ${CACHE_DIR} — skipping plugin scan`,
    });
    return [];
  }

  const enabledKeys = readEnabledPluginKeys(fallbackSettings, warnings);
  const installedPaths = readInstalledPaths(warnings);
  const plugins: PluginInfo[] = [];

  for (const marketplace of listDirs(CACHE_DIR)) {
    for (const name of listDirs(path.join(CACHE_DIR, marketplace))) {
      const key = `${name}@${marketplace}`;
      if (enabledKeys && !enabledKeys.has(key)) continue;

      const pluginDir = path.join(CACHE_DIR, marketplace, name);
      const versions = listDirs(pluginDir);
      if (versions.length === 0) {
        warnings.push({ scope: key, message: "no version directory found" });
        continue;
      }

      // The install manifest is authoritative; fall back to highest semver
      // for plugins installed outside of it (e.g. via an install script).
      const manifestPath = installedPaths.get(key);
      const version =
        manifestPath && fs.existsSync(manifestPath)
          ? path.basename(manifestPath)
          : [...versions].sort(compareSemver).at(-1)!;

      const root = path.join(pluginDir, version);
      if (!fs.existsSync(root)) {
        warnings.push({ scope: key, message: `version ${version} not on disk` });
        continue;
      }

      plugins.push(Object.freeze({ name, marketplace, key, version, root }));
    }
  }

  return Object.freeze(
    [...plugins].sort((a, b) => a.name.localeCompare(b.name))
  );
}

// --- Scanners ---

function readSkillFile(
  plugin: PluginInfo,
  skillFile: string,
  fallbackName: string
): SkillEntry | null {
  if (!fs.existsSync(skillFile)) return null;

  const { frontmatter, body } = parseFrontmatter(
    fs.readFileSync(skillFile, "utf-8")
  );
  const baseName = frontmatter.name || fallbackName;
  // Claude Code addresses plugin skills as "<plugin>:<skill>".
  const id = `${plugin.name}:${baseName}`;

  return Object.freeze({
    id,
    name: id,
    description: frontmatter.description || "",
    keywords: extractKeywords(baseName, frontmatter.description || "", body),
    category: deriveCategory(path.dirname(skillFile)),
    path: skillFile,
    contentSummary: summarize(body),
    source: "plugin" as const,
    plugin: plugin.name,
  });
}

/**
 * Skills live in <root>/skills/<name>/SKILL.md. A few single-skill plugins
 * instead ship one SKILL.md at the plugin root.
 */
export function scanPluginSkills(plugin: PluginInfo): readonly SkillEntry[] {
  const skills: SkillEntry[] = [];

  const skillsDir = path.join(plugin.root, "skills");
  for (const name of listDirs(skillsDir)) {
    const entry = readSkillFile(
      plugin,
      path.join(skillsDir, name, "SKILL.md"),
      name
    );
    if (entry) skills.push(entry);
  }

  const rootSkill = readSkillFile(
    plugin,
    path.join(plugin.root, "SKILL.md"),
    plugin.name
  );
  if (rootSkill) skills.push(rootSkill);

  return Object.freeze(skills);
}

function listMarkdown(dir: string): readonly string[] {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isFile() && e.name.endsWith(".md"))
    .map((e) => e.name);
}

export function scanPluginAgents(plugin: PluginInfo): readonly AgentEntry[] {
  const agentsDir = path.join(plugin.root, "agents");
  const agents: AgentEntry[] = [];

  for (const file of listMarkdown(agentsDir)) {
    const filePath = path.join(agentsDir, file);
    const { frontmatter, body } = parseFrontmatter(
      fs.readFileSync(filePath, "utf-8")
    );

    const baseName = frontmatter.name || file.replace(/\.md$/, "");
    const id = `${plugin.name}:${baseName}`;

    let tools: string[] = [];
    if (frontmatter.tools) {
      try {
        tools = JSON.parse(frontmatter.tools);
      } catch {
        tools = frontmatter.tools.split(",").map((t: string) => t.trim());
      }
    }

    agents.push(
      Object.freeze({
        id,
        name: id,
        description: frontmatter.description || "",
        role: body.split("\n").find((l) => l.startsWith("You are"))?.trim() || "",
        tools: Object.freeze(tools),
        model: frontmatter.model || "sonnet",
        path: filePath,
        contentSummary: summarize(body),
        source: "plugin" as const,
        plugin: plugin.name,
      })
    );
  }

  return Object.freeze(agents);
}

/**
 * Only top-level commands/*.md are invocable slash commands — nested
 * directories hold prompt modules that commands include.
 *
 * Two kinds of files are skipped, matching what Claude Code actually offers
 * the model: files without frontmatter are not registered as commands at all,
 * and `disable-model-invocation: true` marks a command as user-only. Neither
 * is worth recommending in an optimized prompt.
 */
export function scanPluginCommands(
  plugin: PluginInfo
): readonly CommandEntry[] {
  const commandsDir = path.join(plugin.root, "commands");
  const commands: CommandEntry[] = [];

  for (const file of listMarkdown(commandsDir)) {
    const filePath = path.join(commandsDir, file);
    const { frontmatter, body, hasFrontmatter } = parseFrontmatter(
      fs.readFileSync(filePath, "utf-8")
    );

    if (!hasFrontmatter) continue;
    if (frontmatter["disable-model-invocation"] === "true") continue;

    const id = `${plugin.name}:${file.replace(/\.md$/, "")}`;

    const usageMatch = body.match(/## Usage\n([\s\S]*?)(?=\n##|\n$)/);
    const usage = usageMatch ? (usageMatch[1] ?? "").trim().slice(0, 200) : "";

    const relatedSkills: string[] = [];
    const skillRefPattern = /skills\/([a-z0-9-]+)/gi;
    let skillMatch: RegExpExecArray | null;
    while ((skillMatch = skillRefPattern.exec(body)) !== null) {
      if (skillMatch[1]) relatedSkills.push(skillMatch[1]);
    }

    commands.push(
      Object.freeze({
        id,
        name: id,
        description: frontmatter.description || "",
        usage,
        relatedSkills: Object.freeze(relatedSkills),
        path: filePath,
        contentSummary: summarize(body),
        source: "plugin" as const,
        plugin: plugin.name,
      })
    );
  }

  return Object.freeze(commands);
}
