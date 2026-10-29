# Networking

## Contents
1. VPC layout principles
2. Connecting many VPCs and on-premises
3. Hybrid connectivity
4. Private access to services
5. Edge and DNS
6. Checklist

## 1. VPC layout principles
Use at least two AZs with the same subnet tiers in each: public (load balancers, NAT), private application, private data (no internet route). Size CIDRs for growth and avoid overlap with on-prem and other VPCs you may connect later - renumbering is painful. Use security groups as the primary stateful control, network ACLs sparingly. Put internet ingress behind an ALB/NLB (and CloudFront/WAF for web) rather than exposing instances. Reference diagrams: `reference-architectures.md`. Docs entry: https://docs.aws.amazon.com/vpc/

## 2. Many VPCs / accounts
AWS Transit Gateway is a network transit hub interconnecting VPCs and on-premises networks, with inter-Region peering; traffic between AWS data centres is encrypted at the physical layer: https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html . Use separate route tables to segment environments, attach an inspection VPC (Network Firewall / appliances) for centralised egress/east-west inspection, and share the gateway across accounts with AWS RAM (verify current sharing model). For 2-3 VPCs, simple peering may be cheaper and simpler - compare cost and operational model.

## 3. Hybrid connectivity
Options: Site-to-Site VPN (fast to start, internet-based, encrypted) and AWS Direct Connect (dedicated, consistent latency). For high availability the Direct Connect Resiliency Toolkit describes models: Maximum Resiliency (design for 99.99% SLA), High Resiliency (99.9%), and Development/Test (no SLA) - confirm the SLA conditions live: https://aws.amazon.com/blogs/networking-and-content-delivery/explore-the-aws-direct-connect-resiliency-toolkit/ . A common pattern: Direct Connect as primary with Site-to-Site VPN as backup, terminated on a Transit Gateway. Plan bandwidth for migration data transfer too (see `migration.md`).

## 4. Private access to AWS services and between services
VPC endpoints (gateway and interface) and AWS PrivateLink keep traffic off the public internet and can cut NAT data-processing costs; centralising interface endpoints in a hub VPC reduces endpoint cost across spokes: https://aws.amazon.com/blogs/networking-and-content-delivery/centralize-access-using-vpc-interface-endpoints/ . Use PrivateLink to expose a service to other VPCs/accounts without routing the whole network.

## 5. Edge and DNS
CloudFront for caching and TLS termination near users; AWS WAF and Shield for L7/DDoS protection; Route 53 for DNS with health checks and failover/latency/weighted routing; Global Accelerator for static anycast IPs and fast regional failover for TCP/UDP. Verify feature details per service page before committing.

## 6. Checklist
CIDR plan documented - 2+ AZs - private data tier - egress path and its cost understood - endpoints for high-volume AWS service traffic - flow logs enabled to central bucket - DNS strategy (private hosted zones, resolver rules for hybrid) - hybrid link redundancy - no 0.0.0.0/0 on admin ports.
