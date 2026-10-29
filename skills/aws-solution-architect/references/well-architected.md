# Well-Architected review

The AWS Well-Architected Framework has six pillars. Pillar summary (official): https://docs.aws.amazon.com/wellarchitected/latest/migration-lens/well-architected-framework-pillars.html
Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html

## Contents
1. Pillars and where to read the detail
2. Review procedure
3. Question bank per pillar (design-review prompts)
4. Lenses
5. Report format

## 1. Pillars
| Pillar | Focus areas per AWS | Whitepaper |
|---|---|---|
| Operational excellence | organization, prepare, operate, evolve | https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html |
| Security | foundations, IAM, detection, infrastructure protection, data protection, incident response, application security | https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html |
| Reliability | foundations, workload architecture, change management, failure management | https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html |
| Performance efficiency | architecture selection, compute/hardware, data management, networking/content delivery, process and culture | https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html |
| Cost optimization | cloud financial management, expenditure and usage awareness, cost-effective resources, demand/supply management, optimization | https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html |
| Sustainability | Region selection, alignment to demand, software/architecture, data, hardware/services, process and culture | https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html |

## 2. Review procedure
1. Establish scope: workload boundary, environment (prod?), business criticality, constraints.
2. Walk the six pillars with the prompts below against the *actual* design (diagram + notes). Do not review what is not shown - list it as "unknown".
3. Rate each finding: **High** (likely outage/breach/compliance gap) - **Medium** - **Low**. Rate by impact x likelihood for *this* workload, not generically.
4. Every finding = observation -> risk -> recommended fix -> doc link -> effort (S/M/L).
5. Prioritise a short improvement plan (quick wins first, then structural).
For a formal, tracked review the customer can use the AWS Well-Architected Tool (console), which produces an improvement plan from answers; mention it, do not claim to replace it.

## 3. Prompts per pillar
**Operational excellence**: Are deployments automated and repeatable (IaC, pipeline)? Can you deploy and roll back safely? Are metrics, logs, traces and alarms defined against SLOs? Runbooks and game days? How are operational events learned from?
**Security**: Multi-account isolation? Human access via federation/SSO and MFA; workloads via roles (no long-term keys)? Least privilege and guardrails (SCPs)? Data classified and encrypted in transit/at rest with managed keys? Threat detection and centralised logging on? Incident response playbooks? Vulnerability management in pipeline?
**Reliability**: Every tier Multi-AZ? Single points of failure? Quotas known and monitored? Retries with backoff/timeouts/circuit breakers? Health checks and automatic recovery? Backups tested by restore? DR strategy matches RTO/RPO? Static stability (no control-plane dependency during recovery) - see https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/abstract-and-introduction.html
**Performance efficiency**: Right compute model and instance/runtime family? Data store matches access pattern? Caching and CDN where useful? Load tested? Performance monitored and reviewed as services evolve?
**Cost optimization**: Tagging and cost allocation? Budgets/anomaly alerts? Right-sized? Commitment discounts for steady baseline, Spot for fault-tolerant? Storage lifecycle? Data-transfer paths reviewed (NAT, cross-AZ, cross-Region, egress)? Idle resources removed?
**Sustainability**: Region chosen with latency/cost/carbon considered? Scale to demand? Efficient instance families (verify current options)? Data retention and lifecycle? Managed/serverless where it raises utilisation?

## 4. Lenses (apply when the workload matches)
- Financial Services Industry Lens - resiliency, security, data privacy, auditability for regulated FS: https://docs.aws.amazon.com/wellarchitected/latest/financial-services-industry-lens/financial-services-industry-lens.html
- Serverless Applications Lens: https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html
- Generative AI Lens (model selection, prompt engineering, customization, responsible AI): https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html
- SaaS Lens (multi-tenant; tenant isolation): https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html
- Migration Lens: https://docs.aws.amazon.com/wellarchitected/latest/migration-lens/well-architected-framework-pillars.html
Other lenses exist (data analytics, machine learning, container build, etc.) - search the Well-Architected lens catalogue live rather than guessing a URL.

## 5. Report format
```
# Well-Architected review - <workload>   (date, scope, assumptions)
## TL;DR  (overall risk, top 3 actions)
## Findings by pillar   | # | Pillar | Finding | Risk | Fix | Effort | Source |
## Improvement plan     Now (<2 wks) / Next (<3 months) / Later
## Unknowns to confirm
```
