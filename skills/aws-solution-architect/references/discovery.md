# Discovery - requirements that actually change the design

Ask the *minimum* set that changes the architecture. Everything else becomes a written assumption the customer can correct. Max 5 questions per round; offer sensible defaults in the question so a one-word answer is enough.

## Contents
1. The six questions that matter most
2. Full checklist (use for workshops / documents)
3. Turning answers into design drivers
4. Assumption block template

## 1. The six questions that matter most
| # | Question | Why it changes the design |
|---|---|---|
| 1 | What does the workload do and who uses it (users, peak/avg traffic, growth)? | Compute model, scaling, edge/CDN, data store |
| 2 | Availability target and **RTO/RPO** (what is an hour of downtime / lost data worth)? | Multi-AZ vs multi-Region, DR strategy ([reliability-dr.md](reliability-dr.md)) |
| 3 | Compliance and data residency (PCI DSS, DORA, GDPR, HIPAA, sector rules, Region constraints)? | Region choice, account structure, encryption, evidence ([security-compliance.md](security-compliance.md)) |
| 4 | Greenfield or existing system (what, where, how big, dependencies, licences)? | Migration strategy ([migration.md](migration.md)), connectivity, data transfer |
| 5 | Team skills and operating model (Kubernetes? serverless? 24x7 ops?) | Managed vs self-managed, ECS vs EKS, IaC tool |
| 6 | Budget shape (CAPEX/OPEX, steady vs spiky, hard ceiling)? | Pricing models, serverless vs provisioned ([cost-optimization.md](cost-optimization.md)) |

## 2. Full checklist (when time allows)
- **Business**: goals, deadline, success metrics, cost of downtime, regulatory exposure, stakeholders.
- **Workload**: components, protocols, statefulness, session handling, batch vs interactive, data volume and growth, data classification, retention, latency targets by user geography.
- **Integration**: upstream/downstream systems, on-prem links (bandwidth, latency), identity provider (SSO/SAML/OIDC), third-party SaaS/APIs.
- **Data**: engine and version, size, change rate, consistency needs, analytical needs, backup/retention, residency.
- **Security**: threat model, data classes, key ownership (customer-managed keys?), network isolation, audit/logging obligations, pen-test/attestation requirements.
- **Operations**: monitoring tooling, on-call, change process, release frequency, environments, existing IaC/CI.
- **Constraints**: approved technologies, existing enterprise agreements, mandated Regions, vendor lock-in concerns, existing AWS accounts/landing zone.

## 3. From answers to design drivers
Write 4-8 drivers in testable form, then reference them in every decision.
Example: "D1 RTO <= 15 min / RPO <= 1 min -> warm standby or active/active, not backup/restore. D2 PCI DSS in scope -> isolate cardholder data environment in its own account/VPC. D3 EU residency -> EU Regions only; replication stays in EU. D4 team knows containers, not Kubernetes -> ECS on Fargate."

## 4. Assumption block (put at the top of the answer when information is missing)
```
Assumptions (tell me which are wrong):
- A1 Traffic: ~50 req/s average, 5x spikes  [Assumption]
- A2 Availability 99.9%, RTO 1 h, RPO 15 min  [Assumption]
- A3 Single Region (eu-west-1), 2+ AZs  [Assumption]
```
