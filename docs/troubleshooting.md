# Troubleshooting runbook

## 1. Application does not respond

1. Confirm the instance is running and the application process is active.
2. Check service logs for import errors, port conflicts, and configuration problems.
3. Test locally on the instance before testing from a browser.
4. Confirm the security group permits only the intended inbound application port from the correct source.
5. Verify the application is listening on the expected interface and port.

## 2. Cannot connect to PostgreSQL on port 5432

Check in this order:

1. Confirm RDS status is Available and the endpoint/port are copied from the current console.
2. Confirm EC2 and RDS VPC/subnet routing are compatible.
3. Confirm the RDS security group allows inbound TCP 5432 from the EC2 security group.
4. Check network ACLs and route tables.
5. From a Linux shell, test TCP reachability without exposing secrets:

   ~~~bash
   timeout 5 bash -c '</dev/tcp/REPLACE_WITH_RDS_ENDPOINT/5432' && echo "TCP reachable" || echo "TCP failed"
   ~~~

6. If TCP succeeds, test PostgreSQL authentication using a secure prompt or managed secret source. Do not put a password directly in a shell command or commit it to a file.

**Interpretation:** TCP success proves only that a network connection could be established. It does not prove credentials are valid or SQL queries will succeed.

## 3. AWS SDK reports missing credentials or access denied

- On EC2, verify the intended IAM instance profile is attached.
- Confirm the role policy grants only the actions required for the feature being tested.
- Check the configured region and service resource region.
- Distinguish missing credentials from AccessDenied; the remedies are different.
- Never fix access issues by publishing or hard-coding long-lived access keys.

## 4. S3 check fails

- Confirm S3_BUCKET_NAME is set correctly.
- Check bucket region and IAM permissions for the specific operation.
- A failed HeadBucket can reflect permissions as well as a missing bucket.
- Keep bucket names and account-specific details out of public screenshots unless intentionally sanitized.

## 5. No CloudWatch alert or SNS notification

These integrations are currently documented as planned, not complete. Before claiming success, configure the relevant logs/metrics/alarms and SNS topic/subscription, then trigger a controlled test and record sanitized evidence.

## Evidence checklist

- Sanitized health endpoint response
- Successful local or container startup
- EC2-to-RDS TCP test output with endpoint redacted
- Database query result after authentication is verified
- CloudWatch/SNS evidence only after those integrations are configured and tested
