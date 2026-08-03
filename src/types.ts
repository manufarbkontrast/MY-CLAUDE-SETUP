/** Where a registry entry came from. */
export type EntrySource = "local" | "plugin";

/**
 * An installed + enabled Claude Code plugin resolved to a concrete
 * version directory under ~/.claude/plugins/cache.
 */
export interface PluginInfo {
  /** Plugin name, e.g. "claude-seo" — also the invocation namespace. */
  readonly name: string;
  /** Marketplace directory name, e.g. "agricidaniel-claude-seo". */
  readonly marketplace: string;
  /** Key used in settings.json enabledPlugins, e.g. "claude-seo@agricidaniel-claude-seo". */
  readonly key: string;
  readonly version: string;
  /** Absolute path to the version directory. */
  readonly root: string;
}

export interface SkillEntry {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly keywords: readonly string[];
  readonly category: string;
  /** Repo-relative for local entries, absolute for plugin entries. */
  readonly path: string;
  readonly contentSummary: string;
  readonly source: EntrySource;
  /** Plugin name when source === "plugin". */
  readonly plugin?: string;
}

export interface AgentEntry {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly role: string;
  readonly tools: readonly string[];
  readonly model: string;
  readonly path: string;
  readonly contentSummary: string;
  readonly source: EntrySource;
  readonly plugin?: string;
}

export interface CommandEntry {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly usage: string;
  readonly relatedSkills: readonly string[];
  readonly path: string;
  readonly contentSummary: string;
  readonly source: EntrySource;
  readonly plugin?: string;
}

export interface RuleEntry {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly path: string;
  readonly contentSummary: string;
}

export interface HookEntry {
  readonly id: string;
  readonly type: string;
  readonly matcher: string;
  readonly description: string;
}

export interface Registry {
  readonly skills: readonly SkillEntry[];
  readonly agents: readonly AgentEntry[];
  readonly commands: readonly CommandEntry[];
  readonly rules: readonly RuleEntry[];
  readonly hooks: readonly HookEntry[];
  /** Plugins that contributed entries to this registry. */
  readonly plugins: readonly PluginInfo[];
  readonly metadata: {
    readonly generatedAt: string;
    readonly skillCount: number;
    readonly agentCount: number;
    readonly commandCount: number;
    readonly ruleCount: number;
    readonly hookCount: number;
    readonly pluginCount: number;
    /** Entries contributed by plugins, for a quick local/plugin split. */
    readonly pluginSkillCount: number;
    readonly pluginAgentCount: number;
    readonly pluginCommandCount: number;
  };
}

export interface MatchResult {
  readonly item: SkillEntry | AgentEntry | CommandEntry | RuleEntry;
  readonly score: number;
  readonly matchType: "keyword" | "fuzzy" | "category";
}

export interface OptimizedPrompt {
  readonly originalPrompt: string;
  readonly skills: readonly SkillEntry[];
  readonly agents: readonly AgentEntry[];
  readonly commands: readonly CommandEntry[];
  readonly rules: readonly RuleEntry[];
  readonly optimizedText: string;
}
