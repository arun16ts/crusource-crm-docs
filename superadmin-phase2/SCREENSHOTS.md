# Phase 2 screenshots

Captures use real compiled CSS and loaded Instrument Sans. Platform screenshots come from actual Next.js routes with the real isolated API. Names and email addresses are synthetic.

| Screen | Capture |
|---|---|
| Invitations, desktop | [1440px](screenshots/platform-access-1440.png) |
| Invitations, intermediate widths | [1024px](screenshots/platform-access-1024.png), [768px](screenshots/platform-access-768.png) |
| Invitations, mobile | [390px](screenshots/platform-access-390.png) |
| Mobile navigation | [390px overlay](screenshots/platform-mobile-navigation-390.png) |
| Collapsed sidebar | [1440px](screenshots/platform-access-collapsed-1440.png) |
| CSS 200% zoom | [Zoom capture](screenshots/platform-access-zoom-200.png) |
| Staff sign-in | [1440px](screenshots/platform-login-1440.png) |
| Dutch platform locale | [1440px](screenshots/platform-access-nl-1440.png) |

The mobile table scrolls horizontally inside its focusable labeled region; the document itself does not overflow. Email/provider status does not imply mailbox receipt.

CRM presentation regression pairs are named `crm-frame-before-<width>.png` and `crm-frame-after-<width>.png`, with a separate `1440-collapsed` pair. All five pairs were pixel-identical. They use the actual CRM frame components with deterministic domain effects. See [comparison metrics](crm-frame-verification.json) and [test scope](VERIFICATION.md).
