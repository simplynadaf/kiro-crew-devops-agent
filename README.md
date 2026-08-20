# Kiro Crew + AWS DevOps Agent: Autonomous Incident Response

> One MCP config block. 34 tools. Autonomous production monitoring that runs while you sleep.

This repository contains the complete setup for connecting **AWS DevOps Agent** to **Kiro Crew** over MCP (Model Context Protocol), enabling autonomous incident detection, investigation, and remediation.

## What This Does

- Monitors your AWS infrastructure every 30 minutes via cron
- Detects silent failures that have no alarms configured
- Investigates root cause across ECS, Lambda, CodeBuild, CodePipeline, CloudWatch
- Applies fixes autonomously (or opens a PR for human review)
- Learns from past incidents and gets smarter over time

## Architecture

```
+-----------------------------------------------------------+
|                       KIRO CREW                            |
|                                                           |
|  +-------------+     +----------------+                   |
|  |  Cron Job   |---->|  Orchestrator  |                   |
|  | (*/30 * * *)|     | (claude-sonnet)|                   |
|  +-------------+     +-------+--------+                   |
|                              |                            |
|                 Spawns parallel subagents                  |
|                              |                            |
|       +----------+-----------+-----------+                |
|       v          v           v           v                |
|  +--------+ +--------+ +--------+ +---------+            |
|  |  ECS   | | CI/CD  | |CloudW. | | DevOps  |            |
|  | Check  | | Check  | | Check  | | Agent   |            |
|  +--------+ +--------+ +--------+ +---------+            |
|                              |                            |
|                    Consolidated findings                   |
|                    (severity-prioritized)                  |
|                              |                            |
|                    +---------v----------+                 |
|                    |  Coding Agent      |                 |
|                    |  (writes fix, PR)  |                 |
|                    +--------------------+                 |
+-----------------------------------------------------------+
                               |
              +----------------+----------------+
              v                                 v
   +--------------------+            +------------------+
   |  AWS DevOps Agent  |            |     GitHub       |
   |  (MCP endpoint)    |            |  (Pull Request)  |
   |  - chat            |            |  Human reviews   |
   |  - investigate     |            |  in the morning  |
   |  - recommend       |            |                  |
   +--------------------+            +------------------+
```

## Quick Start

### Prerequisites

- [Kiro Crew](https://github.com/kirodotdev/KiroCrew) installed and running
- AWS account with resources to monitor
- IAM permissions: `aidevops:*` for Agent Space management
- AWS CLI v2 configured
- Region: us-east-1, us-west-2, or eu-west-1

### Step 1: Create an Agent Space

```bash
aws devops-agent create-agent-space \
  --name "production-monitoring" \
  --description "Autonomous production health monitoring" \
  --region us-east-1
```

Save the `agentSpaceId` from the output.

### Step 2: Create IAM Role for DevOps Agent

```bash
cat <<'EOF' > devops-agent-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Service": "aidevops.amazonaws.com"
    },
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": {
        "aws:SourceAccount": "YOUR_ACCOUNT_ID"
      }
    }
  }]
}
EOF

aws iam create-role \
  --role-name DevOpsAgentSourceRole \
  --assume-role-policy-document file://devops-agent-trust.json \
  --description "Read-only access for AWS DevOps Agent monitoring"

aws iam attach-role-policy \
  --role-name DevOpsAgentSourceRole \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

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

Save the token value securely.

### Step 6: Add MCP Server to Kiro Crew

Copy `mcp-config.json` into your Crew MCP settings:

```bash
kirocrew config mcp add aws-devops-agent \
  --url "https://connect.aidevops.us-east-1.api.aws/mcp" \
  --header "X-Agent-Space-Id=YOUR_SPACE_ID"
```

Or add directly to `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "aws-devops-agent": {
      "url": "https://connect.aidevops.us-east-1.api.aws/mcp",
      "headers": {
        "X-Agent-Space-Id": "YOUR_SPACE_ID"
      },
      "description": "AWS DevOps Agent (34 tools)",
      "disabled": false
    }
  }
}
```

### Step 7: Add Cron Job

In Crew Dashboard > Schedule > Add Job:

| Field | Value |
|-------|-------|
| Name | production-health-check |
| Schedule | `*/30 * * * *` |
| Agent | default |
| Message | Check production health via AWS DevOps Agent. Scan ECS, Lambda, CodeBuild, CodePipeline, and CloudWatch. Flag any issues found with severity and recommended fixes. |

## Configuration Files

| File | Description |
|------|-------------|
| `mcp-config.json` | MCP server configuration for DevOps Agent |
| `mcp-config-sigv4.json` | Alternative: SigV4 auth (no token rotation needed) |
| `cron-config.json` | Cron job definition for 30-minute health checks |
| `iam-trust-policy.json` | IAM trust policy for DevOps Agent role |
| `deny-patterns.json` | Safety deny patterns (prevent auto-deploy) |
| `test-connection.py` | Script to verify MCP connection is working |

## What AWS DevOps Agent Monitors

| Service | What It Checks |
|---------|----------------|
| Amazon ECS | Services, tasks, deployments, health checks, task definitions |
| AWS Lambda | Invocations, errors, duration, throttles, cold starts, timeouts |
| Amazon API Gateway | 5xx errors, latency, integration failures |
| Amazon RDS | Connections, CPU, storage, replication lag |
| Amazon DynamoDB | Throttles, capacity, latency |
| Amazon EC2 | Status checks, CPU, network |
| Amazon CloudWatch | Alarms, metrics, anomalies |
| AWS CodeBuild | Build status, duration, failures |
| AWS CodePipeline | Pipeline state, stage failures, deployment status |

## 34 Tools Available Over MCP

### Investigation and Monitoring

| Tool | Description |
|------|-------------|
| `chat` | Instant health check, cost analysis, architecture review |
| `investigate` | Deep async root-cause analysis (5-8 minutes) |
| `create_investigation` | Start investigation with priority level |
| `list_recommendations` | Get AI-generated mitigations with severity |
| `get_recommendation` | Detailed mitigation specification |
| `list_journal_records` | Stream investigation findings in real-time |
| `start_evaluation` | Evaluate against operational goals (SLOs) |
| `list_tasks` | Track async investigation status |
| `get_task` | Check if an investigation has completed |

### Release and Deployment Safety

| Tool | Description |
|------|-------------|
| `create_release_readiness_review` | Analyze PRs for production risk |
| `create_release_testing_job` | Run exploratory tests on deployed apps |

### Service and Space Management

| Tool | Description |
|------|-------------|
| `get_service` | Service topology, dependencies, health |
| `list_agent_spaces` | Manage monitoring environments |
| `create_agent_space` | Provision new monitoring environments |
| `update_agent_space` | Modify space settings |

### Access and Security

| Tool | Description |
|------|-------------|
| `create_access_token` | Issue new credentials programmatically |
| `list_access_tokens` | Audit all active tokens |
| `revoke_access_token` | Revoke compromised credentials |

## Security Model

### Why This Is Safe

1. **DevOps Agent is read-only** - Uses `ReadOnlyAccess` IAM policy. Can observe everything, change nothing.

2. **Deny patterns block destructive commands** - Even if the agent tries to deploy:

```json
{
  "deny_patterns": [
    "kubectl apply",
    "aws deploy create-deployment",
    "terraform apply",
    "aws ecs update-service",
    "aws lambda update-function-code",
    "aws cloudformation execute-change-set"
  ]
}
```

3. **Output is always a Pull Request** - Never a direct production change. Human reviews in the morning.

4. **Full CloudTrail audit trail** - Every MCP call logged with source IP, tool name, and timestamp.

5. **Token scoping and rotation** - Tokens expire in 1-60 days with optional IP allowlist.

## Demo: What the Agent Found

In a live demo, the agent spawned 5 parallel subagents and found:

| Issue | Severity | Detail |
|-------|----------|--------|
| ECS failure loop | CRITICAL | Tasks failing continuously, grace period = 0 |
| CI/CD breakdown | CRITICAL | Empty CodeCommit repo, pipeline permanently failed |
| Zero monitoring | HIGH | 0 CloudWatch alarms in entire account |
| CodeBuild timeout | MEDIUM | 5-minute timeout too short for real builds |
| No source code | HIGH | CodeCommit has 0 branches |

### Fixes Applied (by the agent)

1. ECS health check grace period: 0 to 60 seconds
2. Created CloudWatch alarm for ECS unhealthy tasks
3. Created CloudWatch alarm for CodeBuild failures
4. CodeBuild timeout: 5 min to 30 min
5. Created main branch in CodeCommit with buildspec.yml

Total investigation time: 46 seconds. Fix application: 48 seconds.

## Cost

| Component | Cost |
|-----------|------|
| Kiro Crew (Claude Sonnet 4) | ~$0.02-0.08 per cron run |
| 48 runs/day at */30 | ~$1-4/day |
| AWS DevOps Agent | Included with Agent Space |
| Compare with | On-call engineer: $200+/night |

First catch pays for months of monitoring.

## Alternative: SigV4 Authentication

If you prefer AWS credentials over bearer tokens:

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

Uses existing AWS credentials from `~/.aws/credentials` or instance profile. No separate token to rotate.

## Related Resources

- [Kiro Crew (GitHub)](https://github.com/kirodotdev/KiroCrew)
- [AWS DevOps Agent Documentation](https://docs.aws.amazon.com/devopsagent/latest/userguide/)
- [DevOps Agent MCP Setup Guide](https://www.repost.aws/articles/ARSH7PwFXZRWS1Pp2LZPzFug/call-aws-devops-agent-from-kiro-and-claude-code-over-mcp)
- [DevOps Agent GA Announcement](https://aws.amazon.com/blogs/mt/announcing-general-availability-of-aws-devops-agent/)

## Kiro Crew Series

This is Part 6 of the Kiro Crew series:

1. [Introducing Kiro Crew](https://dev.to/aws-builders/introducing-kiro-crew-awss-open-source-ai-agent-orchestrator-1e63)
2. [I Spent a Day With Kiro Crew](https://dev.to/aws-builders/i-spent-a-day-with-kiro-crew-heres-what-it-actually-does-fk0)
3. [Cron Jobs Replaced 4 Hours of Weekly Toil](https://dev.to/aws-builders/how-kiro-crews-cron-jobs-replaced-4-hours-of-weekly-toil-37h)
4. [The Security Model That Got CISO Approval](https://dev.to/aws-builders/i-showed-my-ciso-kiro-crew-heres-the-security-model-that-got-it-approved-423j)
5. [I Built a Custom App in 5 Minutes](https://dev.to/aws-builders/i-built-a-custom-kiro-crew-app-in-5-minutes-the-app-kit-nobodys-talking-about)
6. **This repo** - Crew + DevOps Agent autonomous ops

## Author

**Sarvar Nadaf** - Cloud Architect | 7x AWS Certified | 200+ Articles

- [Portfolio](https://sarvarnadaf.com)
- [LinkedIn](https://www.linkedin.com/in/sarvar04/)
- [Dev.to](https://dev.to/sarvar_04)
- [YouTube](https://www.youtube.com/@TechwithSarvar)
- [X (Twitter)](https://x.com/SarvarN_04)

## License

MIT
