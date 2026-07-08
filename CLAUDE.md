# KnowledgeHUB — project guide

FPG Brand Hub / **KnowledgeHUB™** — Finance Planning Group's password-gated intranet for mortgage & protection advisers. Brand assets, marketing templates, Learning (videos/tests/reading), AutoCPD™ logging, Pay statements, compliance reporting, team management.

## Stack & deployment

- Node.js + Express (`server.js`, single ~5,000-line file) with session auth (express-session, bcryptjs, speakeasy 2FA).
- Vanilla HTML/CSS/JS — **single-page `public/index.html`** (~11,500 lines, inline styles, no build step). Separate auth pages: login, 2fa, 2fa-setup, forgot-password, reset-password.
- Data lives in **Airtable** (users, CPD, videos, Feefo, news, CAS path, compliance reports) plus small local JSON files (marketing-users, extra-products, features, asset-dates).
- Deployed on **Railway**, triggered by push to GitHub `markninnim/KnowledgeHUB` (main). User runs git commands themselves in Terminal — provide them ready to paste:
  `git add … && git commit -m "…" && git push`
- Font: **Plus Jakarta Sans** everywhere (Google Fonts; body sets it, components use `font-family:inherit`).

## Brand rules (always apply)

- **Buttons (all forms):** transparent background, `1px solid #d1d5db` grey border, `#6b7c8f` grey text, border-radius 8px, font-weight 600–700. Hover: border and text turn navy `#003768`. **No solid navy default state.** Exception: toggle buttons (e.g. Month/Quarter/Year, Cards/List) keep a navy filled *active* state.
- **Standard label/pill:** background `#dbeafe` (light blue), text `#003768` (dark navy), border-radius 20px (10px for tiny badges). Applies to category/type/product labels. Exceptions: CAS (green `#dcfce7`/`#166534`), Non-CAS (red `#fef2f2`/`#b91c1c`), status indicators (e.g. amber "On track" `#fef9c3`/`#854d0e`).
- **Sidebar section headers:** orange caps — `font-size:10px;font-weight:700;letter-spacing:.08em;color:#fcb034;` (e.g. REPORTING, READING, KNOWLEDGE TESTS).
- **Core colours:** navy `#003768`, orange `#fcb034`, muted text `#6b7c8f`, borders `#e8ecf0`, page text `#1a2a3a`, page bg `#f5f7fa`.
- Subtitle/intro text under page titles: grey `#6b7c8f` 13.5px, sentence case, `line-height:1.6`, max-width matching the card below (typically 640px).
- **Referencing buttons in body text:** button name in `<strong>` with the button's exact capitalisation, no quotes — "Click <strong>Stop &amp; Log CPD</strong> when you're done."

## Naming

- Product is **KnowledgeHUB™** (`KnowledgeHUB&#8482;` in user-facing text). Never Knowledge Hub / FPG Knowledge Hub / DAM.
- CPD feature is **AutoCPD™** (`AutoCPD&#8482;`).
- "Learning Zone" renamed to **Learning** in UI copy only — internal `source: 'Learning Zone'` data values must NOT be renamed (matched against Airtable history and icon logic).

## Airtable (base `appqQv0Xog8yZMwI9`)

| Table | ID | Notes |
|---|---|---|
| Users | `tbltcinwWF3FXDGre` | auth + profile; Birthday `fldUxRahlmboP7g4y`, Start Date `fldA7RE4kgsGwqvad` |
| Learning Videos | `tblGxOMw9SDUlzw1h` | |
| CPD Log | `tblajx6AAKFtI6K1N` | source values incl. 'Learning Zone' |
| Feefo | `tblU58wJ0rNFPMiKp` | reviews |
| News | `tbltfeViC5SfCniWt` | bulletins; + Add Story posts here |
| CAS Path | `tblY3lKPcIQCbCoFP` | |
| Compliance Reports | `tblG1vsuA3GZb38nk` | six REPORTING forms |

- Always use **field IDs** (declared as consts near the top of each server.js section), never field names.
- Use `typecast: true` on Compliance Report creates so new Type select choices auto-create.
- Server reads `AIRTABLE_API_KEY` from env (Railway); no key locally, so the server can't be fully run locally without env vars.

## Key features & where they live

- **Compliance tab:** AutoCPD™ (`section-cpd`) + six REPORTING forms sharing one section (`section-cr`) driven by `CR_CONFIG` in index.html: Complaint, Breach, Conflict of Interest, Gifts & Hospitality, Self Sale, Whistleblowing. Server: `POST /api/compliance-report` (auth), `GET /api/compliance-reports` (admin).
- **Learning tab:** View Live (Zoom link, logs 50/50 CPD via `lvLogLiveCpd`), Weekly/Induction/Revalidation recordings, Monthly Newsletters (logs 20 min CPD), Industry Reading (timed CPD), Knowledge Tests (`KT_TESTS`), Fitness & Properness questionnaire. Section switching: `showLvSection` / `ktNavLoad` / `showFpForm` — each hides ALL other Learning sections (keep their section lists in sync; historic bug when lists drift).
- **Home:** quick links, News Bulletins scroller (+ Add Story button for supervisors/admins → `news-modal` → `POST /api/news-bulletin`), CPD summary, birthday card (shows if `_currentUser.birthday` is today).
- **My Team (Supervisor Zone):** adviser cards/list with CPD bars, 🎂 next to name on their birthday (`_svBirthdayCake`), drill-down, CSV export, transfer.
- **User management (admin):** users table with product pills, CSV import/export.
- **PDF generation:** business cards, moving cards, DIP certificates, CPD record — pdf-lib with Plus Jakarta Sans TTFs in `public/static/fonts/`.
- Role flags on session user: `isAdmin`, `isSupervisor`, `isMarketing`; helpers `_isActingSupervisor()` etc. Supervisor/admin UI is unhidden in the post-login block around `user && (user.isSupervisor || user.isAdmin)` in index.html.

## Verification before handing back

- `node --check server.js`
- Extract inline scripts from index.html and `node --check` them:
  `python3 -c "import re;open('/tmp/all.js','w').write('\n'.join(re.findall(r'<script>(.*?)</script>', open('public/index.html').read(), re.S)))" && node --check /tmp/all.js`

## Related projects

- **SurveyingHUB** (`~/Documents/Claude/Projects/SurveyingHUB`) — sister site, same Plus Jakarta Sans typography; reference for shared styling.
