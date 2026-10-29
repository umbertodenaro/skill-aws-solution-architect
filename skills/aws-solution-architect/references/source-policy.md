# Source policy - how to stay grounded in official AWS documentation

## Contents
1. What counts as an official source
2. Verification order (tools)
3. What must be verified live
4. How to cite
5. Master index of verified entry points

## 1. What counts as official
Allowed: `docs.aws.amazon.com`, `aws.amazon.com` (product pages, compliance, whitepapers, Architecture Center, AWS blogs by AWS staff as *supporting* context), `repost.aws/knowledge-center` (AWS-run), AWS Prescriptive Guidance, AWS Well-Architected, AWS Decision Guides, AWS-owned GitHub orgs (`aws-samples`, `awslabs`, `aws-cloudformation`, `aws`) for code samples.
Not allowed as evidence: third-party blogs, forums, vendor comparisons, training-course notes, AI-generated summaries. If the user supplies them, treat as claims to check against AWS docs.

Rank evidence: (1) user guide / API reference / whitepaper / Well-Architected / Decision Guide, (2) Prescriptive Guidance / Architecture Center, (3) AWS blog posts and re:Post articles (good for patterns, weaker for current limits - check they are recent).

## 2. Verification order
1. **AWS documentation MCP / search tool** when available (e.g. `search_documentation`, `read_documentation`, `get_regional_availability`, or any AWS docs MCP server such as `awslabs.aws-documentation-mcp-server`). Search with the exact service and feature names; the returned chunk is verbatim page text - answer from it and cite its URL. Read the full page only if the chunk lacks the needed detail.
2. **Web fetch/search restricted to the official domains above.**
3. **Neither available**: use these references, mark volatile facts `[verify]`, give the link.

Also use live tools for: Regional availability of a service/feature, current service names, "what's new" (use the current-awareness topic or What's New pages).

## 3. Verify live (never from memory)
Quotas and limits - prices and discount percentages - SLAs - Regional availability - instance types/families - compliance programme scope per service - feature GA/preview status - deprecations/end-of-support dates - engine/runtime versions - default settings that changed recently.

Stable enough to state from references (still link): the six Well-Architected pillars, shared responsibility model, DR strategy definitions, the 7 Rs, multi-account principles, least privilege, Multi-AZ rationale.

## 4. How to cite
Inline after the claim: `[Doc](https://docs.aws.amazon.com/...)`. Use the exact page you read. One link per claim cluster, not link spam. If sources disagree or a page looks outdated (old publication date), say so and prefer the newer one.

## 5. Master index (entry points verified in this repo's authoring session)
- Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Pillars: operational excellence https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html - security https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html - reliability https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html - performance efficiency https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html - cost optimization https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html - sustainability https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html
- Lenses: Financial Services https://docs.aws.amazon.com/wellarchitected/latest/financial-services-industry-lens/financial-services-industry-lens.html - Serverless https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/welcome.html - Generative AI https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html - SaaS (tenant isolation) https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html - Migration lens pillars https://docs.aws.amazon.com/wellarchitected/latest/migration-lens/well-architected-framework-pillars.html
- Decision Guides index: https://docs.aws.amazon.com/decision-guides/
- Disaster recovery whitepaper: https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html
- Security Reference Architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/introduction.html
- Architecture icons: https://aws.amazon.com/architecture/icons/
- Pricing Calculator: https://docs.aws.amazon.com/pricing-calculator/latest/userguide/generate-estimate.html
