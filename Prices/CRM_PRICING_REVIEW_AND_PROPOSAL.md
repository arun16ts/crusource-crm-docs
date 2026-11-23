# Crusource CRM pricing proposal and research review

**23 November 2026 · Internal discussion draft · Commercial terms pending cost validation**

Use this brief and the [revised calculator](Crusource_CRM_Pricing_Review_Model.xlsx) for the manager discussion. Advaith's [research notes](CRM_PRICING_AI_CREDITS_AND_COMPETITIVE_ANALYSIS.md) and [original workbook](Crusource_CRM_Pricing_And_Cost_Analysis.xlsx) are the starting point for this review.

## Proposed offer

| Offer | Price to test | What the customer gets |
| --- | --- | --- |
| **Free · 14-day trial** | ₹0 / $0 | Try the core Pro workflows with a small AI allowance. After 14 days, lock normal workspace access and give the owner an upgrade or contact-sales screen. Confirm the trial limits and post-expiry data retention policy before launch. |
| **Pro** | **₹1,199 India / $19 US** per paid seat per month, billed annually. **₹1,499 / $24** month to month. | Self-service CRM with core sales workflows, reporting, team collaboration, permission controls and a shared AI allowance. Confirm storage, outreach and support limits before publishing. |
| **Custom** | **Contact sales** | Quote Pro capabilities plus agreed volumes, onboarding, migration, integrations or support. Scope and price one-time services separately from recurring seats, capacity and support. Include specific deliverables and limits in each quote. |

Recommend launching at these four Pro price points once the paid workflow and limits are verified. Annual invoices would be **₹14,388 / $228 per seat** before taxes. India and US prices are regional list-price proposals. Reserve approval, migration and other detailed claims for workflows verified end to end.

### How to present the pricing

| Card | Lead with | Action |
| --- | --- | --- |
| **Free trial** | **₹0 for 14 days.** Try your pipeline, share it with your team and use 200 trial AI credits. Show the expiry date and explain when access locks. | Start 14-day trial |
| **Pro** | **₹1,199 per seat/month, billed ₹14,388 per seat/year.** Save 20% compared with ₹1,499 billed monthly. Feature bullets: manage your pipeline and follow-ups, share work with permissions, report on sales performance, and use a shared AI allowance. | Start 14-day trial |
| **Custom** | **Contact sales.** Get a quote for migration, support and higher volumes based on the scope agreed with your team. | Talk to sales |

Give Pro the strongest visual emphasis and use the same primary trial action on both eligible cards. In the US, show **$19 per seat/month, billed $228 per seat/year**, and **Save 21%** compared with $24 billed monthly. Put the annual invoice total beside the monthly equivalent and keep the monthly option visible. Use real monthly prices as the reference point. The price endings are a presentation choice. The business case rests on regional price comparisons, a trial that shows real value, and measured contribution.

Keep AI recharge below the cards as a single optional pack. Show the organization allowance and the action costs in the product. Describe any storage, sending and credit limits in plain language before checkout.

Source shows a 14-day entitlement decision and a billing page that renders a beta notice. Verify whether expiry gates reads, writes and background work as intended before promising a workspace lock. Test the owner upgrade path and restoration of access after payment. [Backend entitlement](../../crusource-crm-backend/src/modules/billing/services/subscription_access.py) · [Current billing page](../../crusource-crm-frontend/src/app/dashboard/billing/page.tsx)

## Competitor benchmark

Public list prices reviewed on 23 November 2026. Totals assume 15 equivalent paid seats and exclude tax and add-ons. US figures are USD list prices, and HubSpot totals assume all paid users need the stated seat type. Get a local quote before making India claims for a US-priced competitor.

| Benchmark | Unit price per month | 15 seats per month | Basis |
| --- | ---: | ---: | --- |
| **Crusource Pro India** | **₹1,199** | **₹17,985** | Proposed, annual billing |
| Zoho CRM Standard | ₹800 | ₹12,000 | India, annual |
| Zoho CRM Professional | ₹1,400 | ₹21,000 | India, annual |
| Zoho CRM Enterprise | ₹2,400 | ₹36,000 | India, annual |
| **Crusource Pro US** | **$19** | **$285** | Proposed, annual billing |
| Pipedrive Lite / Growth | $14 / $39 | $210 / $585 | US list, annual |
| Salesforce Starter / Pro Suite | $25 / $100 | $375 / $1,500 | Starter monthly or annual, Pro annual |
| HubSpot Sales Hub Starter | From $20 | From $300 | Monthly list per Core Seat |
| HubSpot Sales Hub Professional | From $100 | From $1,500 | Monthly list per Sales Seat, $1,500 required onboarding |
| HubSpot Sales Hub Enterprise | From $150 | From $2,250 | Annual billing per Sales Seat, $3,500 required onboarding |

At the proposed annual rate, Crusource costs **14.4% less than Zoho Professional** and **24% less than Salesforce Starter** at equal seat counts. Zoho Standard and Pipedrive Lite are cheaper. Zoho also offers an ongoing free edition for up to three users, while Pipedrive advertises a 14-day trial. These are comparisons of list prices. Feature coverage, implementation and buying terms vary. [Zoho edition comparison](https://www.zoho.com/crm/complete-feature-list.html?src=customer-management-software) · [Pipedrive pricing](https://www.pipedrive.com/en/pricing) · [Salesforce pricing](https://www.salesforce.com/sales/pricing/) · [HubSpot Sales Hub catalog](https://legal.hubspot.com/hubspot-product-and-services-catalog/products#sales-hub)

Zoho lists Standard with roles and Teamspaces, Professional with field-level security, and Enterprise with reporting hierarchy and approval processes. This replaces the draft's blanket Enterprise claim. Compare specific behaviors in demos, particularly shared record access, approval paths and reporting. The maintained CRM inventory reports some scope limitations for Team Space and Forecast. Pipedrive Lite already advertises AI report creation, so AI reporting alone is a weak differentiation claim. [Zoho edition comparison](https://www.zoho.com/crm/complete-feature-list.html?src=customer-management-software) · [CRM feature inventory](../product/CRUSOURCE_CRM_MODULES_AND_FEATURES.md) · [Pipedrive pricing](https://www.pipedrive.com/en/pricing)

## AI recharge proposal

- Start the pilot with **200 one-time trial credits** and **500 + 400 per paid seat per month** pooled for Pro. At 15 seats, that is 6,500 credits. Use contracted allowances for Custom.
- Launch one manual recharge pack as a hypothesis: **2,500 credits for ₹799 / $10**. Spend monthly credits first and show the organization balance and action costs. Confirm recharge expiry and refund terms before selling packs. Keep core CRM available when AI credits run out.
- Publish predictable credit costs for supported actions after observing actual usage. Keep Advaith's **$0.001 per credit as an internal cost target** for the spreadsheet. At that target, a fully used Pro grant at 15 seats models $6.50 of provider spend, or ₹552.50 at the draft's ₹85/USD assumption. A fully used recharge models $2.50 of provider spend. These figures depend on metering and actual model costs.
- Before selling credits, measure prompt, output including thinking, embedding, retry and batch costs for each supported workflow. Reserve or otherwise cap spend before provider calls, reconcile usage without double charging, and validate trial abuse controls. Track public website AI separately. The lead scoring ledger is a starting point for the audit. [Lead scoring ledger](../../crusource-crm-backend/src/modules/leads/repositories/lead_scoring_models.py)

Google lists Gemini 2.5 Flash standard text input at $0.30 per million tokens and output at $2.50 per million, including thinking. Published rates establish the price per token. The original workbook's per-action volumes need usage measurements. Confirm the production model IDs and applicable rate cards with engineering. [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)

## What changed after the audit

| Finding | Revision |
| --- | --- |
| Both originals describe two offers and omit Custom. | Added a quote-based Custom offer. AI recharge is an add-on. |
| HubSpot India prices and package assumptions lack a verified quote. | Replaced them with HubSpot’s official USD Sales Hub seat rates and onboarding. Vendor credits use different units. |
| Workbook cell `1. Feature Comparison!B41` counts competitor advantages as Crusource wins and can count a row twice. Several feature rows claim broad parity. | Removed the win score and retained only specific comparisons supported by vendor or CRM evidence. |
| `4. Profit & Break-Even!C19` uses six India seats while the Markdown says eight. India AI costs also reference USD scenario values that include USD recharge revenue. | Model the two currencies independently, with recharge purchases and credits consumed as separate inputs. |
| `2. Monthly App Costs!E24` omits query embedding and thinking costs from chat. The draft's credit estimate sets column mapping to one credit in Excel despite its sample costing about $0.001045 before any other work. | Treat raw AI estimates and credit charges as provisional. Measure billed usage before setting action prices. |
| The $94.93 production estimate sums as written. Scaling thresholds, 86–92% margins and six/eight seat break-even depend on unverified costs and usage. | Preserve $94.93 as the original estimate. Update the illustration with the new AWS report and leave actual all-in costs blank. |

## AWS baseline and remaining inputs

The 23 November AWS report estimates **$55.88/month production** and **$52.17/month staging** before GST with shared load balancer allocation. It assumes 730 runtime hours and uses an even split across services sharing each load balancer. Its reported after-tax amounts are $65.94 and $61.56, respectively. These are reported run-rate estimates. Confirm the allocation, metered charges and invoice totals before treating them as actuals. [AWS monthly cost report](Crusource_CRM_AWS_Monthly_Cost_Report.docx)

DevOps confirmed that **$20/month covers Vercel for the entire company**. Use **$5/month** as a planning allocation to CRM (25%). Use $10 for a higher allocation scenario until there is project usage evidence. Unlimited projects coexist with usage limits and additional usage charges. [Vercel Pro billing](https://vercel.com/docs/plans/pro-plan/billing)

For the target SQS architecture, remove the $7 Redis Cloud placeholder and budget **$2/month provisionally** for queue requests. AWS lists a monthly free allowance of one million SQS requests. Polls, sends, deletes and payload size affect the bill. Verify the cost of any additional worker capacity and how existing cache, locks and rate limits will be covered before relying on this assumption. [Amazon SQS pricing](https://aws.amazon.com/sqs/pricing/)

Budget Actions runtime from the billing dashboard. As a planning example, **3,000 additional CRM-attributed standard Linux minutes cost $18** at $0.006/minute. The reported 3,000-minute allowance and this 3,000-minute overage example are separate figures. Verify the included compute and billed overage on the account. Keep Enterprise as a future scenario at **$21 per licensed user per month**. Compare the incremental license bill and remaining runtime charges against actual overages. The workbook lets you reduce the future Actions charge when the Enterprise allowance covers it. [GitHub runner rates](https://docs.github.com/en/billing/reference/actions-runner-pricing) · [Included compute](https://docs.github.com/en/billing/reference/product-usage-included) · [GitHub plans](https://github.com/pricing)

The resulting **$80.88/month planning subtotal** combines $55.88 production AWS, $5 Vercel, a $2 SQS reserve and $18 for the Actions example. Actions is engineering overhead included here for sensitivity. The subtotal excludes staging and still needs email, support, worker, payment, and usage reconciliation. Keep actual inputs blank until measured.

### Why these prices leave room for contribution

A 15-seat India Pro customer pays **₹17,985/month equivalent** annually, versus **₹21,000** on Zoho Professional at its annual list price. Under the calculator's illustrative ₹85/USD, 2.9% payment fee and full use of 6,500 included credits at $0.001 per credit, assigning the entire $80.88 subtotal to that one customer leaves **about ₹10,036/month** before direct support, trial, and other unconfirmed costs. Assigning the same subtotal to one five-seat customer gives a loss of about **₹1,266/month** under the same assumptions. Shared costs need a paying customer base, and these examples are planning scenarios. [Zoho edition pricing](https://www.zoho.com/crm/complete-feature-list.html)

Use conversion from trial to paid, realized contribution per paying organization, and credit spend to validate the launch price. Quote Custom with explicit seat, support and volume commitments. Price delivery separately and check the quote against Finance's contribution target.

Use the calculator to rerun the base case and higher cost cases when bills arrive. It shows modeled contribution after the entered costs, with separate trial/support inputs, and leaves the actual-cost result blank until the required figures are entered. Validate seat willingness to pay with sales conversations using the proposed prices before approving public terms.
