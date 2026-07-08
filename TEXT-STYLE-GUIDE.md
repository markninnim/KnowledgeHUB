# KnowledgeHUB™ — Text Style Guide

Reference for consistent typography across `public/index.html`. Font: **Plus Jakarta Sans** everywhere (body sets it; components should use `font-family:inherit`, never redeclare a different font).

## Core text colours

| Use | Colour |
|---|---|
| All titles/headings (h1, h2, h3) | `#003768` (navy) — no exceptions |
| All body text (paragraphs, table cells, names, stats, JS-rendered copy) | `#6b7c8f` — no exceptions |
| Placeholder / very muted (e.g. "learned" notes in tables) | `#9aa5b1` |
| Placeholder / very muted (e.g. "learned" notes in tables) | `#9aa5b1` |
| Success / target met | `#22c55e` / `#166534` |
| Warning / on track | `#854d0e` |
| Error / Non-CAS / destructive | `#ef4444` / `#b91c1c` |
| Sidebar section labels | `#fcb034` (orange) |

## Page title + subtitle

The standard header for any page or major section (e.g. AutoCPD™, Weekly Recordings, Advice Standards):

```html
<h2 style="color:#003768;font-size:20px;margin:0 0 4px;">Page Title</h2>
<p style="color:#6b7c8f;font-size:13.5px;margin:0;line-height:1.6;">
  One or two sentences in sentence case describing the page or section.
</p>
```

- Title: navy `#003768`, 20px, default (bold) weight, `margin:0 0 4px`.
- Subtitle: grey `#6b7c8f`, 13.5px, `line-height:1.6`, sentence case, no trailing full-width formatting. Max-width should match the width of the card/content below it (typically ~640px) rather than running edge-to-edge.
- Where a subtitle needs bottom spacing before the next block (no wrapping div margin available), keep that spacing on the `<p>` margin-bottom but keep the font styling identical.

Modal dialog headers (e.g. "Make My Business Card", "User Management") are intentionally smaller — 18px title, 13px subtitle — since they sit in a constrained popup context, not a full page.

## Card / content titles

- Card heading (`<h3>` inside asset/marketing cards): default browser `<h3>` sizing, navy or dark text, no special override needed beyond colour.
- Adviser/user name on cards and profile header: 13–14px on cards, 20px (`font-weight:800`) on the full profile page, always `#1a2a3a` or `#003768` if it's a clickable link.

## Body copy

- Default paragraph text: `#1a2a3a`, 13–14px depending on density of the surrounding UI.
- Descriptive/help text under a field or section: `#6b7c8f`, 12–13px.
- Table cell text: primary column (e.g. Activity) bold `#1a2a3a` 12–13px; secondary columns (Date, Category) regular weight `#6b7c8f`.
- Table header row (`<th>`): 10–11px, `font-weight:700`, `#6b7c8f`, uppercase, `letter-spacing:.4px`.

## Labels & pills

Standard pill: background `#dbeafe`, text `#003768`, `border-radius:20px` (10px for tiny badges), `font-size:10–11px`, `font-weight:700`.

Exceptions: CAS (green `#dcfce7`/`#166534`), Non-CAS (red `#fef2f2`/`#b91c1c`), status indicators (amber "On track" `#fef9c3`/`#854d0e`).

## Sidebar section headers

Orange caps: `font-size:10px;font-weight:700;letter-spacing:.08em;color:#fcb034;text-transform:uppercase;` — e.g. REPORTING, READING, KNOWLEDGE TESTS.

## Buttons

Button label text: `#6b7c8f`, `font-weight:600–700`, 12–14px depending on button size. Hover: text turns navy `#003768`. See brand rules for border/background conventions.

## Referencing UI elements in body text

When naming a button in prose, use `<strong>` with the button's exact capitalisation and no quotes:

> Click <strong>Stop &amp; Log CPD</strong> when you're done.

## Numbers & stats

Large stat figures (e.g. "12" entries, CPD totals): bold, navy (or red for Non-CAS counts), 20–28px depending on prominence, with a smaller uppercase label beside/below in grey 10–11px.

## Dates

Format consistently as `D MMM YYYY` (e.g. "8 Jul 2026") via `toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })`. Avoid mixing date formats (e.g. `DD/MM/YYYY`) within the same page.

## General rules

- Never hard-code a font-family other than Plus Jakarta Sans; always inherit.
- Keep grey text at `#6b7c8f` — don't introduce new near-grey shades unless matching an established exception (e.g. table "learned" notes use a lighter mid-grey for de-emphasis).
- Sentence case for subtitles and body copy; avoid Title Case except in headings and pill labels.
- Trademark symbols: KnowledgeHUB™ and AutoCPD™ must always carry `&#8482;` in user-facing text.
