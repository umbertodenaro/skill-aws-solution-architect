# Migration to AWS

## Contents
1. The 7 Rs
2. Process: assess -> mobilize -> migrate and modernize
3. Tooling
4. Wave planning
5. Data transfer and cutover
6. Risks and success criteria

## 1. The 7 Rs
AWS defines seven strategies: **Retire, Retain, Rehost, Relocate, Repurchase, Replatform, Refactor/re-architect**. For large migrations the guidance names rehost, relocate, replatform and retire as the common ones; refactor is not recommended *during* a large migration because modernising while moving is the most complex path - rehost/relocate/replatform first, modernise afterwards. https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html
| Strategy | Meaning (short) | Pick when |
|---|---|---|
| Retire | decommission | no business value, duplicate |
| Retain | keep where it is for now | not ready, recent investment, compliance blocker |
| Rehost | lift-and-shift to EC2 | speed, minimal change, large estates |
| Relocate | move hypervisor-level (e.g. VMware workloads) without changing the stack | VMware estates; verify current service options |
| Repurchase | switch to SaaS/different licence | commodity apps |
| Replatform | small optimisations (e.g. managed DB) | quick win without code change |
| Refactor | re-architect cloud-native | strategic apps needing agility/scale |
Decide per application using a documented rationale (business value, technical fit, licence, dependencies, risk).

## 2. Process
Application portfolio assessment (stakeholders, automated discovery, progressive enrichment, prioritisation, wave plan, continuous reassessment): https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-application-portfolio-assessment-migration/introduction.html
AWS Migration Acceleration Program (MAP) methodology: Migration Readiness Assessment (based on the AWS Cloud Adoption Framework), Migration Readiness & Planning (landing zone, operating model, security/compliance, business case/TCO), then the Migration phase run as a "migration factory": https://docs.aws.amazon.com/whitepapers/latest/public-sector-cloud-transformation/phase-3---gaining-momentum-and-optimization.html . Programme funding/eligibility is an AWS commercial matter - refer to the account team, do not state terms.
Migration Lens for Well-Architected: https://docs.aws.amazon.com/wellarchitected/latest/migration-lens/well-architected-framework-pillars.html

## 3. Tooling
- **Rehost servers**: AWS Application Migration Service (MGN) - continuous block-level replication to a staging area, automated conversion, cutover. Current AWS pages present it as *AWS Transform MGN* (formerly AWS Application Migration Service), including an agentic path and a self-directed console path: https://aws.amazon.com/application-migration-service/ . Check the live page for current naming and features.
- **Databases**: AWS Database Migration Service (DMS) for homogeneous/heterogeneous migration with replication; schema conversion tooling for engine changes - verify the current tool name and supported engines live.
- **Files/data**: AWS DataSync, Storage Gateway, Transfer Family; offline transfer devices for very large data (verify current device options).
- **Discovery and planning**: AWS's current discovery/planning services change names - use the live "migration and modernization" product pages.

## 4. Wave planning
Group apps by dependency and risk; wave 0 = landing zone + connectivity + pilot apps; early waves = low-risk/low-dependency; later waves = complex, data-heavy, regulated. For each wave: owner, cutover window, rollback criteria, test plan, hypercare. Keep a dependency map so you do not split chatty systems across on-prem and AWS (latency, egress cost).

## 5. Data transfer and cutover
Size the data and the link: required transfer time = data / usable bandwidth - compute it, show it, and if too slow propose offline transfer or phased replication. Use continuous replication to shorten the final cutover window. Rehearse cutover at least once; define go/no-go and rollback.

## 6. Risks and success criteria
Risks: licence terms (BYOL, Windows/SQL/Oracle), hidden dependencies, cut-over downtime, security baseline missing before first workload, over-provisioned lift-and-shift costs, skills gap. Success: measurable (apps migrated per wave, downtime per cutover, cost vs baseline after rightsizing, incident count first 30 days). Post-migration: rightsize with Compute Optimizer, adopt commitments after usage stabilises (`cost-optimization.md`), then modernise.
