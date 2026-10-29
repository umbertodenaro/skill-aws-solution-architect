# Reliability and disaster recovery

Whitepaper: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html
DR options page: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html

## Contents
1. Define the targets first
2. The four DR strategies
3. Choosing a strategy
4. Within-Region resilience (AZ)
5. Design rules
6. Testing and tooling

## 1. Define targets first
**RTO** (how long until service is back) and **RPO** (how much data loss is tolerable). Ask the business for the cost of downtime per hour; targets without cost justification get over-engineered. Set them per workload tier, not per company.

## 2. The four strategies (active/passive to active/active)
The AWS DR whitepaper describes: backup and restore, pilot light, warm standby, and multi-site active/active. Per the whitepaper, the difference between pilot light and warm standby: both keep an environment in the DR Region with copies of primary assets, but pilot light cannot process requests without additional action first (you turn on servers, deploy non-core infrastructure, scale up), whereas warm standby is a scaled-down but fully functional copy that can handle traffic at reduced capacity immediately - recovery only requires scaling up, and it is easier to test continuously. Use RTO/RPO to choose.
| Strategy | Idea | Typical recovery speed | Relative cost |
|---|---|---|---|
| Backup & restore | Backups copied to another Region; rebuild with IaC on disaster | slowest | lowest |
| Pilot light | Data replicated, core infra minimal/off | faster | low |
| Warm standby | Scaled-down full stack always running | fast | medium |
| Active/active | Multiple Regions serve traffic | fastest (near zero) | highest, plus data-consistency design |
(Ordering is qualitative; do not quote minutes for a strategy - they depend on the workload; check the whitepaper for its stated ranges.)

## 3. Choosing
| If | Then |
|---|---|
| RTO/RPO of hours, tolerable data loss, non-critical | Backup & restore |
| RTO tens of minutes, RPO minutes | Pilot light or warm standby |
| RTO minutes, RPO seconds-minutes, critical | Warm standby |
| Near-zero RTO/RPO, revenue-critical | Active/active (needs conflict resolution/data partitioning design) |
A DR design must also cover: data replication mechanism per data store, DNS/traffic failover, secrets/keys in the DR Region, IAM and IaC parity, quotas in the DR Region, runbook and who decides to fail over.

## 4. Within-Region resilience
Spread each tier across at least two Availability Zones; use managed Multi-AZ options for data stores; use load balancers with health checks and Auto Scaling for replacement; keep state out of instances. AZ failure is the common case to design for before Region failure. Understand fault isolation boundaries (AZ, Region, partition) and control-plane vs data-plane dependencies, and design for **static stability** - recovery should not depend on control-plane operations during the event: https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/abstract-and-introduction.html

## 5. Design rules
- Backups are not DR until restore is tested; protect them from the same blast radius (cross-account/cross-Region, immutability options - verify service-specific features).
- Prefer data-plane failover mechanisms over control-plane actions during an incident.
- Make failover and failback explicit steps in the runbook; test failback.
- Account for quotas and capacity in the DR Region (request increases in advance; consider capacity reservation options - see EC2 purchasing guide in `cost-optimization.md`).
- Regulated workloads: check whether data residency allows replication to the DR Region.

## 6. Testing and tooling
AWS Resilience Hub lets you define a resiliency policy with RTO/RPO targets (application, infrastructure, AZ, optional Region) and assess an application against it: https://docs.aws.amazon.com/resilience-hub/latest/userguide/setup-resiliency-policy.html . Schedule game days; test AZ-failure behaviour and restore from backup regularly. Verify live which services have built-in cross-Region replication features before relying on them.
