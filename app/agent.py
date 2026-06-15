from datetime import datetime, timezone
from typing import Any, Dict, List


def _first(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    return rows[0] if rows else {}


def analyze_incident(error_summary, timeline, deployment_events, latency_services):
    """Deterministic agent-style reasoning layer for reliable hackathon demos.

    This can be replaced with Splunk hosted models or an external LLM, but this
    deterministic flow keeps the demo reliable under deadline pressure.
    """
    top_error = _first(error_summary)
    top_latency = _first(latency_services)
    deployment = _first(deployment_events)

    likely_service = top_error.get("service", "checkout-api")
    likely_endpoint = top_error.get("endpoint", "/checkout")
    likely_version = top_error.get("deployment_version", "v2.3.1")
    error_count = top_error.get("count", "unknown")
    avg_latency = top_latency.get("avg(latency_ms)", "unknown")

    root_cause = (
        f"The most likely root cause is a regression affecting {likely_service} "
        f"on {likely_endpoint} after deployment {likely_version}. Splunk evidence "
        f"shows elevated 5xx errors and high latency during the same incident window."
    )

    if deployment:
        root_cause += " A deployment event was detected before the error spike, increasing confidence in a deployment-related incident."

    recommendations = [
        "Rollback checkout-api from v2.3.1 to the previous stable version.",
        "Check database connection pool saturation and timeout configuration.",
        "Temporarily scale checkout-api and payment-service capacity.",
        "Notify on-call engineering and customer support with the generated summary.",
        "Add pre-deployment latency and dependency regression checks."
    ]

    postmortem = f"""
# Incident Postmortem Draft

## Title
Checkout API latency and payment failure incident

## Generated
{datetime.now(timezone.utc).isoformat()}

## Impact
Customers experienced checkout failures, payment timeouts, and elevated response latency.

## Detection
Splunk telemetry showed a spike in ERROR events, 5xx status codes, and latency above normal thresholds.

## Timeline
- Baseline application traffic was normal before the deployment.
- checkout-api deployment v2.3.1 completed.
- Error rate and latency increased after the deployment.
- Database and payment-service errors appeared during the incident window.

## Probable Root Cause
{root_cause}

## Supporting Evidence
- Primary affected service: {likely_service}
- Primary affected endpoint: {likely_endpoint}
- Error events found: {error_count}
- Average high-latency value: {avg_latency}

## Recommended Mitigation
{recommendations[0]}

## Prevention
- Add automated latency checks before deployment.
- Add deployment correlation to incident dashboards.
- Monitor database connection pool saturation.
- Improve rollback runbooks and incident readiness.
""".strip()

    return {
        "summary": f"{likely_service} is the primary affected service with {error_count} error events.",
        "root_cause": root_cause,
        "confidence": "High" if deployment else "Medium",
        "recommendations": recommendations,
        "postmortem": postmortem,
    }
