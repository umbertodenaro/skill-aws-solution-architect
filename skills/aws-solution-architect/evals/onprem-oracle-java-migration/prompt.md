---
tags: [aws-solution-architect]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

We run ~120 servers on-prem in a VMware datacenter: a Java monolith on WebLogic, an Oracle 19c database (4 TB), some Windows file servers. The lease on the datacenter ends in 14 months. Management wants to be on AWS before then, with minimal downtime for the Oracle database. Give me a migration strategy and wave plan, including which of the 7 Rs per workload, the tooling, network connectivity, and what could go wrong.
