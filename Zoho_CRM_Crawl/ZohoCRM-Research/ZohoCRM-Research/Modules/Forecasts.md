# Module — Forecasts

> Source: https://help.zoho.com/portal/en/kb/crm/sales-force-automation/forecasts/articles/creating-and-working-with-forecasts

## FC.1 General Information

- **API name**: `Forecasts`
- **OAuth scope**: `ZohoCRM.modules.deals` (forecasts are derived from Deals) — admin-side access via Forecast Settings.
- **Purpose**: Set quota / revenue target for each user or role; compare achieved vs target visually.
- **Edition**: Sales Forecasting is a Standard-eedition feature; AI Forecasting requires Enterprise+ (https://www.zoho.com/crm/ai-features-in-zoho-crm.html).

## FC.2 Forecast Calculation Logic

Quoted verbatim from the official help page:

> "Only one role can be assigned to a user, so a user can only have one target, as per the forecast."

Forecast rollup formula:

- Pipeline = ∑(Open Deals × Probability) for deals in Forecast Category = "Pipeline".
- Closed Won = ∑(Amount) for deals with Stage.Category = Closed Won.
- Achieved = Closed Won.

## FC.3 AI Forecasting (Enterprise+)

Verbatim from https://www.zoho.com/crm/ai-features-in-zoho-crm.html :

> "Zia suggests optimal targets for individual users and roles... Zia predicts how much an individual user or a team is likely to achieve in the current forecast period."

## FC.4 Cross References

- `../Modules/Deals.md`.
- `../06_Data_Model.md`.
