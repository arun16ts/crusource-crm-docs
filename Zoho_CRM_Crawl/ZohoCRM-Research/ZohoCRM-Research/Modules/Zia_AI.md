# Module — Zia AI

> Master Zia reference. Source-of-truth summary: see `../08_AI_Features.md`. This document focuses on the **Zia module UX surface** (notifications panel, Zia Notebook, Zia Assistants pane, etc.) rather than per-feature descriptions, which live in `08_AI_Features.md`.

## ZI.1 Surfaces inside Zoho CRM

- **Zia icon (top bar) / Bell-icon panel** — drop-down notifications issuing AI prompts.
- **Zia Notebook** — inside each Record page where supported, Zia insights appear inline (Lead Score, Churn Score, Best Time to Contact, Next Best Action).
- **Zia Writing Assistant** — sidebar when composing Email.
- **Zia Voice** (VoC) module (separate top-level menu in some orgs).
- **QuickML** — Manage ML Models menu (Ultimate).

## ZI.2 Trigger entry points for Zia

- Record create/update events feed learning engines.
- Email-related Zia features run on Incoming/Outgoing email ingestion.
- Call Zia features run on Call Recording upload.

## ZI.3 Edition gating (verbatim Pricing page hints)

- AI Sales assistant (Enterprise).
- Custom AI/Machine Learning (Ultimate — daily free QuickML calls).
- Most Predictive AI features gated to Enterprise / Ultimate per pricing page: "AI sales assistant (insights, predictions, and recommendations from Zia)".
- AI Agents listed in **Standard** edition ("AI agents — build and deploy to automate sales activities").

## ZI.4 Cross References

- `../08_AI_Features.md` — full verbatim feature list.
- `../Modules/Calls.md` — Call Transcription/Intelligence.
- `../Modules/Forecasts.md` — AI Forecasting.
