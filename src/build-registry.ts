import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import type {
  Registry,
  SkillEntry,
  AgentEntry,
  CommandEntry,
  RuleEntry,
  HookEntry,
} from "./types.js";
import {
  deriveCategory,
  extractKeywords,
  parseFrontmatter,
  summarize,
} from "./parse.js";
import {
  discoverPlugins,
  scanPluginAgents,
  scanPluginCommands,
  scanPluginSkills,
  type ScanWarning,
} from "./plugins.js";

const REPO_ROOT =
  process.env.PROMPT_OPTIMIZER_ROOT ?? path.resolve(import.meta.dirname, "..");

/**
 * Claude Code loads skills, agents, commands and rules from ~/.claude — the
 * repo is only the versioned copy of them. Scanning ~/.claude keeps the
 * registry aligned with what is actually available at runtime; the repo is
 * the fallback when no user config directory exists (e.g. CI).
 */
const USER_ROOT = process.env.CLAUDE_CONFIG_DIR ?? path.join(os.homedir(), ".claude");

/** Picks the live directory when present, else the repo copy. */
function assetRoot(dirName: string): string {
  const userDir = path.join(USER_ROOT, dirName);
  return fs.existsSync(userDir) ? userDir : path.join(REPO_ROOT, dirName);
}

/** settings.json holds the hook definitions; the live one wins. */
function settingsFile(): string {
  const userSettings = path.join(USER_ROOT, "settings.json");
  return fs.existsSync(userSettings)
    ? userSettings
    : path.join(REPO_ROOT, "settings.json");
}

const SETTINGS_FILE = settingsFile();

// --- Local scanners ---

function scanSkills(): readonly SkillEntry[] {
  const skillsDir = assetRoot("skills");
  if (!fs.existsSync(skillsDir)) return [];

  const entries = fs.readdirSync(skillsDir, { withFileTypes: true });
  const skills: SkillEntry[] = [];

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;

    const skillDir = path.join(skillsDir, entry.name);
    const skillFile = path.join(skillDir, "SKILL.md");

    if (!fs.existsSync(skillFile)) continue;

    const content = fs.readFileSync(skillFile, "utf-8");
    const { frontmatter, body } = parseFrontmatter(content);

    const id = entry.name;
    const name = frontmatter.name || entry.name;
    const description = frontmatter.description || "";

    skills.push(
      Object.freeze({
        id,
        name,
        description,
        keywords: extractKeywords(name, description, body),
        category: deriveCategory(skillDir),
        path: skillFile,
        contentSummary: summarize(body),
        source: "local" as const,
      })
    );
  }

  return Object.freeze(skills);
}

function scanAgents(): readonly AgentEntry[] {
  const agentsDir = assetRoot("agents");
  if (!fs.existsSync(agentsDir)) return [];

  const files = fs.readdirSync(agentsDir).filter((f) => f.endsWith(".md"));
  const agents: AgentEntry[] = [];

  for (const file of files) {
    const filePath = path.join(agentsDir, file);
    const content = fs.readFileSync(filePath, "utf-8");
    const { frontmatter, body } = parseFrontmatter(content);

    const id = file.replace(".md", "");
    const name = frontmatter.name || id;
    const description = frontmatter.description || "";
    const role =
      body.split("\n").find((l) => l.startsWith("You are"))?.trim() || "";

    // Parse tools array from frontmatter
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
        name,
        description,
        role,
        tools: Object.freeze(tools),
        model: frontmatter.model || "sonnet",
        path: filePath,
        contentSummary: summarize(body),
        source: "local" as const,
      })
    );
  }

  return Object.freeze(agents);
}

function scanCommands(): readonly CommandEntry[] {
  const commandsDir = assetRoot("commands");
  if (!fs.existsSync(commandsDir)) return [];

  const files = fs.readdirSync(commandsDir).filter((f) => f.endsWith(".md"));
  const commands: CommandEntry[] = [];

  for (const file of files) {
    const filePath = path.join(commandsDir, file);
    const content = fs.readFileSync(filePath, "utf-8");
    const { frontmatter, body } = parseFrontmatter(content);

    const id = file.replace(".md", "");

    // Try to find usage from body
    const usageMatch = body.match(/## Usage\n([\s\S]*?)(?=\n##|\n$)/);
    const usage = usageMatch ? (usageMatch[1] ?? "").trim().slice(0, 200) : "";

    // Find related skills by scanning body for skill references
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
        source: "local" as const,
      })
    );
  }

  return Object.freeze(commands);
}

function scanRules(): readonly RuleEntry[] {
  const rulesDir = assetRoot("rules");
  if (!fs.existsSync(rulesDir)) return [];

  const files = fs.readdirSync(rulesDir).filter((f) => f.endsWith(".md"));
  const rules: RuleEntry[] = [];

  for (const file of files) {
    const filePath = path.join(rulesDir, file);
    const content = fs.readFileSync(filePath, "utf-8");
    const { body } = parseFrontmatter(content);

    const id = file.replace(".md", "");
    const name = id
      .split("-")
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(" ");

    // First heading or first paragraph as description
    const firstHeading = body.match(/^#\s+(.+)$/m);
    const description = (firstHeading ? firstHeading[1] : name) ?? name;

    rules.push(
      Object.freeze({
        id,
        name,
        description,
        path: filePath,
        contentSummary: summarize(body),
      })
    );
  }

  return Object.freeze(rules);
}

function scanHooks(): readonly HookEntry[] {
  if (!fs.existsSync(SETTINGS_FILE)) return [];

  const settings = JSON.parse(fs.readFileSync(SETTINGS_FILE, "utf-8"));
  const hooksConfig = settings.hooks;
  if (!hooksConfig) return [];

  const hooks: HookEntry[] = [];
  let idx = 0;

  for (const [hookType, hookList] of Object.entries(hooksConfig)) {
    if (!Array.isArray(hookList)) continue;
    for (const entry of hookList) {
      const hookEntry = entry as {
        matcher?: string;
        description?: string;
      };
      hooks.push(
        Object.freeze({
          id: `hook-${idx++}`,
          type: hookType,
          matcher: hookEntry.matcher || "",
          description: hookEntry.description || "",
        })
      );
    }
  }

  return Object.freeze(hooks);
}

// --- Merging ---

/**
 * Concatenates local and plugin entries, dropping later duplicates by id.
 * Local entries win, so a plugin can never shadow a hand-written asset.
 */
function mergeById<T extends { readonly id: string }>(
  ...groups: readonly (readonly T[])[]
): readonly T[] {
  const byId = new Map<string, T>();
  for (const group of groups) {
    for (const entry of group) {
      if (!byId.has(entry.id)) byId.set(entry.id, entry);
    }
  }
  return Object.freeze([...byId.values()]);
}

// --- Main ---

function buildRegistry(): Registry {
  const warnings: ScanWarning[] = [];

  console.log(`Scanning local assets from ${assetRoot("skills")}/..`);
  const localSkills = scanSkills();
  const localAgents = scanAgents();
  const localCommands = scanCommands();
  console.log(
    `  ${localSkills.length} skills, ${localAgents.length} agents, ${localCommands.length} commands`
  );

  console.log("Scanning plugins...");
  const plugins = discoverPlugins(SETTINGS_FILE, warnings);
  const scanned = plugins.map((plugin) => ({
    plugin,
    skills: scanPluginSkills(plugin),
    agents: scanPluginAgents(plugin),
    commands: scanPluginCommands(plugin),
  }));

  const pluginSkills = scanned.flatMap((s) => [...s.skills]);
  const pluginAgents = scanned.flatMap((s) => [...s.agents]);
  const pluginCommands = scanned.flatMap((s) => [...s.commands]);
  console.log(
    `  ${plugins.length} plugins -> ${pluginSkills.length} skills, ${pluginAgents.length} agents, ${pluginCommands.length} commands`
  );
  for (const s of scanned) {
    const total = s.skills.length + s.agents.length + s.commands.length;
    if (total === 0) {
      warnings.push({
        scope: s.plugin.key,
        message: "contributes no skills, agents or commands",
      });
      continue;
    }
    console.log(
      `    ${s.plugin.name}@${s.plugin.version}: ${s.skills.length} skills, ${s.agents.length} agents, ${s.commands.length} commands`
    );
  }

  console.log("Scanning rules & hooks...");
  const rules = scanRules();
  const hooks = scanHooks();
  console.log(`  ${rules.length} rules, ${hooks.length} hooks`);

  const skills = mergeById(localSkills, pluginSkills);
  const agents = mergeById(localAgents, pluginAgents);
  const commands = mergeById(localCommands, pluginCommands);

  if (warnings.length > 0) {
    console.log("\nWarnings:");
    for (const w of warnings) {
      console.log(`  [${w.scope}] ${w.message}`);
    }
  }

  return Object.freeze({
    skills,
    agents,
    commands,
    rules,
    hooks,
    plugins,
    metadata: Object.freeze({
      generatedAt: new Date().toISOString(),
      skillCount: skills.length,
      agentCount: agents.length,
      commandCount: commands.length,
      ruleCount: rules.length,
      hookCount: hooks.length,
      pluginCount: plugins.length,
      pluginSkillCount: skills.filter((s) => s.source === "plugin").length,
      pluginAgentCount: agents.filter((a) => a.source === "plugin").length,
      pluginCommandCount: commands.filter((c) => c.source === "plugin").length,
    }),
  });
}

const registry = buildRegistry();
const outputPath = path.join(REPO_ROOT, "registry.json");
fs.writeFileSync(outputPath, JSON.stringify(registry, null, 2), "utf-8");

const m = registry.metadata;
console.log(`\nRegistry written to ${outputPath}`);
console.log(
  `Total: ${m.skillCount} skills, ${m.agentCount} agents, ${m.commandCount} commands, ${m.ruleCount} rules, ${m.hookCount} hooks`
);
console.log(
  `  thereof from ${m.pluginCount} plugins: ${m.pluginSkillCount} skills, ${m.pluginAgentCount} agents, ${m.pluginCommandCount} commands`
);
