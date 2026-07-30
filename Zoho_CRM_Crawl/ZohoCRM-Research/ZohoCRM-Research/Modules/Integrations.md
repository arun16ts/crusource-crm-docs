# Module — Integrations (Marketplace)

## IN.1 General Information

- **Marketplace URL**: https://marketplace.zoho.com/
- **Catalog scope**: Zoho app extensions covering Zoho CRM, Books, Invoice, Recruit, etc.
- **Verification**: "Zoho Marketplace offers over 2,500 apps…" (https://timelines.ai/10-essential-zoho-crm-marketplace-apps-for-team-productivity — third-party count, treat as approximate; the marketplace page itself only confirms catalog existence).
- **Categories**: Sales, Marketing, Productivity, Communication, Finance, Customer Support, Analytics, Document Management, Travel, Telephony, Social.

## IN.2 Native Zoho Family Integrations

| Integration | URL pattern | Capability |
|---|---|---|
| Zoho Mail | https://www.zoho.com/mail/ | Two-way email sync, Templates |
| Zoho Desk | https://www.zoho.com/desk/ | Tickets ↔ Cases |
| Zoho Books | https://www.zoho.com/books/ | Invoices/Payments sync |
| Zoho Campaigns | https://www.zoho.com/campaigns/ | Email marketing ↔ Leads/Contacts |
| Zoho Survey | https://www.zoho.com/survey/ | Survey responses → Contacts |
| Zoho SalesIQ | https://www.zoho.com/salesiq/ | Live chat → Leads |
| Zoho PhoneBridge | Multiple PBX | Call logs → Calls module (Signals) |
| Zoho Meeting | https://www.zoho.com/meeting/ | Online meetings |
| Zoho Backstage | https://www.zoho.com/backstage/ | Event ticketing → Leads/Contacts (Signals) |
| Zoho Webinar | https://www.zoho.com/webinar/ | Registration → Leads (Signals) |
| Zoho Cliq | Chat | Notifications routing |
| Google Workspace | — | Calendar sync |
| Microsoft 365 | — | Calendar sync, email sync |
| Slack | — | Notifications |
| Cisco Webex | — | Notifications |

## IN.3 Installation lifecycle

1. Admin → Marketplace → search app.
2. Click Install → accept permissions.
3. Authenticate via OAuth where required.
4. App appears in left-sidebar (custom module) or Settings → Extensions.

## IN.4 Build-Your-Own via Extensions

- Custom JS extensions can be deployed via Setup → Extensions (https://www.zoho.com/crm/developer/docs/api/v8/).
- Server-side extensions via Custom Functions (Deluge).
- Webhook + REST call patterns.
