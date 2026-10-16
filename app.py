"""Cloud Support Portal demo. Local mode makes no AWS API calls."""
import os
from datetime import datetime, timezone
from flask import Flask, jsonify

app = Flask(__name__)
APP_ENV = os.getenv("APP_ENV", "local").strip().lower()
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1").strip()
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "").strip()


def aws_identity_status():
    try:
        import boto3
        boto3.client("sts", region_name=AWS_REGION).get_caller_identity()
        return {"status": "ok", "detail": "AWS credentials resolved"}
    except Exception as exc:
        app.logger.warning("AWS identity check failed: %s", type(exc).__name__)
        return {"status": "not_configured_or_unavailable", "detail": "Check IAM role, credentials, and network access"}


def s3_status():
    if not S3_BUCKET_NAME:
        return {"status": "not_configured", "detail": "Set S3_BUCKET_NAME to enable the optional check"}
    try:
        import boto3
        boto3.client("s3", region_name=AWS_REGION).head_bucket(Bucket=S3_BUCKET_NAME)
        return {"status": "ok", "detail": "Configured bucket is reachable"}
    except Exception as exc:
        app.logger.warning("S3 check failed: %s", type(exc).__name__)
        return {"status": "unavailable", "detail": "Check bucket name, IAM permissions, region, and network access"}


@app.get("/")
def index():
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cloud Support Portal</title>
<style>body{font:16px/1.6 system-ui,sans-serif;max-width:850px;margin:4rem auto;padding:0 1.25rem}
main{padding:2rem;border:1px solid #8886;border-radius:1rem}.tag{display:inline-block;padding:.2rem .65rem;border:1px solid #8888;border-radius:99px}</style></head>
<body><main><span class="tag">AWS learning project</span><h1>Cloud Support Portal</h1>
<p>A small operations-focused Flask application for practicing health checks, cloud connectivity, and troubleshooting.</p>
<p>Environment: """ + APP_ENV.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + """</p>
<a href="/health">Health status (JSON)</a> · <a href="/ops">Operations summary (JSON)</a></main></body></html>"""


@app.get("/health")
def health():
    result = {
        "status": "ok",
        "application": "cloud-support-portal",
        "environment": APP_ENV,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "application": {"status": "ok"},
            "aws_identity": {"status": "skipped", "detail": "Local mode"},
            "s3": {"status": "skipped", "detail": "Local mode"},
        },
    }
    if APP_ENV == "aws":
        result["checks"]["aws_identity"] = aws_identity_status()
        result["checks"]["s3"] = s3_status()
        if result["checks"]["aws_identity"]["status"] != "ok":
            result["status"] = "degraded"
    return jsonify(result), (200 if result["status"] == "ok" else 503)


@app.get("/ops")
def ops():
    return jsonify({
        "application": "cloud-support-portal",
        "environment": APP_ENV,
        "aws_region": AWS_REGION if APP_ENV == "aws" else "not used in local mode",
        "configured_features": {
            "aws_sdk_checks": APP_ENV == "aws",
            "s3_check": bool(S3_BUCKET_NAME) and APP_ENV == "aws",
            "rds_postgresql": "TCP connectivity tested separately; app query integration must be verified",
            "cloudwatch": "planned",
            "sns": "planned",
        },
        "security_note": "This endpoint omits credentials, account IDs, endpoints, and resource identifiers.",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
