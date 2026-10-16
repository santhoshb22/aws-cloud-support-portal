# Run and deploy

## Local development

Requires Python 3.10 or newer.

~~~bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
python app.py
~~~

Open http://127.0.0.1:5000 and test:

~~~bash
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/ops
~~~

Local mode intentionally avoids AWS API calls.

## Container

~~~bash
docker build -t cloud-support-portal:local .
docker run --rm -p 5000:5000 -e APP_ENV=local cloud-support-portal:local
~~~

## EC2 deployment checklist

1. Confirm the instance is intended to be running and review current AWS charges.
2. Use Amazon Linux 2023 and a supported Python runtime.
3. Install Git and Python packages from approved package sources.
4. Deploy code from this repository; keep .env outside version control.
5. Run Gunicorn behind a properly restricted security group. Do not expose Flask's development server directly to the internet.
6. Attach a least-privilege instance profile if AWS SDK access is required.
7. Restrict RDS inbound port 5432 to the application security group.
8. Validate the application, logs, database authentication, and billing before leaving resources running.

## Cost guardrails

- Keep EC2 and RDS stopped when the lab is not in use.
- Avoid creating a NAT gateway or load balancer without reviewing costs first.
- Stopping compute does not remove every possible charge; storage and other provisioned resources can still cost money.
- Never include account-specific endpoints, IDs, secrets, or unredacted console screenshots in public documentation.
