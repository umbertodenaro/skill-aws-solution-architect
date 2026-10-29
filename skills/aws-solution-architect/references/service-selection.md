# Service selection - choose by requirement, using AWS Decision Guides

AWS publishes Decision Guides that map requirements to services. Start there, then verify the specific service page for current limits/Regions. Guides are updated over time - check the "Last updated" date.
Index: https://docs.aws.amazon.com/decision-guides/

## Contents
1. Compute
2. Containers
3. Databases
4. Storage
5. Integration / messaging
6. Analytics
7. Heuristics for tie-breaks
8. Anti-patterns

## 1. Compute
Guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/choosing-aws-compute-service.html
The guide groups options as: Amazon EC2 (scalable general compute, plus Auto Scaling, Image Builder, Elastic Beanstalk, Lightsail), container services (ECS, EKS, Batch, ECR), serverless (AWS Fargate, AWS Lambda), on-premises/edge (Local Zones, Outposts, Wavelength), cost tools (Savings Plans, Compute Optimizer, Spot), and Elastic Load Balancing.
| Need | Lean toward | Why |
|---|---|---|
| Event-driven glue, spiky/unknown load, minimal ops | Lambda | no servers to manage; pay per use |
| Long-running containers, steady traffic, minimal cluster ops | ECS on Fargate | no instance management |
| Kubernetes portability / ecosystem required | EKS | managed Kubernetes control plane |
| Lift-and-shift, special OS/licensing, GPU/custom kernel | EC2 | full control |
| Batch/HPC job queues | AWS Batch | managed scheduling |
Purchasing options for EC2 (On-Demand, Spot, Savings Plans, Capacity Reservations): https://docs.aws.amazon.com/decision-guides/latest/decision-guides/ec2-purchasing-options-aws-how-to-choose.html

## 2. Containers
Guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/choosing-aws-container-service.html
Its decision factors: managed-service/operation overhead, workload characteristics, application portability, organization size and skills, ease of deployment. Capacity: EC2, Fargate, Outposts. Orchestration: ECS, EKS, Red Hat OpenShift Service on AWS. Vertical solutions: App Runner, Lambda, Lightsail, Batch. Rule of thumb: pick ECS unless the team already runs Kubernetes or needs its ecosystem/portability; pick Fargate unless you need daemon sets, GPUs, special networking or cost tuning at scale.

## 3. Databases
Guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/databases-on-aws-how-to-choose.html
Covered services include Aurora, Aurora DSQL, Aurora PostgreSQL Limitless, DocumentDB, DynamoDB, ElastiCache, Keyspaces, MemoryDB, Neptune, RDS, Timestream. Choose by **data model and access pattern first**:
| Access pattern | Candidate |
|---|---|
| Relational, transactions, joins | Aurora or RDS (engine fit, licence, features) |
| Key-value/document at any scale, single-digit ms | DynamoDB |
| Cache / sub-ms reads | ElastiCache (cache) or MemoryDB (durable in-memory) |
| Graph traversals | Neptune |
| Time series | Timestream |
| MongoDB-compatible | DocumentDB |
| Global multi-Region relational | verify current Aurora global/DSQL capabilities live |

## 4. Storage
Guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/choosing-aws-storage-service.html
Services: S3 (objects), EBS (block for EC2), EFS (shared POSIX files), FSx (managed file systems), File Cache, Backup, DataSync, Storage Gateway, Transfer Family. Choose by access protocol (object/block/file), performance, sharing model and lifecycle.

## 5. Integration and messaging
Guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/sns-or-sqs-or-eventbridge.html
SQS = queue/decoupling and buffering; SNS = pub/sub fan-out; EventBridge = event routing, SaaS and AWS-service events, rules/pipes/scheduler. Product comparison: https://aws.amazon.com/compare/eventbridge-and-sqs/ (EventBridge: event-driven architectures, SaaS integration, audit; SQS: microservice decoupling, work queues, batch, buffering).

## 6. Analytics
Guide: https://docs.aws.amazon.com/decision-guides/latest/decision-guides/analytics-on-aws-how-to-choose.html
Covers Athena, Clean Rooms, Data Firehose, DataZone, EMR, Glue, Kinesis Data Streams, Managed Service for Apache Flink, MSK, MWAA, OpenSearch Service, Redshift, S3, SageMaker. See also `data-genai.md`.

## 7. Heuristics for tie-breaks
Prefer the more managed option unless a requirement forbids it - operations cost is the hidden bill. Prefer regional services with built-in Multi-AZ. Use purpose-built databases per access pattern instead of one engine for everything. Keep the number of distinct services low: each adds IAM, monitoring and skills overhead. Check Regional availability of every non-core service for the chosen Region before committing.

## 8. Anti-patterns to call out
Single-AZ production tiers - shared databases between unrelated services - long-lived access keys instead of roles - public S3/RDS exposure - lift-and-shift sizing copied from on-prem peak - Kubernetes chosen for résumé reasons - NAT Gateway for traffic that could use VPC endpoints (data-transfer cost) - no budget/alert on a new account.
