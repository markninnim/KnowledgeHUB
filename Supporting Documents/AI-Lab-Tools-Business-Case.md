# Business Case: AI-Assisted Tools in KnowledgeHUB™ (Payslip Check, Bank Statement Check & KnowledgeHELPER™)

**Prepared for:** Finance Planning Group internal review
**Date:** 17 July 2026

## Purpose

This note sets out the business case for using Anthropic's Claude AI model, via the Claude API, to power two tools in the KnowledgeHUB™ "Lab" section: **Payslip Check** and **Bank Statement Check**. These tools give users an automated first-pass review of customer-submitted payslips and bank statements, flagging inconsistencies or signs of tampering before a case proceeds.

It also covers **KnowledgeHELPER™**, the site-wide Help widget, for completeness — but as set out below, KnowledgeHELPER™ is rule-based rather than AI-powered, so it does not carry the same data-handling considerations as the Lab tools.

## What the tools do

Payslip Check and Bank Statement Check let a KnowledgeHUB™ user upload a customer's payslip and/or bank statement. The document is sent to Claude, which performs a forensic-style review — checking for arithmetic inconsistencies, formatting irregularities, mismatched dates, and other anomalies associated with altered or fraudulent documents. Bank Statement Check can also cross-reference an uploaded payslip against a bank statement to confirm that stated income actually appears as deposited income. The tool returns a risk rating, a plain-English summary, and a list of specific checks and flags, which the user then uses as one input into their own underwriting/compliance judgement — it does not make an automated decision on its own.

## Why this needs an AI model

Manually cross-checking a payslip and bank statement line-by-line for consistency is slow and inconsistent between reviewers. A large language model can read an unstructured document (a scanned or photographed statement, in whatever format the customer's bank or employer uses) and apply the same checklist of fraud indicators every time, at speed. This is the kind of task AI is well suited to and manual review is not: it doesn't replace the supervisor's judgement, it gives them a faster, more consistent starting point.

## How the data is handled

The way these tools work has been designed to keep customer data exposure to a minimum.

The document a user uploads is read in the browser, sent once to the KnowledgeHUB server, and forwarded directly to Anthropic's Claude API for analysis. Nothing is written to disk or saved into Airtable at any point in this process — once the API returns its result, the document itself is discarded from server memory. There is no copy of the document sitting in a second system.

The report Claude generates is also written so that it doesn't repeat the customer's identifying details back — no name, National Insurance number, account number, sort code, or address appears in the output. The report deals only in findings ("figures across pages are inconsistent," "date formatting differs from the stated provider's usual layout") rather than restating personal data.

These tools are available to KnowledgeHUB™ users generally, not restricted to supervisors and admins.

## How this fits with our existing data handling

FPG already collects and retains customer documents such as payslips and bank statements for six years, as part of our normal case files, and this is already covered under our existing privacy policy. That six-year retention is our own record-keeping obligation and happens regardless of whether the Lab tools are used.

Sending a document to Claude for this one-off analysis does not create a new retention point or a new copy of the document that sits outside our existing systems. It is a processing step — the document passes through the API call and the output is returned — not a place where the document is additionally stored. Anthropic's own standard policy is to delete API inputs and outputs within 30 days by default, and not to use API data to train its models. So the practical effect is that the *only* place this document is retained on an ongoing basis is FPG's own systems, under the six-year policy we already operate and disclose to customers.

## Safeguards already in place

- No server-side storage of uploaded documents — processed once, then discarded.
- AI-generated reports are written to avoid repeating personal identifiers.
- Available to KnowledgeHUB™ users generally, as an assistive check rather than an automated decision.
- Underlying documents remain governed by FPG's existing six-year retention policy and privacy policy — this feature doesn't change that.
- Anthropic does not train its models on API inputs/outputs by default, and API data is deleted within 30 days under its standard terms.

## Note on KnowledgeHELPER™

KnowledgeHELPER™, the Help widget available site-wide, works differently. It answers questions by running deterministic lookups against KnowledgeHUB's own Airtable data (e.g. broker counts, review leaderboards, a user's own clients or leads) rather than sending queries to Claude or any other AI model. It does not process customer documents and doesn't raise the same Claude API data-handling questions covered above. It's mentioned here only so this document gives a complete picture of "AI-labelled" features in KnowledgeHUB™ — in practice, Payslip Check and Bank Statement Check are the only features that call an external AI model.

## Recommendation

Continue using the Payslip Check and Bank Statement Check tools as an assistive screening step available to KnowledgeHUB™ users. As usage grows, it would be worth considering whether a Zero Data Retention (ZDR) agreement with Anthropic — which removes even the 30-day default retention window on their side — is a worthwhile additional safeguard; this is a separate commercial arrangement negotiated directly with Anthropic's sales team, not something available automatically on the current plan.
