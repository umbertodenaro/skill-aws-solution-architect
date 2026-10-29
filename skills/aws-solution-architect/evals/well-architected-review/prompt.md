---
tags: [aws-solution-architect]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Review this architecture against the AWS Well-Architected Framework and give me prioritized findings:

- One AWS account for dev, test and prod.
- A single EC2 instance (m5.xlarge) in one AZ runs the web app and a self-managed MySQL on the same instance, data on a gp3 EBS volume. No snapshots.
- The instance has a public IP; security group allows 0.0.0.0/0 on ports 22, 80 and 3306.
- The app uses an IAM user access key stored in a .env file to read an S3 bucket that is public-read because 'it is easier'.
- Deployments are done by SSHing into the box and running git pull.
- No monitoring except an uptime ping from a third-party service. Nobody tracks the monthly bill.
