# Crusource CRM application cost breakdown

23 November 2026 · USD unless stated otherwise · Production, staging and CRM-attributable application services

## AWS monthly run-rate from DevOps

The report models 730 runtime hours and allocates one third of the shared staging ALB and one half of the shared production ALB to CRM. Figures are run-rate estimates. The source rounds the line items and reports separate subtotals. [DevOps AWS cost report](Crusource_CRM_AWS_Monthly_Cost_Report.docx)

| Charge | Production / month | Staging / month |
| --- | ---: | ---: |
| ECS Fargate CPU | $15.53 | $15.53 |
| ECS Fargate RAM | $3.40 | $3.40 |
| Public IPv4 | $3.65 | $3.65 |
| RDS PostgreSQL compute | $18.98 | $18.98 |
| RDS storage | $2.62 | $2.62 |
| RDS automated backup storage | $0.00 reported | $0.00 reported |
| Secrets Manager | $0.40 | $0.40 |
| CRM allocation of shared load balancer | $11.13 | $7.42 |
| ECR image storage | $0.16 | $0.16 |
| S3 file storage | < $0.01 | < $0.01 |
| CloudWatch logs | $0.00 reported | $0.00 reported |
| **Reported subtotal** | **$55.88** | **$52.17** |
| Reported AWS GST | $10.06 | $9.39 |
| **Reported total including AWS GST** | **$65.94** | **$61.56** |

**Combined AWS: $108.05/month before GST, or $127.50/month including the reported GST.** DevOps reports no NAT gateway or Route 53 charge for these environments. The report lists the full ALB allocation as an alternative, so it stays out of the shared total.

## Other CRM application costs in the pricing model

| Charge | Monthly planning amount | Evidence or remaining detail |
| --- | ---: | --- |
| Vercel frontend | **$5.00** | The company bill is $20/month. The calculator assigns 25% to CRM provisionally. Check project usage and any billed overage. Count the shared bill once across CRM environments. |
| AWS SQS requests | **$2.00** | Planning reserve. Confirm actual requests and worker runtime separately. |
| GitHub Actions runtime | **$18.00** | Scenario for 3,000 additional CRM-attributed standard Linux minutes at $0.006/min. Check billed minutes, other runner types, storage, and any existing company plan allocation. |
| Redis Cloud | **$0.00 in the target budget** | Planned SQS setup. Any historical or transition charges need invoice evidence. |
| GitHub Enterprise | **$0.00 in the current budget** | Future option. |

**Modeled production, staging and shared-service subtotal: $133.05/month before tax.** This adds $25 of planning allocations and reserves to $108.05 of reported AWS. With only the report's AWS GST added, it becomes $152.50. Neither total includes the unpriced usage below. [Pricing workbook](Crusource_CRM_Pricing_Review_Model.xlsx)

## Charges to reconcile before calling the total complete

| Cost line | Needed to price it |
| --- | --- |
| AWS SES outbound and inbound email, and associated SNS notifications | CRM-tagged billed messages, attachments/data, and notifications. The original $2 email assumption was based on 20,000 sends and is not a bill. |
| SQS worker compute and extra AWS jobs | Task or instance runtime for workers, migrations, background jobs, scheduled jobs and scaled replicas. Match runtime to ECS charges already included. |
| AWS usage above the baseline | Metered egress and cross-AZ traffic, ALB capacity, S3 requests and downloads, retained snapshots and backup overage, RDS burst credits, CloudWatch metrics and log charges, ECR pulls, any extra IPv4, secrets or key charges. Compare with the AWS report to avoid double counting. |
| Gemini AI and embeddings | Billed input, output, reasoning and embedding usage across CRM, including public chat, trial traffic, retries and staging. Split shared provider bills by CRM project or usage. |
| Domain and external DNS | CRM's share of renewal and any paid DNS or certificates. DevOps reports no AWS Route 53 charge. |
| Direct CRM tools and external integrations | CRM-attributable usage or licenses for Google Workspace/Drive, paid monitoring, test services and other integrations where the company pays. Identify customer-owned subscriptions before allocating costs. |
| Payment processing, if charging customers | Gateway fees, refunds or dispute fees actually billed. The workbook uses 2.9% only as a scenario. |
| Historical or one-time application charges | CRM-related cloud, build, testing, migration and setup invoices from the start of the project, including retired services and any refunds or credits. |

An invoice-based total requires the relevant AWS billing export, CRM usage or allocations for Vercel and GitHub, Gemini provider billing, and any direct CRM vendor invoices for the period being totaled. Use a single reporting currency and document tax treatment and credits. Keep unknown amounts blank until reconciled.
