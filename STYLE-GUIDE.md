# KnowledgeHUB™ — Master Style Guide

Single source of truth for visual and typographic style across `public/index.html`. If anything here conflicts with what's currently in the code, the code is wrong — fix it to match this doc.

Font: **Plus Jakarta Sans** everywhere. Never hard-code another font-family; components should use `font-family:inherit`.

## Core colours

| Use | Colour |
|---|---|
| All titles/headings (h1, h2, h3) | `#003768` (navy) — no exceptions |
| All body text (paragraphs, table cells, names, stats, JS-rendered copy, inline `<strong>`/links inside body copy) | `#6b7c8f` — no exceptions |
| Names in the User Management admin list | `#003768` (navy) — approved exception to the body-text rule |
| Page background | `#f5f7fa` |
| CPD/product type colours | Mortgage `#003768` (navy), Protection `#fcb034` (amber), Investment `#fcb034` (amber) — where all three appear together (e.g. activity-type pills), Protection uses accent blue `#2e99d5` instead to stay distinct from Investment |
| Borders (default) | `#e8ecf0` or `#d1d5db` (see Borders section) |
| Sidebar section labels | `#fcb034` (orange) |
| Success / target met / CAS | `#22c55e` / `#166534` (pill bg `#dcfce7`) |
| Warning / on track | `#854d0e` (pill bg `#fef9c3`) |
| Error / Non-CAS / destructive | `#ef4444` / `#b91c1c` (pill bg `#fef2f2`) |
| Standard pill background | `#dbeafe` with `#003768` text |

Do not introduce new near-grey or near-navy shades. If existing code has a stray colour (e.g. `#374151`, `#2D3748`, `#4a5a6a`, `#1a2a3a`), it's a bug — replace it with `#6b7c8f` (body) or `#003768` (heading) as appropriate.

## No mixed colour within a block

Inside a single paragraph or subtitle, don't mix navy and grey for emphasis. `<strong>` and inline mailto/tel links inside body copy stay `#6b7c8f` — bold weight alone provides emphasis. Only headings, buttons, pills/badges, sidebar nav items, and standalone brand-coloured callout boxes get their own distinct colour.

## Page title + subtitle

Standard header for any page or major section:

```html
<h2 style="color:#003768;font-size:20px;margin:0 0 4px;">Page Title</h2>
<p style="color:#6b7c8f;font-size:13.5px;margin:0;line-height:1.6;">
  One or two sentences in sentence case describing the page or section.
</p>
```

- Title: navy, 20px, default (bold) weight, `margin:0 0 4px`.
- Subtitle: grey, 13.5px, `line-height:1.6`, sentence case, full width of the content column (no `max-width` constraint) unless it shares a flex row with another element (e.g. a search box) that needs the room.
- If a subtitle needs bottom spacing before the next block, put it on the `<p>` margin-bottom but keep the font styling identical.
- Modal dialog headers (e.g. "Make My Business Card", "User Management") are intentionally smaller — 18px title, 13px subtitle — since they're in a constrained popup, not a full page.

## Card / content titles

- Card heading (`<h3>` in asset/marketing cards): navy `#003768` per `.card h3` class, 14px.
- Adviser/user name: 13–14px on cards, 20px (`font-weight:800`) on the full profile page. Navy if it's a clickable link, otherwise grey per body-text rule.

## Table text

- Table header row (`<th>`): 10–11px, `font-weight:700`, grey, uppercase, `letter-spacing:.4px`.
- Table cell text: all grey `#6b7c8f`; bold weight (not colour) distinguishes the primary column (e.g. Activity/Date).

## Labels & pills

Standard pill: background `#dbeafe`, text `#003768`, `border-radius:20px` (10px for tiny badges), 10–11px, `font-weight:700`. Exceptions: CAS/Non-CAS/status pills use their own colour pairs (see Core colours).

## Sidebar section headers

Orange caps: `font-size:10px;font-weight:700;letter-spacing:.08em;color:#fcb034;text-transform:uppercase;` — e.g. REPORTING, READING, KNOWLEDGE TESTS.

## Buttons

- Transparent background, `1px solid #d1d5db` border, `#6b7c8f` text, `border-radius:8px`, `font-weight:600–700`, 12–14px depending on size.
- Hover: border and text turn navy `#003768`.
- No solid navy default state. Exception: toggle buttons (Month/Quarter/Year, Cards/List) keep a navy filled *active* state.

## Borders

All borders are `1px` — no `1.5px`/hairline borders anywhere. Deliberate accent weights (2px/3px/4px underlines, left-accent bars, the avatar ring) are a separate, intentional design choice and stay as-is; every plain container/input/card/date-picker border should be `1px solid #d1d5db` (or `#e8ecf0` for very subtle internal dividers).

## Referencing UI elements in body text

Name a button in prose using `<strong>` with its exact capitalisation, no quotes:

> Click <strong>Stop &amp; Log CPD</strong> when you're done.

## Numbers & stats

Large stat figures (e.g. "12" entries, CPD totals): bold, navy (or red for Non-CAS counts), 20–28px depending on prominence, with a smaller uppercase grey label beside/below (10–11px).

## Dates

Format as `D MMM YYYY` (e.g. "8 Jul 2026") via `toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })`. Don't mix formats (e.g. `DD/MM/YYYY`) within the same page.

## Naming

- Product is **KnowledgeHUB™** (`KnowledgeHUB&#8482;`) — never "Knowledge Hub" / "FPG Knowledge Hub" / "DAM".
- CPD feature is **AutoCPD™** (`AutoCPD&#8482;`).
- "Learning Zone" is renamed to **Learning** in UI copy only — internal `source: 'Learning Zone'` data values must not change.
- Sentence case for subtitles and body copy; Title Case reserved for headings and pill labels.
