# Security, identity and compliance

## Contents
1. Shared responsibility
2. Multi-account foundation
3. Identity and access
4. Detection and logging
5. Data protection and network
6. Compliance map (PCI DSS, DORA, GDPR, evidence)
7. Regulated-industry checklist
8. Wording rules

## 1. Shared responsibility
AWS operates and secures the host/virtualization layer down to physical facilities; the customer owns the guest OS (patching), application software, and configuration of AWS-provided controls such as security groups. Responsibilities shift with the service model (more managed = more AWS responsibility). https://docs.aws.amazon.com/whitepapers/latest/aws-risk-and-compliance/shared-responsibility-model.html
Always include a one-line split in security sections: "AWS: ... Customer: ...".

## 2. Multi-account foundation
Use multiple accounts to isolate workloads/environments and apply guardrails across Well-Architected pillars: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html
- **AWS Organizations** with OUs; **AWS Control Tower** gives a landing zone (multi-account environment based on best practices), controls (preventive, detective, proactive), Account Factory for standard account provisioning, and a dashboard: https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html and controls https://docs.aws.amazon.com/controltower/latest/controlreference/controls.html
- **AWS Security Reference Architecture (SRA)**: prescriptive multi-account security design with a dedicated Security Tooling account (delegated administrator for GuardDuty, Security Hub, Config, IAM Access Analyzer; CloudTrail organization trails; Macie where S3 is used; Inspector where EC2/ECR): https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/introduction.html and https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/security-tooling.html
Typical OU/account set (adapt, verify against SRA): management, security tooling, log archive, network/shared services, workload accounts per environment, sandbox.
Guardrails: SCPs for region restriction and protection of security services; tag policies; budgets per account.

## 3. Identity and access
Official IAM best practices (verify the current list): https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html - human users via federation with an identity provider and temporary credentials; workloads use IAM roles (temporary credentials); require MFA; least privilege, start from managed policies and refine using IAM Access Analyzer; remove unused access; use conditions; guardrails across accounts (SCPs); permission boundaries to delegate.
CI/CD to AWS: use OIDC federation instead of stored keys. For GitHub Actions the trust policy must restrict the `token.actions.githubusercontent.com:sub` condition to specific organisation/repo/branch, otherwise workflows outside your control could assume the role: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html

## 4. Detection and logging
Baseline in every account (SRA): GuardDuty, Security Hub, AWS Config, IAM Access Analyzer, CloudTrail organization trail; send logs to a Log Archive account with restricted write/delete. Add Macie for S3 data discovery, Inspector for EC2/ECR/Lambda vulnerability scanning, Detective/Audit Manager when a team will use them. Service names evolve (for example Security Hub CSPM appears in current SRA text) - check live names.

## 5. Data protection and network
Encrypt at rest and in transit by default; use KMS keys with explicit key policies (customer-managed keys when regulation or separation of duty requires); Secrets Manager/Parameter Store for secrets; private subnets for data stores; VPC endpoints/PrivateLink to keep AWS service traffic off the internet; WAF and Shield at the edge for internet-facing apps; TLS certificates via ACM. See `networking.md`.

## 6. Compliance map
AWS Artifact is the portal for AWS compliance reports and agreements (SOC, PCI DSS, ISO and others): https://docs.aws.amazon.com/whitepapers/latest/aws-overview/security-services.html . SOC 3 is public; SOC 1/2 require NDA via Artifact (https://repost.aws/knowledge-center/download-share-artifact-documents).
- **PCI DSS**: AWS has a Service Provider PCI Report on Compliance and a shared responsibility matrix in Artifact; PCI DSS does not require single-tenant environments (AWS FAQ: https://aws.amazon.com/compliance/pci-faqs/). Architecture guidance: https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-security-reference-architecture-pci-data-security-standard-dss/introduction.html - design to minimise scope: isolate the cardholder data environment (own account/VPC), tokenise, restrict and log all access. Check which AWS services are in PCI scope for your Region on the compliance programme page before selecting them.
- **DORA** (EU financial sector operational resilience): ICT risk management, incident reporting, resilience testing, third-party risk; DORA does not restrict cloud adoption. AWS user guide and addendum: https://aws.amazon.com/compliance/dora/ . Map to: multi-AZ/Region design and tested DR (reliability), logging and incident process, exit strategy and concentration-risk thinking, contractual addendum (customer action via account manager).
- **GDPR**: shared responsibility is unchanged; AWS is processor, customer is usually controller. Residency: keep data in chosen Regions, document transfers. https://aws.amazon.com/compliance/gdpr-center/
- **Financial services in general**: use the FSI Lens (`well-architected.md`).

## 7. Regulated-industry checklist
Data classification - Region/residency decision - account separation for in-scope data - encryption + key ownership - immutable audit logs retained per policy - least-privilege and break-glass procedure - vulnerability and patch process - tested incident response and DR - evidence collection plan (Artifact, Config conformance packs, Audit Manager - verify availability) - third-party/exit plan.

## 8. Wording rules
Say "supports", "helps meet", "is in scope of the AWS programme" - never "makes you compliant". Certification belongs to the customer's own workload and assessor. If asked whether service X is PCI/HIPAA/etc. eligible, verify on the live compliance-scope pages; do not answer from memory.
