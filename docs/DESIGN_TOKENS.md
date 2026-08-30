# DESIGN_TOKENS.md
# EquineSync Design Tokens

> **RECONCILED (Phase 1):** This file has been reconciled to match the authoritative `BRAND_AND_LOGO_GUIDE.md` (Brand Guide 22). The earlier earth-toned palette is **DEPRECATED** and must not be used going forward unless explicitly reintroduced later as a secondary seasonal/accent palette. See `DECISION_LOG.md` entry 2026-05-30.

## Colors

### Primary Foundation
| Token | Hex | Usage |
|---|---|---|
| `--es-graphite` | `#232734` | Midnight Graphite — sidebars, headers, hero, dark surfaces |
| `--es-navy` | `#2E3550` | Slate Navy — panels, nav, interactive states, buttons, cards |
| `--es-white` | `#F7F8FA` | Frost White — primary background, forms |
| `--es-mist` | `#E3E6EB` | Platinum Mist — cards, dividers, borders, table bg |

### Accent System
| Token | Hex | Usage |
|---|---|---|
| `--es-lilac` | `#B8AECF` | Smoky Lilac — primary accent, buttons, highlights |
| `--es-lavender` | `#D8D2E3` | Frosted Lavender Gray — hover, soft fills, empty states |
| `--es-ice` | `#DCEAF4` | Ice Blue — informational UI, charts, data cues |
| `--es-silver` | `#BCC9D6` | Glacier Silver Blue — secondary charts, inactive |

### Typography Colors
| Token | Hex | Usage |
|---|---|---|
| `--es-text` | `#1E2128` | Rich Charcoal — primary text, headings |
| `--es-muted` | `#667085` | Muted Slate — supporting text, metadata |
| `--es-disabled` | `#98A2B3` | Soft Disabled — placeholders, inactive |

### Status Colors
| Token | Hex | Usage |
|---|---|---|
| `--es-success` | `#7FA98B` | muted sage — completed, confirmations |
| `--es-warning` | `#D7B67A` | warm warning — attention, upcoming care |
| `--es-critical` | `#B46A6A` | muted oxblood — urgent/health alerts |

### Gradients
- Sidebar: `#232734 → #2E3550`
- Frost: `#F7F8FA → #ECEFF4`
- Lilac Atmosphere: `#D8D2E3 → #E8E3EF`

## Typography
| Token | Value |
|---|---|
| Display | **Cormorant Garamond** (SemiBold for headlines) |
| UI / Body | **Inter** (Regular body, Medium navigation) |

> Identity line: **"Every Horse. Every Task. In Sync."**

## Border Radius
| Token | Value |
|---|---|
| Small | 6px |
| Medium | 10px |
| Large | 16px |
| Card (brand) | 18px |

## Shadows
Subtle only. Avoid aggressive shadows. Brand card shadow: `0 2px 12px rgba(35,39,52,0.04)`.

## Spacing Scale
`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64`

## Mobile Breakpoints
| Name | Range |
|---|---|
| Mobile | 0–767 |
| Tablet | 768–1023 |
| Desktop | 1024+ |

## Canonical CSS Variables (from Brand Guide)
```css
:root {
  --es-graphite: #232734;
  --es-navy:     #2E3550;
  --es-white:    #F7F8FA;
  --es-mist:     #E3E6EB;
  --es-lilac:    #B8AECF;
  --es-lavender: #D8D2E3;
  --es-ice:      #DCEAF4;
  --es-silver:   #BCC9D6;
  --es-text:     #1E2128;
  --es-muted:    #667085;
  --es-disabled: #98A2B3;
  --es-success:  #7FA98B;
  --es-warning:  #D7B67A;
  --es-critical: #B46A6A;
}
```

> **Implementation status:** Runtime CSS and Tailwind tokens now expose the approved Valencia brand names directly. New UI should use the lavender, lilac, ice, silver-blue, ivory/frost, slate, and graphite naming system.
