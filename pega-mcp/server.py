#!/usr/bin/env python3
"""
MCP Pega Server - Simple async MCP server for Pega DX APIs

Usage: python server.py
"""

import asyncio
import logging
from typing import Dict, Any, List
from fastmcp import FastMCP

# Import business logic
from tools import config, verify_pega_connectivity, get_case_types, create_case

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# MCP Server
# ============================================================================

mcp = FastMCP("MCPPegaServer")

# ============================================================================
# MCP Tools
# ============================================================================

@mcp.tool()
async def verify_pega_connectivity_tool():
    """Verify connectivity to Pega Platform"""
    return await verify_pega_connectivity()

@mcp.tool()
async def get_case_types_tool():
    """Get available case types"""
    return await get_case_types()

@mcp.tool()
async def create_case_tool(case_type_id: str):
    """Create a new case"""
    return await create_case(case_type_id)

# ============================================================================
# MCP Resources
# ============================================================================

@mcp.resource("pega://case-types")
async def get_case_types_resource() -> str:
    """Get case types as a resource"""
    from resources import get_case_types_resource
    return await get_case_types_resource()

@mcp.resource("pega://connection-status")
async def get_connection_status() -> str:
    """Get connection status as a resource"""
    from resources import get_connection_status
    return await get_connection_status()

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Check configuration
    if not config.is_configured():
        logger.error("Missing configuration. Check your env file.")
        exit(1)
    
    logger.info(f"Starting MCP Pega Server for {config.BASE_URL}")
    
   
    asyncio.run(
        mcp.run_async(
            transport='streamable-http',
            host='0.0.0.0',
            port=8080
        )
    ) 