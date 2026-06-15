# RescueOps AI

**Agentic Incident Commander for Splunk**

RescueOps AI helps operations teams investigate incidents faster using Splunk data and AI agents.

## Tagline

From alert noise to root cause in minutes.

## Hackathon Track

Observability

## Problem

Modern operations teams have too much telemetry and too little time. During incidents, engineers must jump across dashboards, logs, alerts, deployment notes, and chat messages to understand what happened.

## Solution

RescueOps AI turns Splunk telemetry into an AI-guided incident investigation. It queries Splunk, builds a timeline, identifies likely root causes, recommends next actions, and generates a postmortem draft.

## Features

- Splunk-powered incident investigation
- AI-generated incident summary
- Timeline reconstruction
- Root-cause hypothesis
- Recommended remediation actions
- Human approval workflow
- Postmortem draft generator
- Splunk MCP Server-ready architecture
- Splunk Python SDK fallback for reliable local demo

## Demo Scenario

A synthetic e-commerce checkout system experiences a production incident after deployment `v2.3.1`.

The incident includes:

- checkout API 500 errors
- payment authorization timeouts
- database connection pool saturation
- elevated latency
- deployment correlation

## How Splunk Is Used

Splunk Enterprise indexes synthetic application logs in the `rescueops` index. RescueOps AI uses SPL searches to retrieve evidence about errors, latency, deployments, and affected services.

## How AI Is Used

The AI layer acts as an incident commander with four agents:

1. Timeline Agent
2. Root Cause Agent
3. Recommendation Agent
4. Postmortem Agent

The included implementation uses deterministic agent-style reasoning for reliability during judging. It can be extended with Splunk Hosted Models, Splunk AI Toolkit, or external LLM APIs.

## Architecture

See [`architecture_diagram.md`](./architecture_diagram.md).

## Repository Structure

```text
rescueops-ai/
  app/
    main.py
    splunk_client.py
    agent.py
  data/
    synthetic_logs.jsonl
  scripts/
    generate_logs.py
  splunk/
    sample_searches.spl
  architecture_diagram.md
  README.md
  requirements.txt
  .env.example
  LICENSE
```

## Setup

### 1. Install Splunk Enterprise Trial

Install Splunk Enterprise locally and create an admin username/password.

Default local URLs:

```text
Splunk Web: https://localhost:8000 or http://localhost:8000
Management API: https://localhost:8089
```

### 2. Create Splunk Index

In Splunk Web:

```text
Settings → Indexes → New Index
```

Create:

```text
Index name: rescueops
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Demo Logs

The repo already includes `data/synthetic_logs.jsonl`, but you can regenerate it:

```bash
python scripts/generate_logs.py
```

### 5. Upload Logs to Splunk

In Splunk Web:

```text
Add Data → Upload
```

Use:

```text
File: data/synthetic_logs.jsonl
Sourcetype: _json
Index: rescueops
```

Then confirm data exists:

```spl
index=rescueops
```

### 6. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
copy .env.example .env
```

Update `.env`:

```env
SPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=your_password_here
SPLUNK_INDEX=rescueops
```

### 7. Run App

```bash
streamlit run app/main.py
```

Click **Run AI Incident Investigation**.

## Example SPL Queries

```spl
index=rescueops level=ERROR
| stats count by service endpoint deployment_version
| sort - count
```

```spl
index=rescueops latency_ms>1000
| stats count avg(latency_ms) max(latency_ms) by service deployment_version
| sort - avg(latency_ms)
```

```spl
index=rescueops message="deployment completed for checkout-api"
| table _time service deployment_version message
```

## Splunk MCP Server Path

RescueOps AI is designed to support Splunk MCP Server as the secure bridge between AI agents and Splunk data. For local hackathon reliability, this repo includes a Splunk Python SDK fallback.

Suggested MCP extension:

1. Install Splunk MCP Server from Splunkbase.
2. Enable token authentication in Splunk.
3. Configure the MCP server with a Splunk token.
4. Replace the SDK query layer with MCP tool calls.

## Human-in-the-Loop Safety

RescueOps AI recommends actions but does not execute production changes automatically. This keeps operators in control and makes the demo suitable for real-world operations workflows.

## Devpost Summary

RescueOps AI is an agentic observability assistant that helps engineering and operations teams investigate incidents faster using Splunk data. When an incident occurs, RescueOps AI queries Splunk logs and metrics, builds a timeline of what happened, identifies likely root causes, recommends next actions, and generates a post-incident report.

## License

MIT
