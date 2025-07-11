# Pega MCP + ADK Agent

A complete setup for Pega case management using MCP (Model Context Protocol) server and ADK (Agent Development Kit) agent.

## Overview

This repository contains two main components:

- **Pega MCP Server** (`pega-mcp/`) - Connects to Pega Platform APIs
- **Pega ADK Agent** (`pega-adk/`) - AI agent that uses MCP tools to manage Pega cases

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/amribhatt/pega.git
cd pega
```

### 2. Run Setup

```bash
python setup.py
```

This interactive script will:
- Prompt for your Pega Platform credentials
- Create `.env` files for both components
- Configure the MCP server and ADK agent

### 3. Create Virtual Environments

```bash
# Create virtual environment for MCP server
cd pega-mcp
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac

# Install MCP server dependencies
pip install -r requirements.txt

# Create virtual environment for ADK agent
cd ../pega-adk
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac

# Install ADK agent dependencies
pip install -r requirements.txt
```

### 4. Start the System

**Terminal 1 - Start MCP Server:**
```bash
cd pega-mcp
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
python server.py
```

**Terminal 2 - Start ADK Agent:**
```bash
cd pega-adk
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
adk run pega_adk_agent
```

Or to start with web interface:
```bash
cd pega-adk
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
adk web
```

## Configuration

### Required Pega Credentials

You'll need these from your Pega Platform:

- **Pega Platform URL** - Your Pega instance URL
- **OAuth Client ID** - OAuth2 client identifier
- **OAuth Client Secret** - OAuth2 client secret
- **Application Alias** - Your Pega application alias

### Environment Files

The setup creates two `.env` files:

**`pega-mcp/.env`** - MCP Server Configuration:
```
PEGA_BASE_URL=https://your-pega-instance.com
PEGA_CLIENT_ID=your_client_id
PEGA_CLIENT_SECRET=your_client_secret
APP_ALIAS=your_app_alias
```

**`pega-adk/.env`** - ADK Agent Configuration:
```
MCP_SERVER_URL=http://localhost:8080/mcp/
AI_MODEL=gemini-2.0-flash
AGENT_NAME=pega_adk_agent
```

## Usage

### MCP Server Features

The MCP server provides these tools:

- **Verify Connectivity** - Test connection to Pega Platform
- **Get Case Types** - List available case types
- **Create Case** - Create new cases with specified case type

### ADK Agent Features

The ADK agent can:

- Connect to Pega Platform via MCP tools
- List available case types
- Create new cases
- Provide natural language responses about case management

### Example Interactions

```
User: "List available case types"
Agent: "Found 3 case types:
  1. Home Loan Application (ID: H-28021)
  2. Credit Card Application (ID: C-15045)
  3. Personal Loan Request (ID: P-89012)"

User: "Create a home loan case"
Agent: "Case created successfully with ID: LOAN-2024-001"
```

## Project Structure

```
pega/
├── setup.py                 # Interactive setup script
├── README.md               # This file
├── pega-mcp/              # MCP Server
│   ├── server.py          # MCP server implementation
│   ├── tools.py           # Pega API tools
│   ├── resources.py       # MCP resources
│   ├── requirements.txt   # MCP dependencies
│   └── dx-apis/          # API documentation
└── pega-adk/             # ADK Agent
    ├── pega_adk_agent/
    │   └── agent.py      # ADK agent implementation
    └── requirements.txt   # ADK dependencies
```

## Troubleshooting

### Common Issues

1. **"Missing configuration" error**
   - Run `python setup.py` to create `.env` files
   - Ensure all required Pega credentials are provided

2. **Connection failed**
   - Verify your Pega Platform URL is correct
   - Check OAuth credentials are valid
   - Ensure network connectivity to Pega instance

3. **MCP server won't start**
   - Check port 8080 is available
   - Verify virtual environment is activated
   - Verify all dependencies are installed
   - Check `.env` file exists in `pega-mcp/` directory

4. **ADK agent can't connect**
   - Ensure MCP server is running on localhost:8080
   - Check MCP server URL in `pega-adk/.env`
   - Verify virtual environment is activated
   - Verify ADK dependencies are installed
   - Use `adk run pega_adk_agent` or `adk web` to start the agent

### Security Notes

- `.env` files are excluded from Git (see `.gitignore`)
- Never commit real credentials to version control
- Keep your OAuth credentials secure
- The setup script masks secret input for security

## Development

### Adding New Tools

To add new Pega API tools:

1. Add function to `pega-mcp/tools.py`
2. Register tool in `pega-mcp/server.py`
3. Update agent instructions in `pega-adk/pega_adk_agent/agent.py`

### Customizing the Agent

Edit `pega-adk/pega_adk_agent/agent.py` to:
- Change AI model
- Modify agent instructions
- Add custom tools
- Update agent behavior

### ADK Commands

- `adk run pega_adk_agent` - Start agent in terminal mode
- `adk web` - Start agent with web interface
- `adk --help` - Show all available commands

## License

This project is for educational and development purposes. Ensure compliance with your organization's policies when using with production Pega systems. 