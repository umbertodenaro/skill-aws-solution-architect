# Architecture diagrams

AWS publishes official architecture icons and guidelines: https://aws.amazon.com/architecture/icons/ . The renderer in `scripts/render_diagram.py` uses icon identifiers verified against the upstream sources (draw.io AWS4 library, awslabs/aws-icons-for-plantuml, the `diagrams` Python package) - see `scripts/verify_catalog.py`.

## Contents
1. Workflow
2. Spec format
3. Group types
4. Service keys
5. Output formats and how to render them
6. Drawing conventions
7. Limits and honesty notes

## 1. Workflow
Write the spec -> `--validate-only` -> render `--format all -o diagrams/` -> show Mermaid inline -> hand over `.drawio` (and others on request). If the user changes the design, edit the spec and re-render all formats; never hand-edit one format and leave the others stale.

## 2. Spec format
```json
{
  "title": "Name shown on the diagram",
  "direction": "LR",
  "groups": [{"id": "vpc", "label": "VPC", "type": "vpc", "parent": "region"}],
  "nodes":  [{"id": "alb", "service": "alb", "label": "Public ALB", "group": "vpc"}],
  "edges":  [{"from": "user", "to": "alb", "label": "HTTPS", "style": "dashed", "bidirectional": false}]
}
```
- ids: letters, digits, `_`, `-`; unique across groups and nodes.
- `group`/`parent` nest arbitrarily; omit for top level (outside the AWS Cloud box: users, internet, on-prem).
- `edges` connect nodes (not groups). `style`: solid (default) or dashed (async/optional/management traffic).
- `direction`: `LR` for request flows, `TB` for layered/tiered views.
Full example: `assets/example-spec.json`.

## 3. Group types
`cloud`, `region`, `account`, `vpc`, `az`, `public-subnet`, `private-subnet`, `onprem`, `generic`. Use `account` groups to show multi-account boundaries (e.g. workload vs shared-services vs security tooling), `generic` for logical clusters (e.g. "Data tier").

## 4. Service keys
List them with: `python3 -c "import json;print(*sorted(json.load(open('scripts/service_catalog.json'))['services']))"`. Categories: compute (ec2, lambda, ecs, eks, fargate, batch, beanstalk, autoscaling, apprunner), network (vpc, alb, nlb, apigw, cloudfront, route53, tgw, directconnect, vpn, igw, nat, vpce, privatelink, globalaccelerator, networkfirewall), storage (s3, ebs, efs, fsx, backup, storagegateway), database (rds, aurora, dynamodb, elasticache, memorydb, redshift, neptune, documentdb), integration (sqs, sns, eventbridge, stepfunctions, appsync, mq), analytics (kinesis, firehose, glue, athena, emr, opensearch, msk, lakeformation), security (iam, cognito, kms, secretsmanager, waf, shield, guardduty, securityhub, inspector, macie, acm, directoryservice), management (cloudwatch, cloudtrail, config, organizations, controltower, cloudformation, systemsmanager), devtools (codepipeline, codebuild, codecommit, codedeploy, xray, cdk), ml (sagemaker, bedrock), migration (mgn, dms, datasync), generic (user, client, internet, onprem, datacenter, generic).
Need a service that is missing? Use `generic` with a clear label, and (maintainers) add it to `service_catalog.json` then run `scripts/verify_catalog.py`. Do not guess icon names.

## 5. Formats
| Format | File | Best for | Render / open |
|---|---|---|---|
| Mermaid | `.mmd` | inline in chat, GitHub READMEs, docs | paste in a ```mermaid block; CLI: `mmdc -i x.mmd -o x.png` (mermaid-cli) |
| draw.io | `.drawio` | editable, official AWS icons, customer decks | open in diagrams.net / draw.io desktop; File > Export as PNG/SVG/PDF |
| PlantUML | `.puml` | docs-as-code, wikis | `java -jar plantuml.jar -tpng x.puml` (needs internet at render time: the file includes the AWS icon library from GitHub at tag v23.1, the version the catalog was verified against) |
| Python diagrams | `.py` | PNG with AWS icons and automatic edge routing | `pip install diagrams` + Graphviz installed; `python x.py` writes the PNG |

## 6. Drawing conventions (what makes a diagram useful)
Show trust boundaries: AWS account, Region, VPC, AZ, subnet tier. Arrows show request/data direction and are labelled with protocol or purpose. Put users/internet/on-prem on the left or top, data stores on the right or bottom. One diagram = one message: split "network view", "data flow", "CI/CD" and "DR" rather than one giant picture. Keep to ~15-25 icons per view. Note the AZ duplication once (draw AZ a and AZ b, or one AZ with "x2") consistently. Add a legend line for dashed = async/optional.

## 7. Limits and honesty notes
- Mermaid has no AWS icons (coloured boxes by category). It is the quick preview; use draw.io/PlantUML/Python for icon-based deliverables.
- The draw.io layout is an automatic left-to-right (or top-down) column layout by flow rank: a clean starting point, but expect to nudge some connectors in diagrams.net for a presentation-grade result. The Python `diagrams` output has Graphviz auto-routing.
- Icons follow the upstream libraries' current versions; AWS updates icon sets periodically, so re-run `verify_catalog.py` when upgrading.
