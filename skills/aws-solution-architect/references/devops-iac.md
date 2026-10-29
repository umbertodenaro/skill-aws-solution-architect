# DevOps, CI/CD, IaC and observability

## Contents
1. Principles
2. CI/CD on AWS
3. Infrastructure as code
4. Deployment strategies
5. Observability
6. Operating model

## 1. Principles
Everything in version control; environments created from code; pipelines are the only path to production; no long-lived credentials in CI; each deploy is small, reversible and observable. These map to Operational Excellence: https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html

## 2. CI/CD on AWS
AWS CodePipeline models source -> build -> test -> deploy stages and integrates partner/custom tools (e.g. GitHub, Jenkins): https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/aws-codepipeline.html . Related services: CodeBuild (build/test), CodeDeploy (deployments), CodeCommit (check current availability/status of the service live before recommending it for new repositories). Many teams keep GitHub/GitLab/other CI and deploy to AWS from there - then authenticate via OIDC federation to an IAM role scoped to repo and branch, never stored access keys: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html
Pipeline stages to recommend: lint/unit tests -> IaC validation (cfn-lint/cfn-guard/cdk-nag - verify tool pages) -> build + image scan -> deploy to dev -> integration tests -> approval gate for prod (if policy requires) -> progressive prod rollout -> post-deploy checks. Use separate AWS accounts per environment (see `security-compliance.md`).

## 3. Infrastructure as code
- **AWS CDK**: open-source framework to define infrastructure in TypeScript, JavaScript, Python, Java, C#/.NET or Go; synthesises to CloudFormation; v2 is current (v1 support ended June 1, 2023 per the guide): https://docs.aws.amazon.com/cdk/v2/guide/home.html
- **AWS CloudFormation**: declarative templates, stacks and StackSets across accounts/Regions: https://aws.amazon.com/pm/cloudformation/
- **Terraform** (AWS provider): popular multi-cloud alternative; not an AWS product - for provider/resource details use the AWS provider documentation and still verify AWS behaviour in AWS docs.
Selection: team already on Terraform -> Terraform; developers prefer general-purpose languages and AWS-only -> CDK; templates/governance simplicity or service-catalog use -> CloudFormation. Do not mix tools on the same resource.
When generating code: parameterise Region/account/env, avoid hard-coded ARNs, add tags, use least-privilege roles, never embed secrets (reference Secrets Manager/SSM), include a short README with deploy/destroy commands, and state what you did *not* verify (service quotas, Region availability). Generated code is a starting point and must be reviewed and linted before use.

## 4. Deployment strategies
Rolling, blue/green and canary: choose by risk and statefulness. Blue/green gives fast rollback by switching traffic; canary limits blast radius using automated metric checks; database migrations must be backward compatible (expand/contract). Feature flags decouple deploy from release. Verify service-specific support (ECS, Lambda aliases, CodeDeploy) on the current docs.

## 5. Observability
Observability = metrics, logs, traces that let you ask new questions and tie behaviour to SLOs/KPIs: https://aws.amazon.com/blogs/mt/what-is-observability-and-why-does-it-matter-part-1/ . Baseline: CloudWatch metrics/alarms/logs, X-Ray or OpenTelemetry-based tracing, dashboards per service, alarms on SLO burn rather than raw thresholds, log retention policy, central log account for audit logs, structured JSON logs with correlation IDs. Define SLIs/SLOs per user journey; page only on user-impacting symptoms.

## 6. Operating model
Runbooks for top failure modes, on-call rotation, post-incident reviews (blameless), game days for DR, change calendar for risky windows, cost and security reviews on a schedule. For incident handling in AWS accounts keep break-glass access and tested forensics procedures (see `security-compliance.md`).
