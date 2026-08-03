import * as path from "node:path";

/**
 * Shared parsing / classification helpers used by every scanner
 * (local repo assets as well as installed Claude Code plugins).
 */

// --- Frontmatter ---

export function parseFrontmatter(content: string): {
  frontmatter: Record<string, string>;
  body: string;
  /** False when the file has no `---` block at all. */
  hasFrontmatter: boolean;
} {
  const match = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!match) {
    return { frontmatter: {}, body: content, hasFrontmatter: false };
  }

  const raw = match[1] ?? "";
  const body = match[2] ?? "";
  const frontmatter: Record<string, string> = {};

  for (const line of raw.split("\n")) {
    const colonIdx = line.indexOf(":");
    if (colonIdx === -1) continue;
    const key = line.slice(0, colonIdx).trim();
    let value = line.slice(colonIdx + 1).trim();
    // Strip surrounding quotes
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    frontmatter[key] = value;
  }

  return { frontmatter, body, hasFrontmatter: true };
}

// --- Keywords ---

const TECH_PATTERNS: readonly string[] = Object.freeze([
  "react",
  "next.js",
  "nextjs",
  "vue",
  "nuxt",
  "angular",
  "svelte",
  "solid",
  "astro",
  "remix",
  "gatsby",
  "node",
  "nodejs",
  "deno",
  "bun",
  "express",
  "fastapi",
  "django",
  "flask",
  "rails",
  "laravel",
  "spring",
  "nest",
  "hono",
  "elysia",
  "typescript",
  "javascript",
  "python",
  "rust",
  "go",
  "golang",
  "java",
  "kotlin",
  "swift",
  "c#",
  "csharp",
  "dotnet",
  ".net",
  "ruby",
  "php",
  "elixir",
  "scala",
  "haskell",
  "julia",
  "dart",
  "flutter",
  "c++",
  "cpp",
  "postgres",
  "postgresql",
  "mysql",
  "mongodb",
  "redis",
  "sqlite",
  "supabase",
  "firebase",
  "prisma",
  "drizzle",
  "d1",
  "neon",
  "planetscale",
  "shopify",
  "stripe",
  "paypal",
  "woocommerce",
  "magento",
  "aws",
  "azure",
  "gcp",
  "cloudflare",
  "vercel",
  "netlify",
  "docker",
  "kubernetes",
  "k8s",
  "terraform",
  "helm",
  "github",
  "gitlab",
  "ci/cd",
  "cicd",
  "graphql",
  "rest",
  "grpc",
  "websocket",
  "sse",
  "oauth",
  "jwt",
  "auth",
  "authentication",
  "authorization",
  "rbac",
  "security",
  "testing",
  "jest",
  "vitest",
  "playwright",
  "cypress",
  "selenium",
  "tdd",
  "bdd",
  "seo",
  "accessibility",
  "a11y",
  "wcag",
  "performance",
  "optimization",
  "caching",
  "cdn",
  "rag",
  "llm",
  "ai",
  "ml",
  "embedding",
  "vector",
  "langchain",
  "openai",
  "anthropic",
  "claude",
  "tailwind",
  "css",
  "sass",
  "styled",
  "design-system",
  "ui",
  "ux",
  "responsive",
  "mobile",
  "ios",
  "android",
  "react-native",
  "pwa",
  "api",
  "microservices",
  "monorepo",
  "turborepo",
  "nx",
  "webpack",
  "vite",
  "esbuild",
  "rollup",
  "bundler",
  "blockchain",
  "web3",
  "solidity",
  "nft",
  "defi",
  "automation",
  "workflow",
  "temporal",
  "durable-objects",
  "workers",
  "edge",
  "serverless",
  "lambda",
  "mcp",
  "prompt",
  "agent",
  "debugging",
  "refactoring",
  "migration",
  "deployment",
  "monitoring",
  "observability",
  "logging",
  "tracing",
  "incident",
  "devops",
  "sre",
  "data-pipeline",
  "etl",
  "spark",
  "airflow",
  "dbt",
  "analytics",
  "dashboard",
  "report",
  "e-commerce",
  "checkout",
  "payment",
  "billing",
  "subscription",
  "content",
  "cms",
  "markdown",
  "documentation",
  "openapi",
  "swagger",
  "schema",
  "validation",
  "zod",
  "pydantic",
  "form",
  "upload",
  "image",
  "media",
  "video",
  "threejs",
  "3d",
  "animation",
  "motion",
  "canvas",
  "game",
  "unity",
  "godot",
  "firmware",
  "embedded",
  "iot",
  "arm",
  "cortex",
]);

export function extractKeywords(
  name: string,
  description: string,
  body: string
): readonly string[] {
  const text = `${name} ${description} ${body.slice(0, 2000)}`.toLowerCase();

  const found = new Set<string>();
  for (const kw of TECH_PATTERNS) {
    if (text.includes(kw)) {
      found.add(kw);
    }
  }

  // Add the name segments as keywords (":" splits the plugin namespace off)
  const nameSegments = name
    .split(/[-_./\\:]/)
    .filter((s) => s.length > 2)
    .map((s) => s.toLowerCase());
  for (const seg of nameSegments) {
    found.add(seg);
  }

  return Object.freeze([...found]);
}

// --- Summaries ---

export function summarize(body: string, maxLen = 200): string {
  // Take the first meaningful paragraph after the title
  const lines = body.split("\n").filter((l) => l.trim().length > 0);
  let summary = "";
  for (const line of lines) {
    const trimmed = line.trim();
    // Skip headings and code fences
    if (trimmed.startsWith("#") || trimmed.startsWith("```")) continue;
    // Skip frontmatter-like lines
    if (trimmed.startsWith("---")) continue;
    summary = trimmed;
    break;
  }
  if (summary.length > maxLen) {
    return summary.slice(0, maxLen - 3) + "...";
  }
  return summary || "No summary available";
}

// --- Categories ---

const CATEGORY_MAP: Record<string, readonly string[]> = Object.freeze({
  "e-commerce": [
    "shopify",
    "woocommerce",
    "stripe",
    "paypal",
    "payment",
    "billing",
    "checkout",
  ],
  frontend: [
    "react",
    "vue",
    "angular",
    "svelte",
    "nextjs",
    "nuxt",
    "frontend",
    "css",
    "tailwind",
    "ui",
    "design",
    "responsive",
    "accessibility",
    "motion",
    "canvas",
    "threejs",
  ],
  backend: [
    "express",
    "fastapi",
    "django",
    "flask",
    "nest",
    "hono",
    "rails",
    "spring",
    "backend",
    "api",
    "rest",
    "graphql",
    "grpc",
    "websocket",
  ],
  database: [
    "postgres",
    "mysql",
    "mongo",
    "redis",
    "sqlite",
    "supabase",
    "prisma",
    "drizzle",
    "database",
    "sql",
    "migration",
    "schema",
  ],
  devops: [
    "docker",
    "kubernetes",
    "k8s",
    "terraform",
    "helm",
    "ci",
    "cd",
    "github-actions",
    "gitlab",
    "deploy",
    "monitor",
    "observability",
    "logging",
  ],
  security: [
    "security",
    "auth",
    "oauth",
    "jwt",
    "rbac",
    "csrf",
    "xss",
    "sast",
    "vulnerability",
    "secrets",
    "compliance",
  ],
  testing: [
    "test",
    "jest",
    "vitest",
    "playwright",
    "cypress",
    "tdd",
    "bdd",
    "e2e",
    "coverage",
    "mutation",
  ],
  ai: [
    "ai",
    "ml",
    "llm",
    "rag",
    "embedding",
    "vector",
    "langchain",
    "prompt",
    "agent",
    "model",
  ],
  cloud: [
    "aws",
    "azure",
    "gcp",
    "cloudflare",
    "workers",
    "serverless",
    "lambda",
    "edge",
    "durable",
  ],
  mobile: [
    "mobile",
    "ios",
    "android",
    "react-native",
    "flutter",
    "swift",
    "kotlin",
    "pwa",
    "app-store",
  ],
  data: [
    "data",
    "pipeline",
    "etl",
    "spark",
    "airflow",
    "dbt",
    "analytics",
    "dashboard",
  ],
  content: ["seo", "content", "cms", "markdown", "documentation", "doc"],
  architecture: [
    "architecture",
    "pattern",
    "microservices",
    "monorepo",
    "event",
    "cqrs",
    "saga",
    "ddd",
  ],
  language: [
    "typescript",
    "javascript",
    "python",
    "rust",
    "go",
    "golang",
    "java",
    "ruby",
    "php",
    "elixir",
    "scala",
    "haskell",
    "julia",
    "cpp",
    "csharp",
    "swift",
    "dart",
    "bash",
  ],
  blockchain: ["blockchain", "web3", "solidity", "nft", "defi", "smart-contract"],
  automation: ["automation", "workflow", "temporal", "hook", "script", "shell"],
  gaming: ["game", "unity", "godot", "3d", "ecs"],
  embedded: ["firmware", "embedded", "iot", "arm", "cortex"],
});

export function deriveCategory(dirPath: string): string {
  const dirName = path.basename(dirPath).toLowerCase();

  for (const [category, patterns] of Object.entries(CATEGORY_MAP)) {
    for (const pat of patterns) {
      if (dirName.includes(pat)) {
        return category;
      }
    }
  }

  return "general";
}
