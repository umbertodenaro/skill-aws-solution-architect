# Data, analytics and generative AI

## Contents
1. Choosing data services
2. Lake / warehouse / lakehouse decisions
3. Governance
4. Generative AI on AWS
5. GenAI risk checklist

## 1. Choosing data services
Use the Decision Guides: analytics https://docs.aws.amazon.com/decision-guides/latest/decision-guides/analytics-on-aws-how-to-choose.html and databases https://docs.aws.amazon.com/decision-guides/latest/decision-guides/databases-on-aws-how-to-choose.html . The analytics guide covers: Athena, Clean Rooms, Data Firehose, DataZone, EMR, Glue, Kinesis Data Streams, Managed Service for Apache Flink, MSK, MWAA, OpenSearch Service, Quick, Redshift, S3, SageMaker.
| Need | Lean toward |
|---|---|
| Ad-hoc SQL on S3 data, pay per query | Athena |
| Heavy BI concurrency, warehouse semantics | Redshift |
| ETL/catalog | Glue |
| Big data frameworks (Spark etc.) | EMR |
| Real-time streams | Kinesis Data Streams or MSK + Flink |
| Search / log analytics | OpenSearch Service |
| Cross-organisation collaboration without sharing raw data | Clean Rooms |
| Business-wide data catalog/sharing | DataZone |
Verify the current feature set and Region availability of each service before recommending.

## 2. Lake / warehouse decisions
Land raw data immutably in S3, curate into query-optimised columnar formats, partition by common filters, catalog everything. Choose warehouse (Redshift) when you need consistent, high-concurrency SQL performance and BI; keep the lake as the system of record. Separate storage from compute so each scales independently. Document data ownership and SLAs per dataset.

## 3. Governance
Classify data; discover sensitive data (Macie for S3); central permissions (Lake Formation); encryption with KMS; audit access (CloudTrail data events where needed - cost impact); retention/lifecycle rules; data-residency boundaries respected by replication and by analytics services' Regions.

## 4. Generative AI on AWS
- **Lens first**: the Well-Architected Generative AI Lens extends the pillars to GenAI - model selection, prompt engineering, model customization, workload integration, continuous improvement, responsible AI; it explicitly excludes model training and advanced customization techniques: https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html
- **Amazon Bedrock** provides foundation models via API. **Knowledge Bases** give a managed RAG pipeline (ingestion from S3 and other sources, chunking, embedding, vector storage, retrieval and cited generation); **Guardrails** can screen prompts and responses (block topics, filter harmful content, hide sensitive information) and apply consistently across models: https://repost.aws/articles/ARO2JXBG6cQZObXj0TZJ4gjg/build-a-self-service-student-assistant-with-amazon-bedrock-knowledge-bases and https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- **Amazon SageMaker AI** for custom model training/hosting and MLOps when managed foundation-model APIs are not enough.
- Model catalogue, Regional model availability, quotas and prices change frequently -> always check live (`get_regional_availability` or Bedrock docs) before naming a model or Region.
- Decision sequence: can a prompt + RAG solve it? -> then fine-tuning/customization? -> then training custom model. Move down only with evidence from evaluation.

## 5. GenAI risk checklist
Data privacy (what leaves the VPC; use private connectivity/PrivateLink options - verify) - access control at document level in RAG - prompt injection and output filtering - evaluation set and regression testing for answer quality - human-in-the-loop for high-impact decisions - cost per request and rate limits - logging of prompts/responses with PII handling - auditability and model change management - regulatory duties (e.g. sector rules); cite sources in answers.
