---
name: design-taste-frontend
description: Produce frontend UI with strong taste — deliberate layout, typography, motion, and spacing — instead of generic, template-like AI output. Use when building or redesigning any web/mobile UI (Next.js, React, Vue, Svelte), turning a design comp/image into code, or polishing an existing interface. Pairs with the uncodixify rule (what NOT to do) by providing the positive direction (what TO do) and three explicit dials. Sources the upstream taste-skill (Leonxlnx/taste-skill).
---

# Design Taste — Frontend

Local wrapper for the upstream **taste-skill** (`Leonxlnx/taste-skill`). Where
`rules/uncodixify.md` lists the banned AI-slop patterns (what NOT to do), this
skill carries the *positive* design direction and the dials that make output feel
human-designed and intentional.

## When to Use

- Building or redesigning any UI (merchscene, ESCAPE-TOUR, ac-logistik, dashboards, Shopify themes)
- Image-to-code: a design comp/screenshot needs to become real components
- Polishing an existing interface that feels generic or "AI-made"

## Three Dials

Set these explicitly at the start of a UI task (1–10 scale) so the output matches
the project, instead of defaulting to safe-and-boring:

| Dial | Low (1–3) | High (8–10) |
|------|-----------|-------------|
| `DESIGN_VARIANCE` | Centered, clean, conventional | Asymmetric, editorial, modern layouts |
| `MOTION_INTENSITY` | Subtle hover states only | Scroll-driven, magnetic, GSAP interactions |
| `VISUAL_DENSITY` | Spacious, marketing-style | Dense, information-rich dashboards |

Sensible defaults by project type:
- **Marketing/landing** (ac-logistik, ESCAPE-TOUR): VARIANCE 6–8, MOTION 5–7, DENSITY 3–5
- **Commerce/app** (merchscene, moment): VARIANCE 4–6, MOTION 3–5, DENSITY 5–7
- **Ops dashboards** (social-, google-ads-dashboard): VARIANCE 3–4, MOTION 2–3, DENSITY 7–9

## Workflow

1. **Read `rules/uncodixify.md` first** — it is the hard constraint. Never ship the banned patterns (gradient text, floating shells, oversized radii, dramatic shadows, hero blocks in dashboards).
2. Pick the three dials for this surface.
3. Establish the system before components: type scale, spacing scale, one accent, real content.
4. Build components against the dials; audit each against the uncodixify checklist.
5. For motion, prefer GSAP/Framer with restraint — motion serves hierarchy, not decoration.

## Upstream variants (install on demand)

The full upstream skill set can be vendored when a specific flavor is needed:

```bash
# default v2 (this wrapper documents it)
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"

# specialized flavors
npx skills add https://github.com/Leonxlnx/taste-skill --skill "image-to-code"              # comp → code
npx skills add https://github.com/Leonxlnx/taste-skill --skill "redesign-existing-projects" # audit & improve
npx skills add https://github.com/Leonxlnx/taste-skill --skill "high-end-visual-design"     # premium/soft
npx skills add https://github.com/Leonxlnx/taste-skill --skill "minimalist-ui"              # editorial/Notion-style
npx skills add https://github.com/Leonxlnx/taste-skill --skill "industrial-brutalist-ui"    # Swiss/brutalist
```

When vendoring the upstream files into `~/.claude/skills/`, sync them back into this
repo per the CLAUDE.md sync workflow so the backup stays the source of truth.
