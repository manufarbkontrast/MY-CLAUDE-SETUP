#!/usr/bin/env python3
"""Suggest skills/agents and generate an improved prompt template.

The tool scans local `skills/` and `agents/` directories, scores matches based on
keywords, and emits a structured prompt the user can paste directly.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

WORD_RE = re.compile(r"[a-z0-9][a-z0-9+._-]*", re.IGNORECASE)
FRONTMATTER_NAME_RE = re.compile(r"^name:\s*['\"]?(.+?)['\"]?\s*$", re.IGNORECASE)
FRONTMATTER_DESC_RE = re.compile(r"^description:\s*['\"]?(.+?)['\"]?\s*$", re.IGNORECASE)
EXPLICIT_TAG_RE = re.compile(r"\$(?P<id>[a-zA-Z0-9._-]+)")
EXPLICIT_AGENT_RE = re.compile(r"@(?P<id>[a-zA-Z0-9._-]+)")

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "auf",
    "bei",
    "build",
    "by",
    "das",
    "dem",
    "den",
    "der",
    "die",
    "ein",
    "eine",
    "einer",
    "eines",
    "es",
    "for",
    "fuer",
    "für",
    "ich",
    "in",
    "is",
    "it",
    "mit",
    "my",
    "of",
    "or",
    "the",
    "to",
    "und",
    "von",
    "wie",
    "with",
    "zu",
}

# Curated intent mapping for high-confidence recommendations.
INTENT_SKILLS: Dict[str, Sequence[str]] = {
    "debug": ("systematic-debugging", "root-cause-tracing", "verification-before-completion"),
    "bug": ("systematic-debugging", "tdd-workflow", "verification-before-completion"),
    "review": ("code-review", "verification-before-completion"),
    "security": ("security-review", "api-security-hardening", "csrf-protection"),
    "auth": ("auth-implementation-patterns", "api-authentication", "session-management"),
    "payment": ("payment-integration", "stripe-integration", "pci-compliance"),
    "payments": ("payment-integration", "stripe-integration", "pci-compliance"),
    "dashboard": ("kpi-dashboard-design", "frontend-design", "responsive-design"),
    "saas": ("technical-specification", "prompt-optimizer", "tdd-workflow"),
    "api": ("rest-api-design", "api-design-principles", "api-error-handling"),
    "frontend": ("frontend-design", "ui-styling", "responsive-design"),
    "react": ("frontend-patterns", "react-composition-patterns", "vitest-testing"),
    "next": ("nextjs-app-router-patterns", "vercel-react-best-practices"),
    "nuxt": ("nuxt-core", "nuxt-data", "nuxt-production"),
    "cloudflare": ("cloudflare-manager", "workers-dev-experience", "workers-security"),
    "worker": ("workers-runtime-apis", "workers-performance", "workers-security"),
    "bun": ("bun-runtime", "bun-package-manager", "bun-bundler"),
    "test": ("tdd-workflow", "vitest-testing", "playwright"),
    "performance": ("web-performance-optimization", "sql-optimization-patterns"),
    "database": ("database-schema-design", "postgres-patterns", "sql-optimization-patterns"),
    "sql": ("sql-optimization-patterns", "postgres-patterns"),
    "docs": ("docs-seeker", "technical-specification", "doc-coauthoring"),
    "prompt": ("prompt-optimizer", "prompt-engineering-patterns"),
}

INTENT_AGENTS: Dict[str, Sequence[str]] = {
    "debug": ("debugger", "error-detective", "code-reviewer"),
    "review": ("code-reviewer", "security-reviewer", "architect-review"),
    "security": ("security-reviewer", "backend-security-coder"),
    "auth": ("backend-security-coder", "auth-tester", "backend-architect"),
    "payment": ("payment-integration", "security-reviewer", "backend-architect"),
    "payments": ("payment-integration", "security-reviewer", "backend-architect"),
    "dashboard": ("ui-ux-designer", "frontend-developer", "frontend-tester"),
    "saas": ("planner", "backend-architect", "frontend-developer"),
    "frontend": ("frontend-developer", "ui-ux-designer", "frontend-tester"),
    "react": ("frontend-developer", "frontend-tester"),
    "api": ("backend-architect", "api-documenter"),
    "database": ("database-architect", "database-optimizer"),
    "sql": ("sql-pro", "database-optimizer"),
    "cloudflare": ("cloud-architect", "workers-security-auditor", "workers-performance-analyzer"),
    "bun": ("bun-troubleshooter", "bun-performance-analyzer"),
    "test": ("test-automator", "e2e-runner"),
    "prompt": ("prompt-engineer",),
}


@dataclass
class CatalogItem:
    id: str
    description: str
    keywords: set[str]


@dataclass
class Suggestion:
    skills: List[str]
    agents: List[str]
    score_debug: Dict[str, List[Tuple[str, int]]]


@dataclass
class InteractiveAnswers:
    base_prompt: str
    stack: str
    style: str
    domain: str
    features: str
    output_pref: str
    checks: str
    constraints: str


def tokenize(text: str) -> List[str]:
    tokens = [match.group(0).lower() for match in WORD_RE.finditer(text.lower())]
    return [t for t in tokens if len(t) > 1 and t not in STOPWORDS]


def _frontmatter(raw: str) -> Tuple[str | None, str | None]:
    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None

    name: str | None = None
    description: str | None = None
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            break
        if name is None:
            m_name = FRONTMATTER_NAME_RE.match(stripped)
            if m_name:
                name = m_name.group(1).strip()
                continue
        if description is None:
            m_desc = FRONTMATTER_DESC_RE.match(stripped)
            if m_desc:
                description = m_desc.group(1).strip()
    return name, description


def load_skills(skills_dir: Path) -> Dict[str, CatalogItem]:
    catalog: Dict[str, CatalogItem] = {}
    for skill_file in skills_dir.rglob("SKILL.md"):
        if not skill_file.is_file():
            continue
        raw = skill_file.read_text(encoding="utf-8", errors="ignore")
        fm_name, fm_desc = _frontmatter(raw)
        skill_id = (fm_name or skill_file.parent.name).strip()
        description = (fm_desc or "").strip()
        base = f"{skill_id} {description} {skill_file.parent.as_posix()}"
        keywords = set(tokenize(base))
        catalog[skill_id] = CatalogItem(id=skill_id, description=description, keywords=keywords)
    return catalog


def load_agents(agents_dir: Path) -> Dict[str, CatalogItem]:
    catalog: Dict[str, CatalogItem] = {}
    for agent_file in agents_dir.glob("*.md"):
        if not agent_file.is_file():
            continue
        agent_id = agent_file.stem
        raw = agent_file.read_text(encoding="utf-8", errors="ignore")
        snippet = " ".join(raw.splitlines()[:20])
        keywords = set(tokenize(f"{agent_id} {snippet}"))
        catalog[agent_id] = CatalogItem(id=agent_id, description="", keywords=keywords)
    return catalog


def score_catalog(
    prompt_tokens: set[str],
    catalog: Dict[str, CatalogItem],
    extra_boost: Iterable[str],
    explicit: set[str],
    top_n: int,
    min_score: int = 2,
) -> List[Tuple[str, int]]:
    scores: List[Tuple[str, int]] = []
    boost_set = set(extra_boost)

    for item_id, item in catalog.items():
        overlap = len(prompt_tokens & item.keywords)
        if item_id in boost_set:
            overlap += 4
        if item_id in explicit:
            overlap += 10
        if overlap >= min_score or item_id in explicit:
            scores.append((item_id, overlap))

    scores.sort(key=lambda x: (-x[1], x[0]))

    ordered: List[Tuple[str, int]] = []
    seen = set()
    for item_id, score in scores:
        if item_id in seen:
            continue
        seen.add(item_id)
        ordered.append((item_id, score))
        if len(ordered) >= top_n:
            break
    return ordered


def detect_intents(tokens: set[str]) -> Tuple[List[str], List[str]]:
    matched_skill_ids: List[str] = []
    matched_agent_ids: List[str] = []

    for keyword, mapped in INTENT_SKILLS.items():
        if keyword in tokens:
            matched_skill_ids.extend(mapped)

    for keyword, mapped in INTENT_AGENTS.items():
        if keyword in tokens:
            matched_agent_ids.extend(mapped)

    return matched_skill_ids, matched_agent_ids


def extract_explicit(prompt: str) -> Tuple[set[str], set[str]]:
    explicit_skills = {m.group("id") for m in EXPLICIT_TAG_RE.finditer(prompt)}
    explicit_agents = {m.group("id") for m in EXPLICIT_AGENT_RE.finditer(prompt)}
    return explicit_skills, explicit_agents


def suggest(
    prompt: str,
    skill_catalog: Dict[str, CatalogItem],
    agent_catalog: Dict[str, CatalogItem],
    top_skills: int,
    top_agents: int,
) -> Suggestion:
    prompt_tokens = set(tokenize(prompt))
    explicit_skills, explicit_agents = extract_explicit(prompt)
    intent_skill_boosts, intent_agent_boosts = detect_intents(prompt_tokens)

    scored_skills = score_catalog(
        prompt_tokens=prompt_tokens,
        catalog=skill_catalog,
        extra_boost=intent_skill_boosts,
        explicit=explicit_skills,
        top_n=top_skills,
    )
    scored_agents = score_catalog(
        prompt_tokens=prompt_tokens,
        catalog=agent_catalog,
        extra_boost=intent_agent_boosts,
        explicit=explicit_agents,
        top_n=top_agents,
    )

    # Always enforce the completion guardrails if available.
    for required in ("code-review", "verification-before-completion"):
        if required in skill_catalog and required not in [x[0] for x in scored_skills]:
            scored_skills.append((required, 1))

    skills = [item_id for item_id, _ in scored_skills]
    agents = [item_id for item_id, _ in scored_agents]

    return Suggestion(
        skills=skills,
        agents=agents,
        score_debug={
            "skills": scored_skills,
            "agents": scored_agents,
        },
    )


def split_prompt_context(prompt: str) -> Tuple[str, str]:
    cleaned = prompt.strip()
    if not cleaned:
        return "", ""

    separators = [" mit ", " with ", " using ", " für ", " fuer ", " in "]
    lower = cleaned.lower()
    for sep in separators:
        idx = lower.find(sep)
        if idx > 12:
            task = cleaned[:idx].strip(" ,.;")
            context = cleaned[idx + len(sep) :].strip(" ,.;")
            return task, context

    return cleaned, ""


def format_prompt(original_prompt: str, suggestion: Suggestion) -> str:
    task, context = split_prompt_context(original_prompt)
    skill_line = " ".join(f"${x}" for x in suggestion.skills)
    agent_line = " ".join(f"@{x}" for x in suggestion.agents) if suggestion.agents else ""

    lines = [
        f"Skills: {skill_line}" if skill_line else "Skills:",
        f"Agents: {agent_line}" if agent_line else "Agents:",
        f"Aufgabe: {task or original_prompt.strip()}",
        f"Kontext: {context or 'Projektpfad, relevante Dateien, Constraints ergänzen.'}",
        "Regeln: Keine unnötigen Änderungen, bestehende Patterns beibehalten, Sicherheit und Tests berücksichtigen.",
        "Output: Konkrete Änderungen mit betroffenen Dateien, kurzer Begründung und klaren Next Steps.",
        "Check: Relevante Tests/Lint/Build ausführen und Ergebnisse nennen.",
    ]
    return "\n".join(lines)


def format_prompt_from_answers(answers: InteractiveAnswers, suggestion: Suggestion) -> str:
    skill_line = " ".join(f"${x}" for x in suggestion.skills)
    agent_line = " ".join(f"@{x}" for x in suggestion.agents) if suggestion.agents else ""
    context_bits: List[str] = []
    if answers.stack:
        context_bits.append(f"Stack={answers.stack}")
    if answers.style:
        context_bits.append(f"Stil={answers.style}")
    if answers.domain:
        context_bits.append(f"Bereich={answers.domain}")
    if answers.features:
        context_bits.append(f"Features={answers.features}")

    lines = [
        f"Skills: {skill_line}" if skill_line else "Skills:",
        f"Agents: {agent_line}" if agent_line else "Agents:",
        f"Aufgabe: {answers.base_prompt}",
        f"Kontext: {'; '.join(context_bits) if context_bits else 'Projektpfad, relevante Dateien, Constraints ergänzen.'}",
        (
            f"Regeln: {answers.constraints}"
            if answers.constraints
            else "Regeln: Keine unnötigen Änderungen, bestehende Patterns beibehalten, Sicherheit und Tests berücksichtigen."
        ),
        (
            f"Output: {answers.output_pref}"
            if answers.output_pref
            else "Output: Konkrete Änderungen mit betroffenen Dateien, kurzer Begründung und klaren Next Steps."
        ),
        (
            f"Check: {answers.checks}"
            if answers.checks
            else "Check: Relevante Tests/Lint/Build ausführen und Ergebnisse nennen."
        ),
    ]
    return "\n".join(lines)


def _option_prompt(label: str, options: Sequence[str]) -> str:
    print(f"\n{label}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    value = input("Auswahl (Nummer oder Freitext, Enter = überspringen): ").strip()
    if not value:
        return ""
    if value.isdigit():
        idx = int(value) - 1
        if 0 <= idx < len(options):
            return options[idx]
    return value


def run_interactive(base_prompt: str) -> InteractiveAnswers:
    print("Interaktiver Prompt Enhancer")
    if not base_prompt.strip():
        base_prompt = input("1) Was willst du bauen/ändern? ").strip()
    else:
        print(f"1) Basis-Prompt: {base_prompt}")

    stack = _option_prompt(
        "2) Tech-Stack?",
        ("React + Next.js", "Vue + Nuxt", "Cloudflare Workers", "Bun", "Python/FastAPI", "Node.js API"),
    )
    style = _option_prompt(
        "3) Stil/Ansatz?",
        ("Minimalistisch", "Luxury/Premium", "Brutalist/Editorial", "Performance-first", "Security-first"),
    )
    domain = _option_prompt(
        "4) Bereich?",
        ("SaaS", "E-Commerce", "Dashboard/Admin", "Content/Docs", "API-Backend", "Mobile"),
    )
    features = input("5) Kern-Features (kommagetrennt, z.B. auth, payments, tests): ").strip()
    constraints = input("6) Wichtige Regeln/Constraints: ").strip()
    output_pref = input("7) Gewünschtes Output-Format (z.B. Patch + kurze Erklärung): ").strip()
    checks = input("8) Welche Checks sollen laufen (z.B. lint,test,build): ").strip()

    return InteractiveAnswers(
        base_prompt=base_prompt,
        stack=stack,
        style=style,
        domain=domain,
        features=features,
        output_pref=output_pref,
        checks=checks,
        constraints=constraints,
    )


def build_enriched_prompt(answers: InteractiveAnswers) -> str:
    parts = [answers.base_prompt.strip()]
    context_bits: List[str] = []

    if answers.stack:
        context_bits.append(f"Stack: {answers.stack}")
    if answers.style:
        context_bits.append(f"Stil: {answers.style}")
    if answers.domain:
        context_bits.append(f"Bereich: {answers.domain}")
    if answers.features:
        context_bits.append(f"Features: {answers.features}")
    if answers.constraints:
        context_bits.append(f"Constraints: {answers.constraints}")
    if answers.output_pref:
        context_bits.append(f"Output: {answers.output_pref}")
    if answers.checks:
        context_bits.append(f"Checks: {answers.checks}")

    if context_bits:
        parts.append("mit " + "; ".join(context_bits))
    return " ".join(parts).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-enhance prompts with local skills and agents")
    parser.add_argument("prompt", nargs="*", help="Prompt text to optimize")
    parser.add_argument("--skills-dir", default="skills", help="Path to skills directory")
    parser.add_argument("--agents-dir", default="agents", help="Path to agents directory")
    parser.add_argument("--top-skills", type=int, default=6, help="Max suggested skills")
    parser.add_argument("--top-agents", type=int, default=3, help="Max suggested agents")
    parser.add_argument("--interactive", action="store_true", help="Ask guided questions before generating prompt")
    parser.add_argument("--json", action="store_true", help="Return JSON output")
    return parser.parse_args()


def resolve_catalog_dir(raw_path: str, fallback_root: Path) -> Path:
    """Resolve catalog directories robustly for any current working directory.

    Order:
    1) absolute path as-is
    2) relative to current working directory
    3) relative to repository root (parent of this script directory)
    """
    candidate = Path(raw_path).expanduser()
    if candidate.is_absolute():
        return candidate

    cwd_candidate = Path.cwd() / candidate
    if cwd_candidate.exists():
        return cwd_candidate

    return fallback_root / candidate


def main() -> int:
    args = parse_args()
    prompt = " ".join(args.prompt).strip()
    interactive_answers: InteractiveAnswers | None = None
    if args.interactive:
        interactive_answers = run_interactive(prompt)
        prompt = build_enriched_prompt(interactive_answers)

    if not prompt:
        raise SystemExit("Please provide a prompt text, e.g.: python3 scripts/prompt_enhancer.py 'baue api mit auth'")

    repo_root = Path(__file__).resolve().parent.parent
    skills_dir = resolve_catalog_dir(args.skills_dir, repo_root)
    agents_dir = resolve_catalog_dir(args.agents_dir, repo_root)

    if not skills_dir.exists() or not agents_dir.exists():
        raise SystemExit(
            "Could not find directories: "
            f"skills={skills_dir} agents={agents_dir}. "
            "Hint: run with --skills-dir/--agents-dir or from the repository root."
        )

    skill_catalog = load_skills(skills_dir)
    agent_catalog = load_agents(agents_dir)

    suggestion = suggest(
        prompt=prompt,
        skill_catalog=skill_catalog,
        agent_catalog=agent_catalog,
        top_skills=max(1, args.top_skills),
        top_agents=max(0, args.top_agents),
    )

    enhanced = (
        format_prompt_from_answers(interactive_answers, suggestion)
        if interactive_answers is not None
        else format_prompt(prompt, suggestion)
    )

    if args.json:
        result = {
            "prompt": prompt,
            "skills": suggestion.skills,
            "agents": suggestion.agents,
            "enhanced_prompt": enhanced,
            "score_debug": suggestion.score_debug,
            "catalog_sizes": {
                "skills": len(skill_catalog),
                "agents": len(agent_catalog),
            },
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(enhanced)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
