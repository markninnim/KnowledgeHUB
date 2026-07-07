# KnowledgeHUB — project conventions

FPG Brand Hub / KnowledgeHUB. Node + Express + vanilla HTML/CSS/JS (single-page `public/index.html`, inline styles). Deployed on Railway via GitHub push.

## Brand rules (always apply)

- **Buttons (all forms):** transparent background, `1.5px solid #d1d5db` grey border, `#6b7c8f` grey text, border-radius 8px, font-weight 600–700. Hover: border and text turn navy `#003768`. No solid navy default state.
- **Standard label/pill:** background `#dbeafe` (light blue), text `#003768` (dark navy), border-radius 20px (10px for tiny badges). Applies to category/type/product labels. Exceptions: CAS (green `#dcfce7`/`#166534`), Non-CAS (red `#fef2f2`/`#b91c1c`), status indicators (e.g. amber "On track").
- **Sidebar section headers:** orange caps — `font-size:10px; font-weight:700; letter-spacing:.08em; color:#fcb034;` (e.g. REPORTING, READING, KNOWLEDGE TESTS).
- **Core colours:** navy `#003768`, orange `#fcb034`, muted text `#6b7c8f`, borders `#e8ecf0`, page text `#1a2a3a`.
- Subtitle/intro text under page titles: max-width matching the form/card below it (typically 640px), `line-height:1.6`.
- **Referencing buttons/actions in body text:** sentence-case grey text with the button name in `<strong>` using the button's exact capitalisation, no quotes — e.g. "Click <strong>Stop &amp; Log CPD</strong> when you're done."

## Naming

- Product is **KnowledgeHUB™** (`KnowledgeHUB&#8482;` in user-facing text; not Knowledge Hub / FPG Knowledge Hub / DAM).
- CPD feature is **AutoCPD™** (`AutoCPD&#8482;`).
- "Learning Zone" renamed to **Learning** in UI copy only — internal `source: 'Learning Zone'` data values must NOT be renamed (matched against Airtable history and icon logic).

## Airtable

- Base `appqQv0Xog8yZMwI9`. Tables: Users, Learning Videos, CPD Log, Feefo, News, CAS Path, Compliance Reports (`tblG1vsuA3GZb38nk`).
- Always use field IDs (server.js consts), `typecast: true` on Compliance Report creates so new select choices auto-create.

## Compliance > REPORTING forms

Six forms share one section (`section-cr`) + `CR_CONFIG` in index.html: Complaint, Breach, Conflict of Interest, Gifts & Hospitality, Self Sale, Whistleblowing. Server: `/api/compliance-report` (POST, auth), `/api/compliance-reports` (GET, admin).
