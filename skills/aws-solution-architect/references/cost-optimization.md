# Cost optimization and FinOps

Prices and discount percentages change - **never quote them from memory**. Quote only what you verified live, with the link, or give the estimation method.

## Contents
1. Estimation method
2. Cost drivers by service type
3. Purchasing models
4. Controls and visibility
5. Optimization levers
6. Answer format

## 1. Estimation method
Use the AWS Pricing Calculator: workload estimates are free, can model scenarios (e.g. x86 vs Graviton at identical rates), and should be created per environment (dev/stage/prod) and Region; choose rate type "Before discounts" for a clean baseline then add commitments: https://docs.aws.amazon.com/pricing-calculator/latest/userguide/generate-estimate.html and https://aws.amazon.com/blogs/aws-cloud-financial-management/estimate-and-compare-aws-costs-with-the-aws-pricing-calculator-part-1-creating-and-comparing-workload-estimates/ . Provide the customer the *inputs* (instance counts/types, GB stored, requests, GB transferred per path) so they can reproduce the number.

## 2. Cost drivers (what to list in every design)
Compute (hours/vCPU-GB, requests x duration) - storage (GB-month, tier, requests) - databases (instance or capacity units, storage, I/O, backups, replicas) - data transfer (internet egress, cross-AZ, cross-Region, NAT processing, endpoints) - managed-service fees (per-hour, per-GB processed) - observability (logs ingested/stored, metrics, traces) - support plan. Call out the likely top 2 line items and the non-obvious ones (NAT Gateway data processing, cross-AZ traffic, log volume).

## 3. Purchasing models
EC2 purchasing decision guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/ec2-purchasing-options-aws-how-to-choose.html - guidance there: right-size first (Compute Optimizer), then commit. A common hybrid: commitment-based options (Savings Plans) for baseline, On-Demand or Spot for variable load, On-Demand Capacity Reservations for mission-critical capacity assurance. Spot suits interruption-tolerant work. Savings Plans: commitment in $/hour for 1 or 3 years with All/Partial/No upfront payment; Compute Savings Plans apply across EC2 regardless of family/size/OS/tenancy/Region and also to Fargate and Lambda; recommendations come from Cost Explorer (note the doc states usage-based recommendations and that unused hourly commitment is not rolled over): https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html . Read live pages for current discount ranges and eligible services.

## 4. Controls and visibility
Tag strategy and cost allocation tags - AWS Budgets (alerts on actual/forecast), Cost Explorer (analysis, recommendations), Cost Anomaly Detection (ML-based spend anomalies), Cost and Usage Report for detail: https://aws.amazon.com/blogs/aws-cloud-financial-management/cost-control-blog-series-3-how-to-handle-cost-shock/ . Per-account budgets via the multi-account design. Make someone accountable (FinOps owner) - the Cost Optimization pillar's first focus area is Cloud Financial Management: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html

## 5. Optimization levers (ranked by effort/impact - validate per case)
1. Delete idle/unattached resources; schedule non-prod off-hours.
2. Right-size using utilisation data (Compute Optimizer).
3. Choose the right pricing model (commitments after usage is stable).
4. Storage lifecycle and tiering; compress/delete logs by policy.
5. Remove data-transfer waste (endpoints vs NAT, keep chatty tiers in one AZ only if resilience allows - state the trade-off).
6. Move to managed/serverless where utilisation is low.
7. Evaluate newer-generation/Arm-based instances after testing the workload.

## 6. Answer format
`Driver | Unit | Estimate input | Source` table + "how to estimate" link + range with assumptions. If no verified price: write `[verify price]`, never a made-up figure.
