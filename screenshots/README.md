# Project screenshots

This folder is reserved for **sanitized evidence captured after each feature has been tested**. The project is still in progress; do not add mock screenshots or images that imply an integration works when it has not been verified.

## Planned evidence

Add screenshots here as the matching milestones are completed:

1. `01-portal-home.png` — application homepage running.
2. `02-health-endpoint.png` — successful `/health` response.
3. `03-operations-endpoint.png` — `/ops` response showing the verified feature status.
4. `04-ec2-instance.png` — EC2 instance and relevant status, with account-identifying details hidden.
5. `05-rds-connectivity.png` — successful EC2-to-RDS connection evidence, with the endpoint and identifiers redacted.
6. `06-database-query.png` — successful authenticated PostgreSQL query, only after we verify it.
7. `07-s3-check.png` — successful S3 test, only after it is implemented and tested.
8. `08-cloudwatch-alarm.png` — CloudWatch evidence, only after the alarm has been tested.
9. `09-sns-notification.png` — test notification, only after SNS has been configured and verified.
10. `10-ci-tests.png` — successful GitHub Actions run.

Not every screenshot will necessarily be needed; keep only the clearest evidence relevant to the features actually completed.

## Before uploading

- Hide AWS account IDs, private IPs, database endpoints, bucket names when sensitive, usernames, email addresses, browser profile details, and any other identifying information.
- Never include passwords, access keys, session tokens, private keys, secret values, or a visible `.env` file.
- Do not publish screenshots of billing or account pages containing personal or financial information.
- Capture real output from the actual project. Do not edit results to make a failed or incomplete test look successful.
- Use descriptive filenames and remove duplicate or blurry images.

## Completion rule

The main README should only describe the project as **Completed** after all features advertised as complete are implemented, tested, and supported by evidence. Any remaining optional feature must stay labelled as planned or out of scope. Passing a TCP connection test alone is not proof that a database login or SQL query works.
