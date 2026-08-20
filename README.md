<p align="center">
  <img src="https://img.shields.io/badge/Kiro_Crew-Autonomous_Ops-7c3aed?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0id2hpdGUiLz48L3N2Zz4=&logoColor=white" alt="Kiro Crew"/>
  <img src="https://img.shields.io/badge/AWS_DevOps_Agent-MCP_Integration-FF9900?style=for-the-badge&logo=amazon-web-services&logoColor=white" alt="AWS DevOps Agent"/>
  <img src="https://img.shields.io/badge/34_Tools-Production_Ready-22c55e?style=for-the-badge" alt="34 Tools"/>
</p>

<h1 align="center">Kiro Crew + AWS DevOps Agent</h1>
<h3 align="center">Autonomous Incident Detection, Investigation, and Remediation</h3>

<p align="center">
  <em>One MCP config block. 34 tools. Runs while you sleep.</em>
</p>

<p align="center">
  <a href="https://github.com/SimplyNadaf/kiro-crew-devops-agent/stargazers"><img src="https://img.shields.io/github/stars/SimplyNadaf/kiro-crew-devops-agent?style=social" alt="Stars"/></a>
  <a href="https://github.com/SimplyNadaf/kiro-crew-devops-agent/network/members"><img src="https://img.shields.io/github/forks/SimplyNadaf/kiro-crew-devops-agent?style=social" alt="Forks"/></a>
  <a href="https://github.com/SimplyNadaf/kiro-crew-devops-agent/issues"><img src="https://img.shields.io/github/issues/SimplyNadaf/kiro-crew-devops-agent?style=flat-square" alt="Issues"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/SimplyNadaf/kiro-crew-devops-agent?style=flat-square" alt="License"/></a>
  <a href="https://dev.to/sarvar_04"><img src="https://img.shields.io/badge/Dev.to-Follow-0A0A0A?style=flat-square&logo=devdotto" alt="Dev.to"/></a>
  <a href="https://www.linkedin.com/in/sarvar04/"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin" alt="LinkedIn"/></a>
</p>

<p align="center">
  <a href="#-highlights">Highlights</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-34-tools-available">Tools</a> •
  <a href="#-security-model">Security</a> •
  <a href="#-demo-results">Demo</a> •
  <a href="#-cost">Cost</a>
</p>

---

## Highlights

| | Feature | Detail |
|---|---------|--------|
| 🔍 | **Autonomous Detection** | Cron scans every 30 minutes. No alarm needed. Catches silent failures. |
| 🧠 | **AI Investigation** | DevOps Agent correlates metrics, traces, deployments, and topology automatically. |
| 🔧 | **Auto-Remediation** | Agent applies fixes or opens a PR for human review. Your choice. |
| 📚 | **Self-Learning** | Kiro Crew remembers past incidents. Gets faster with every fix. |
| 🔒 | **Safe by Design** | Read-only IAM + deny patterns + PR-only output. Never touches production directly. |
| ⚡ | **5 Min Setup** | One MCP config block. One cron entry. Done. |

---

## The Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ECS service failing for 4 days         ← No alarm existed    │
│   Pipeline broken since last week        ← Nobody checked      │
│   Lambda timing out every invocation     ← Zero monitoring     │
│   CloudWatch alarms configured: 0        ← Flying blind        │
│                                                                 │
│   WHO NOTICED?  Nobody. Until now.                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Traditional monitoring only catches what you set alarms for. Everything else fails silently.

**This repo fixes that.** An autonomous agent checks everything, every 30 minutes, whether you configured an alarm or not.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         KIRO CREW                                 │
│                                                                   │
│   ┌─────────────┐        ┌──────────────────┐                    │
│   │  Cron Job   │------->│   Orchestrator   │                    │
│   │ (*/30 * * *)│        │  (claude-sonnet) │                    │
│   └─────────────┘        └────────┬─────────┘                    │
│                                   │                               │
│                      Spawns 5 parallel subagents                  │
│                                   │                               │
│          ┌────────────────────────┼────────────────────┐         │
│          v            v           v          v         v         │
│   ┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ ┌──────┐    │
│   │   ECS    │ │  CI/CD   │ │CloudW. │ │DevOps  │ │Lambda│    │
│   │  Check   │ │  Check   │ │ Check  │ │ Agent  │ │Check │    │
│   └────┬─────┘ └────┬─────┘ └───┬────┘ └───┬────┘ └──┬───┘    │
│        └─────────────┴───────────┴──────────┴─────────┘         │
│                               │                                   │
│                     Consolidated findings                         │
│                     (severity-prioritized)                        │
│                               │                                   │
│                     ┌─────────v──────────┐                       │
│                     │   Coding Agent     │                       │
│                     │  (writes fix, PR)  │                       │
│                     └─────────┬──────────┘                       │
└───────────────────────────────┼───────────────────────────────────┘
                                │
               ┌────────────────┼────────────────┐
               v                                 v
    ┌────────────────────┐            ┌──────────────────┐
    │  AWS DevOps Agent  │            │     GitHub       │
    │  (MCP endpoint)    │            │  (Pull Request)  │
    │                    │            │                  │
    │  • chat            │            │  Human reviews   │
    │  • investigate     │            │  in the morning  │
    │  • recommend       │            │                  │
    └────────────────────┘            └──────────────────┘
```

**The separation:**
- **DevOps Agent = the brain** (read-only, investigates, produces exact fix commands)
- **Kiro Crew = the hands** (orchestrates, executes, verifies, learns from past incidents)

---

## Quick Start

### Prerequisites

| Requirement | Detail |
|-------------|--------|
| Kiro Crew | [Install guide](https://github.com/kirodotdev/KiroCrew) |
| AWS Account | With resources to monitor (ECS, Lambda, etc.) |
| IAM Permissions | `aidevops:*` for Agent Space management |
| AWS CLI v2 | Configured with credentials |
| Region | us-east-1, us-west-2, or eu-west-1 |

### Step 1: Create an Agent Space

```bash
aws devops-agent create-agent-space \
  --name "production-monitoring" \
  --description "Autonomous production health monitoring" \
  --region us-east-1
```

> Save the `agentSpaceId` from the output. You will need it for every step below.

### Step 2: Create IAM Role

```bash
# Create the role with trust policy
aws iam create-role \
  --role-name DevOpsAgentSourceRole \
  --assume-role-policy-document file://iam-trust-policy.json \
  --description "Read-only access for AWS DevOps Agent monitoring"

# Attach ReadOnlyAccess (observe everything, change nothing)
aws iam attach-role-policy \
  --role-name DevOpsAgentSourceRole \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

> Edit `iam-trust-policy.json` first and replace `YOUR_ACCOUNT_ID` with your actual AWS account ID.

### Step 3: Associate AWS Account

```bash
aws devops-agent associate-service \
  --agent-space-id YOUR_SPACE_ID \
  --service-id aws \
  --configuration '{
    "aws": {
      "assumableRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/DevOpsAgentSourceRole",
      "accountId": "YOUR_ACCOUNT_ID",
      "accountType": "monitor"
    }
  }' \
  --region us-east-1
```

### Step 4: Enable Access Tokens

```bash
aws devops-agent update-agent-space \
  --agent-space-id YOUR_SPACE_ID \
  --access-token-configuration '{"enabled": true}' \
  --region us-east-1
```

### Step 5: Create Access Token

```bash
aws devops-agent create-access-token \
  --agent-space-id YOUR_SPACE_ID \
  --name "kiro-crew-monitor" \
  --scope "operate" \
  --client-type "agent" \
  --expires-in-days 60 \
  --region us-east-1
```

> Save the token securely. You will not see it again.

### Step 6: Add MCP Server to Kiro Crew

```bash
kirocrew config mcp add aws-devops-agent \
  --url "https://connect.aidevops.us-east-1.api.aws/mcp" \
  --header "X-Agent-Space-Id=YOUR_SPACE_ID"
```

Or add directly to `~/.kiro/settings/mcp.json` using `mcp-config.json` from this repo.

### Step 7: Add Cron Job

In Crew Dashboard > **Schedule** > **Add Job**:

| Field | Value |
|-------|-------|
| Name | `production-health-check` |
| Schedule | `*/30 * * * *` |
| Agent | `default` |
| Message | Check production health via AWS DevOps Agent. Scan ECS, Lambda, CodeBuild, CodePipeline, and CloudWatch. Flag any issues found with severity and recommended fixes. |

### Step 8: Verify

```bash
python3 test-connection.py
```

**That's it. Your autonomous SRE agent is live.**

---

## Repository Contents

```
kiro-crew-devops-agent/
├── README.md                 # You are here
├── mcp-config.json           # MCP config (bearer token auth)
├── mcp-config-sigv4.json     # MCP config (SigV4 auth, no token rotation)
├── cron-config.json          # Cron job definition (30-min health checks)
├── iam-trust-policy.json     # IAM trust policy for DevOps Agent
├── deny-patterns.json        # Safety: block destructive commands
├── test-connection.py        # Verify MCP connection works
└── LICENSE                   # MIT
```

---

## 34 Tools Available

When you connect DevOps Agent via MCP, your Crew agent gets instant access to:

<details>
<summary><b>Investigation and Monitoring (9 tools)</b></summary>

| Tool | What It Does |
|------|--------------|
| `chat` | Instant health check, cost analysis, architecture review, topology mapping |
| `investigate` | Deep async root-cause analysis across all monitored services (5-8 min) |
| `create_investigation` | Start investigation with priority level (P1/P2/P3) |
| `list_recommendations` | Get AI-generated mitigations prioritized by severity |
| `get_recommendation` | Detailed mitigation specification with CLI commands |
| `list_journal_records` | Stream investigation findings in real-time |
| `start_evaluation` | Evaluate against operational goals (SLOs) |
| `list_tasks` | Track async investigation status |
| `get_task` | Check if an investigation has completed |

</details>

<details>
<summary><b>Release and Deployment Safety (2 tools)</b></summary>

| Tool | What It Does |
|------|--------------|
| `create_release_readiness_review` | Analyze PRs for production risk patterns |
| `create_release_testing_job` | Run exploratory tests on deployed apps |

</details>

<details>
<summary><b>Service and Space Management (4 tools)</b></summary>

| Tool | What It Does |
|------|--------------|
| `get_service` | Detailed service topology, dependencies, health |
| `list_agent_spaces` | Manage multiple monitoring environments |
| `create_agent_space` | Provision new monitoring environments |
| `update_agent_space` | Modify space settings |

</details>

<details>
<summary><b>Access and Security (4 tools)</b></summary>

| Tool | What It Does |
|------|--------------|
| `create_access_token` | Issue new credentials programmatically |
| `get_access_token` | Inspect token details and expiration |
| `list_access_tokens` | Audit all active tokens |
| `revoke_access_token` | Revoke compromised credentials immediately |

</details>

<details>
<summary><b>+ 15 more tools for CRUD on spaces, associations, and configurations</b></summary>

Full list available via `tools/list` on the MCP endpoint after connection.

</details>

---

## What DevOps Agent Monitors

| Service | Signals Analyzed |
|---------|-----------------|
| Amazon ECS | Services, tasks, deployments, health checks, task definitions, CPU/memory |
| AWS Lambda | Invocations, errors, duration, throttles, cold starts, timeouts |
| Amazon API Gateway | 5xx errors, latency, integration failures, throttling |
| Amazon RDS | Connections, CPU, storage, replication lag, deadlocks |
| Amazon DynamoDB | Throttles, capacity, read/write latency |
| Amazon EC2 | Status checks, CPU, network, disk |
| Amazon CloudWatch | Alarms, metrics, anomaly bands |
| AWS CodeBuild | Build status, duration, failures, logs |
| AWS CodePipeline | Pipeline state, stage failures, deployment history |

---

## Security Model

<table>
<tr><td>

### 5 Layers of Safety

</td></tr>
</table>

| # | Layer | How It Works |
|---|-------|--------------|
| 1 | **Read-only IAM** | DevOps Agent role uses `ReadOnlyAccess`. Can observe everything, change nothing. |
| 2 | **Deny patterns** | 16 patterns block destructive commands even if the agent attempts them. See `deny-patterns.json`. |
| 3 | **PR-only output** | Agent writes code and opens a Pull Request. Never deploys directly to production. |
| 4 | **CloudTrail audit** | Every MCP call logged with source IP, tool name, timestamp, and request parameters. |
| 5 | **Token scoping** | Tokens expire in 1-60 days. Optional IP allowlist. One-click revocation. |

**The pattern: observe everything, change nothing, suggest via PR, human approves.**

---

## Demo Results

In a live recording, the agent completed a full infrastructure investigation in **46 seconds**:

### What Was Broken

| Issue | Severity | Detail |
|-------|----------|--------|
| 🔴 ECS failure loop | CRITICAL | Tasks failing continuously, health check grace period = 0 |
| 🔴 CI/CD breakdown | CRITICAL | Empty CodeCommit repo, pipeline permanently stuck on Failed |
| 🟠 Zero monitoring | HIGH | 0 CloudWatch alarms in entire account |
| 🟠 No source code | HIGH | CodeCommit has 0 branches, nothing to build |
| 🟡 CodeBuild timeout | MEDIUM | 5-minute timeout too short for real builds |

### What the Agent Fixed (48 seconds)

| # | Fix | Before | After |
|---|-----|--------|-------|
| 1 | ECS health check grace period | 0 seconds | 60 seconds |
| 2 | CloudWatch alarm (ECS) | Did not exist | Active |
| 3 | CloudWatch alarm (CodeBuild) | Did not exist | Active |
| 4 | CodeBuild timeout | 5 minutes | 30 minutes |
| 5 | CodeCommit main branch | 0 branches | 1 branch with buildspec.yml |

**Total time from detection to fix: under 2 minutes. No human involved.**

---

## Cost

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| Kiro Crew (Claude Sonnet 4) | $30-120/month | 48 cron runs/day at $0.02-0.08 each |
| AWS DevOps Agent | $0 | Included with Agent Space |
| **Total** | **~$1-4/day** | |
| | | |
| **Compare with** | | |
| On-call engineer (nights) | $6,000+/month | Plus burnout and context-switch cost |
| Single missed incident | $500-50,000+ | Depending on duration and customer impact |

> First catch pays for months of monitoring.

---

## Alternative: SigV4 Auth (No Token Rotation)

If you prefer using existing AWS credentials instead of managing bearer tokens:

```json
{
  "mcpServers": {
    "aws-devops-agent": {
      "command": "uvx",
      "timeout": 120000,
      "args": [
        "mcp-proxy-for-aws@latest",
        "https://connect.aidevops.us-east-1.api.aws/mcp",
        "--service", "aidevops",
        "--region", "us-east-1"
      ]
    }
  }
}
```

Uses `~/.aws/credentials` or instance profile. No separate token to create or rotate.

---

## Kiro Crew Series

This is **Part 6** of the Kiro Crew series:

| # | Article | Link |
|---|---------|------|
| 1 | Introducing Kiro Crew | [Read](https://dev.to/aws-builders/introducing-kiro-crew-awss-open-source-ai-agent-orchestrator-1e63) |
| 2 | I Spent a Day With Kiro Crew | [Read](https://dev.to/aws-builders/i-spent-a-day-with-kiro-crew-heres-what-it-actually-does-fk0) |
| 3 | Cron Jobs Replaced 4 Hours of Weekly Toil | [Read](https://dev.to/aws-builders/how-kiro-crews-cron-jobs-replaced-4-hours-of-weekly-toil-37h) |
| 4 | The Security Model That Got CISO Approval | [Read](https://dev.to/aws-builders/i-showed-my-ciso-kiro-crew-heres-the-security-model-that-got-it-approved-423j) |
| 5 | I Built a Custom App in 5 Minutes | [Read](https://dev.to/aws-builders/i-built-a-custom-kiro-crew-app-in-5-minutes-the-app-kit-nobodys-talking-about) |
| 6 | **This repo: Crew + DevOps Agent** | You are here |

---

## Related Resources

| Resource | Link |
|----------|------|
| Kiro Crew (GitHub) | [github.com/kirodotdev/KiroCrew](https://github.com/kirodotdev/KiroCrew) |
| AWS DevOps Agent Docs | [docs.aws.amazon.com/devopsagent](https://docs.aws.amazon.com/devopsagent/latest/userguide/) |
| DevOps Agent MCP Setup | [repost.aws](https://www.repost.aws/articles/ARSH7PwFXZRWS1Pp2LZPzFug/call-aws-devops-agent-from-kiro-and-claude-code-over-mcp) |
| DevOps Agent GA Blog | [aws.amazon.com/blogs](https://aws.amazon.com/blogs/mt/announcing-general-availability-of-aws-devops-agent/) |

---

## Author

<table>
<tr>
<td align="center" width="200">
<img src="https://github.com/SimplyNadaf.png" width="100" style="border-radius:50%"/>
<br/>
<b>Sarvar Nadaf</b>
<br/>
Cloud Architect | 7x AWS Certified
<br/>
200+ Articles | 30K+ Followers
</td>
<td>

| Platform | Link |
|----------|------|
| Portfolio | [sarvarnadaf.com](https://sarvarnadaf.com) |
| LinkedIn | [linkedin.com/in/sarvar04](https://www.linkedin.com/in/sarvar04/) |
| Dev.to | [dev.to/sarvar_04](https://dev.to/sarvar_04) |
| YouTube | [@TechwithSarvar](https://www.youtube.com/@TechwithSarvar) |
| X (Twitter) | [@SarvarN_04](https://x.com/SarvarN_04) |
| AWS Builder | [builder.aws.com/@sarvar](https://builder.aws.com/community/@sarvar) |

</td>
</tr>
</table>

---

<p align="center">

**If this helped you, please give it a star!**

<a href="https://github.com/SimplyNadaf/kiro-crew-devops-agent/stargazers"><img src="https://img.shields.io/github/stars/SimplyNadaf/kiro-crew-devops-agent?style=for-the-badge&color=gold" alt="Star this repo"/></a>

</p>

<p align="center">
  <a href="https://github.com/SimplyNadaf/kiro-crew-devops-agent/fork"><img src="https://img.shields.io/badge/Fork_this_repo-181717?style=for-the-badge&logo=github" alt="Fork"/></a>
  <a href="https://github.com/SimplyNadaf/kiro-crew-devops-agent/issues/new"><img src="https://img.shields.io/badge/Report_Issue-ef4444?style=for-the-badge" alt="Issue"/></a>
</p>

---

<p align="center">
  <sub>Built with Kiro Crew and AWS DevOps Agent. Licensed under MIT.</sub>
</p>
