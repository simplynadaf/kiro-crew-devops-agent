#!/usr/bin/env python3
"""Test AWS DevOps Agent MCP connection from Kiro Crew."""
import json
import os

def main():
    mcp_path = os.path.expanduser("~/.kiro/settings/mcp.json")
    
    if not os.path.exists(mcp_path):
        print("ERROR: MCP config not found at", mcp_path)
        print("Run: kirocrew config mcp add aws-devops-agent --url ...")
        return
    
    config = json.load(open(mcp_path))
    servers = config.get("mcpServers", {})
    
    if "aws-devops-agent" not in servers:
        print("ERROR: aws-devops-agent not found in MCP config")
        print(f"Available servers: {list(servers.keys())}")
        print("\nAdd it with:")
        print('  kirocrew config mcp add aws-devops-agent --url "https://connect.aidevops.us-east-1.api.aws/mcp"')
        return
    
    agent = servers["aws-devops-agent"]
    print("AWS DevOps Agent MCP Configuration")
    print("=" * 40)
    print(f"Endpoint:  {agent.get('url', 'NOT SET')}")
    
    headers = agent.get('headers', {})
    space_id = headers.get('X-Agent-Space-Id', 'NOT SET')
    if space_id != 'NOT SET':
        print(f"Space ID:  {space_id[:8]}...{space_id[-4:]}")
    else:
        print(f"Space ID:  {space_id}")
    
    disabled = agent.get('disabled', False)
    print(f"Status:    {'DISABLED' if disabled else 'ENABLED'}")
    print(f"")
    print("Available tools (34):")
    print("  Investigation:  chat, investigate, create_investigation")
    print("  Monitoring:     list_recommendations, get_recommendation")
    print("  Release:        create_release_readiness_review")
    print("  Management:     list_agent_spaces, get_service")
    print("  Security:       create_access_token, revoke_access_token")
    print("  ... and 24 more")
    print("")
    
    if disabled:
        print("WARNING: Server is disabled. Enable it in Crew dashboard or config.")
    else:
        print("Ready! The agent can now call DevOps Agent tools.")
        print("Test with: 'Check production health' in a Crew chat session.")


if __name__ == "__main__":
    main()
