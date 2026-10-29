# Deliverable templates

Choose the smallest artifact that serves the audience. Save long documents to a file; in chat give the TL;DR and the path. Every document: date, author/owner, status, assumptions, sources (links), open questions.

## Contents
1. Solution Design Document (SDD)
2. Architecture Decision Record (ADR)
3. Well-Architected review report
4. Migration plan
5. DR plan
6. Cost model
7. Customer workshop agenda
8. Quick answer format

## 1. Solution Design Document
```
# <Solution> - Design (v, date, owner, status)
1. TL;DR (decision, why, main risk, cost shape)
2. Context and goals (business drivers, success metrics)
3. Requirements and constraints (functional, NFR: availability, RTO/RPO, performance, security, compliance, budget) - table D1..Dn
4. Assumptions and out-of-scope
5. Options considered (2-3) with comparison table and recommendation
6. Target architecture (diagram(s) + component table: component | AWS service | why | alternatives)
7. Network and connectivity
8. Security and compliance (shared-responsibility split, IAM, keys, logging, evidence)
9. Resilience and DR (strategy, RTO/RPO achieved, failure modes table)
10. Operations (CI/CD, observability, runbooks, backup)
11. Cost drivers and estimate method (Pricing Calculator inputs)
12. Well-Architected summary (6 pillars: strengths / risks / actions)
13. Delivery plan (phases, dependencies, team)
14. Risks and open questions
15. References (official AWS links)
```
## 2. ADR
```
# ADR-<n>: <decision>
Status: proposed | accepted | superseded by ADR-x     Date:
Context: forces, requirements (D#), constraints
Options: A / B / C with pros-cons (cost, ops burden, risk, skills)
Decision: chosen option + rationale
Consequences: positive, negative, follow-ups, revisit trigger (what would change the decision)
Sources: AWS docs links
```
## 3. Well-Architected review
Use the report format in `well-architected.md` section 5.

## 4. Migration plan
```
Scope and inventory summary - strategy per application (7 R + rationale) - target landing zone - network/connectivity plan - security baseline - wave plan (table: wave, apps, strategy, tooling, cutover window, owner, rollback) - data transfer plan (volume, link, time estimate) - testing and cutover runbook outline - cost: baseline vs target, post-migration rightsizing - risks - governance (RACI) - success metrics
```
## 5. DR plan
```
Tier and targets (RTO/RPO, business impact) - strategy chosen and why - architecture (primary/DR diagram) - data replication per store - traffic failover mechanism - IaC/secrets/keys/quotas in DR Region - failover and failback runbook (steps, owner, decision authority, comms) - test schedule and last result - open gaps
```
## 6. Cost model
`Driver | Unit | Quantity (assumption) | Pricing model | Source | Notes` per environment, plus scenarios (baseline / peak / growth) and optimisation levers. Prices only if verified live; otherwise the Pricing Calculator inputs.

## 7. Customer workshop agenda (2-3 h)
Goals and success (15) - current state walk-through (30) - requirements and constraints, RTO/RPO, compliance (30) - option discussion (30) - risks and unknowns (15) - next steps, owners, dates (15). Output: assumption list + decisions + action items.

## 8. Quick answer format (chat, no document)
```
TL;DR  (3-5 lines)
Assumptions (if any)
Recommended design  (diagram + component table)
Why / trade-offs vs alternative
Risks and mitigations (Well-Architected, top few)
Cost drivers + how to estimate
Next steps
Sources
```
