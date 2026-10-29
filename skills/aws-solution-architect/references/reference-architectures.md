# Reference architectures (patterns to adapt, not to paste)

These are design patterns assembled from AWS Well-Architected guidance and the Decision Guides in `service-selection.md`. Adapt to the discovery drivers; verify service details live. For official worked examples, search the AWS Architecture Center / Prescriptive Guidance with the pattern name (use the documentation search tool rather than guessing URLs).

## Contents
1. Three-tier web application
2. Serverless API / web backend
3. Event-driven integration
4. Microservices on containers
5. Data lake and analytics
6. Streaming ingestion
7. GenAI RAG assistant
8. Multi-tenant SaaS
9. Hybrid / migration landing
10. Multi-Region active-passive

Every pattern below inherits these baselines: 2+ AZs, private data tier, IAM roles (no keys), encryption at rest/in transit, central logging, IaC, tagged resources, budget alerts.

## 1. Three-tier web application
**Use when**: classic web app, steady traffic, relational data. **Edge**: Route 53 -> CloudFront (+ WAF) -> ALB in public subnets. **App**: ECS Fargate (or EC2 Auto Scaling) in private subnets across AZs. **Data**: Aurora/RDS Multi-AZ in isolated subnets; ElastiCache optional; S3 for static/user content. **Egress**: NAT per AZ or VPC endpoints. **Watch**: session state (externalise), connection pooling, DB failover behaviour, cross-AZ traffic cost. Example spec: `assets/example-spec.json`.

## 2. Serverless API / web backend
**Use when**: spiky/unknown load, small team. **Flow**: CloudFront -> API Gateway (or Lambda function URL / AppSync) -> Lambda -> DynamoDB; Cognito for auth; S3 for assets; SQS/EventBridge for async work; Step Functions for orchestration. **Watch**: cold-start sensitivity, concurrency and downstream throttling, idempotency, timeouts chain, per-request cost at high steady volume (compare with containers). Use the Serverless Applications Lens: https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html

## 3. Event-driven integration
**Use when**: decoupling producers/consumers, fan-out, SaaS events. **Flow**: producers -> EventBridge bus (rules) / SNS topics -> SQS queues (buffer) -> Lambda/ECS consumers, DLQs on every queue. Choose per `service-selection.md` section 5. **Watch**: ordering and at-least-once delivery (idempotent consumers), poison messages, event schema governance, replay needs.

## 4. Microservices on containers
**Use when**: multiple teams/services, long-running workloads. **Compute**: ECS on Fargate (default) or EKS (when Kubernetes needed). **Ingress**: ALB with path/host routing; service-to-service via service discovery/mesh only if justified. **Data**: database per service where boundaries are real. **Platform**: ECR, pipeline per service, central observability. **Watch**: org skills, cluster upgrade burden (EKS), distributed tracing, cost of idle capacity.

## 5. Data lake and analytics
**Use when**: many sources, ad-hoc analytics, BI. **Flow**: ingest (DMS, DataSync, Firehose, Glue) -> S3 zones (raw/curated) with Glue Data Catalog + Lake Formation permissions -> Athena / Redshift / EMR -> QuickSight/BI. **Watch**: partitioning and file format for cost, governance and PII (Macie, Lake Formation), data ownership, small-files problem. See `data-genai.md` and the analytics Decision Guide.

## 6. Streaming ingestion
**Use when**: real-time telemetry/clickstream/CDC. **Flow**: producers -> Kinesis Data Streams or MSK -> Flink / Lambda for processing -> Firehose to S3 / OpenSearch / Redshift. **Watch**: shard/partition key skew, consumer lag, exactly-once expectations, retention vs replay.

## 7. GenAI RAG assistant
**Use when**: grounded Q&A over enterprise documents. **Flow**: documents in S3 -> Amazon Bedrock Knowledge Bases (managed ingestion, chunking, embedding, vector store, retrieval + cited generation) -> Bedrock model; Guardrails screen prompts and responses; app layer on Lambda/ECS with Cognito. Managed RAG overview: https://repost.aws/articles/ARO2JXBG6cQZObXj0TZJ4gjg/build-a-self-service-student-assistant-with-amazon-bedrock-knowledge-bases . **Watch**: data permissions per user (document-level access), prompt injection, evaluation of answer quality, model/Region availability (verify), cost per query, PII handling. Use the Generative AI Lens: https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html

## 8. Multi-tenant SaaS
**Use when**: one product serving many customers. **Decide first**: tenant isolation model (silo/pool/bridge) - isolation is a foundational topic and crossing the tenant boundary can be unrecoverable for a SaaS business: https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html . **Elements**: tenant-aware identity, tenant context propagation, per-tenant metering/cost attribution, noisy-neighbour controls, onboarding automation. **Watch**: compliance per tenant, data residency per tenant, per-tenant backup/restore.

## 9. Hybrid / migration landing
**Use when**: staged migration. Landing zone (Control Tower/Organizations), network hub with Transit Gateway, Direct Connect + VPN backup, identity federation, replication tooling (MGN/DMS/DataSync) into workload accounts. See `migration.md`, `networking.md`, `security-compliance.md`.

## 10. Multi-Region active-passive
**Use when**: RTO/RPO beyond what AZ resilience gives. Warm standby in a second Region: replicated data stores, scaled-down stack, health-checked DNS failover, IaC parity, tested runbook. See `reliability-dr.md` for strategy choice and tests.
