# Architecture and design notes

## High-level flow

~~~mermaid
flowchart TB
    Browser[Browser / tester] -->|HTTP| EC2[EC2: Flask / Gunicorn]
    EC2 -->|Private TCP 5432; connectivity test passed| RDS[(RDS PostgreSQL)]
    EC2 -. optional future integration .-> S3[(S3)]
    EC2 -. planned logs and metrics .-> CW[CloudWatch]
    CW -. planned alert .-> SNS[SNS]
~~~

## Network design

- VPC CIDR: 10.0.0.0/16
- Public subnets: 10.0.1.0/24 and 10.0.2.0/24
- Private subnets: 10.0.11.0/24 and 10.0.12.0/24
- RDS is intended to remain private and use a DB subnet group spanning private subnets.
- PostgreSQL ingress should allow TCP 5432 only from the application EC2 security group, not from the public internet.
- The private route table was designed without a NAT gateway to avoid unnecessary cost. Private resources therefore do not automatically have outbound internet access.

These are design notes from the lab, not a live inventory. Confirm current AWS state before making infrastructure changes.

## IAM and secrets

Use an EC2 instance profile / IAM role and least-privilege permissions. Do not use access keys in source files or bake credentials into container images. The optional app checks use the AWS SDK default credential chain.

## Verification status

- Verified: PostgreSQL client 15.19 installed on EC2 and TCP connection to the RDS endpoint on port 5432 succeeded.
- Not proven by that test: database login, SQL execution, application-to-database query flow, or production readiness.
- Planned: S3 integration, CloudWatch logs/alarms, and SNS notifications.
