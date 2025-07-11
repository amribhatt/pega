#!/usr/bin/env python3
"""
Simple setup for Pega MCP + ADK Agent
"""

import os
import sys
from pathlib import Path

def get_input(prompt, default="", required=True, secret=False):
    while True:
        if secret:
            import getpass
            value = getpass.getpass(prompt)
        else:
            value = input(prompt)
        
        if not value and required:
            print("Required field!")
            continue
        elif not value and not required:
            return default
        else:
            return value

def create_mcp_env():
    print("\nPega MCP Server Setup")
    print("-" * 30)
    
    env_file = Path("pega-mcp/.env")
    if env_file.exists():
        overwrite = input("MCP .env exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            return True
    
    base_url = get_input("Pega Platform URL: ")
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    
    client_id = get_input("OAuth Client ID: ")
    client_secret = get_input("OAuth Client Secret: ", secret=True)
    app_alias = get_input("Application Alias: ")
    
    env_content = f"""PEGA_BASE_URL={base_url}
PEGA_CLIENT_ID={client_id}
PEGA_CLIENT_SECRET={client_secret}
APP_ALIAS={app_alias}
API_BASE_PATH=/prweb/app/{{app_alias}}/api/application/v2
OAUTH2_TOKEN_URL=/prweb/PRRestService/oauth2/v1/token
VERIFY_SSL=true
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8080
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("MCP .env created")
        return True
    except Exception as e:
        print(f"Error creating MCP .env: {e}")
        return False

def create_adk_env():
    print("\nPega ADK Agent Setup")
    print("-" * 25)
    
    env_file = Path("pega-adk/.env")
    if env_file.exists():
        overwrite = input("ADK .env exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            return True
    
    mcp_url = get_input("MCP Server URL (default: http://localhost:8080/mcp/): ", 
                        default="http://localhost:8080/mcp/", required=False)
    model_name = get_input("AI Model (default: gemini-2.0-flash): ", 
                          default="gemini-2.0-flash", required=False)
    agent_name = get_input("Agent Name (default: pega_adk_agent): ", 
                          default="pega_adk_agent", required=False)
    
    env_content = f"""MCP_SERVER_URL={mcp_url}
AI_MODEL={model_name}
AGENT_NAME={agent_name}
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("ADK .env created")
        return True
    except Exception as e:
        print(f"Error creating ADK .env: {e}")
        return False

def main():
    print("Pega MCP + ADK Agent Setup")
    print("=" * 40)
    
    setup_mcp = input("Setup MCP server? (Y/n): ").lower() != 'n'
    setup_adk = input("Setup ADK agent? (Y/n): ").lower() != 'n'
    
    success = True
    
    if setup_mcp:
        success &= create_mcp_env()
    
    if setup_adk:
        success &= create_adk_env()
    
    if success:
        print("\nSetup completed!")
        print("\nTo start:")
        print("1. cd pega-mcp && python server.py")
        print("2. cd pega-adk && python -m pega_adk_agent.agent")
    else:
        print("\nSetup failed!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1) 