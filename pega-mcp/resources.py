"""
MCP Resources for Pega Server
"""

import time
import httpx
from tools import config, get_pega_auth_headers

async def get_case_types_resource() -> str:
    """Get case types as a resource"""
    url = f"{config.api_url}/casetypes"
    
    try:
        headers = await get_pega_auth_headers()
        
        async with httpx.AsyncClient(verify=config.VERIFY_SSL) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                case_types = data.get('caseTypes', [])
                
                if case_types:
                    result = "Available Case Types:\n"
                    for ct in case_types:
                        name = ct.get('name', 'Unknown')
                        case_id = ct.get('ID', ct.get('id', 'No ID'))
                        result += f"- {name} ({case_id})\n"
                else:
                    result = "No case types available"
            else:
                result = f"Failed to get case types: {response.status_code}"
            
            return result
            
    except Exception as e:
        return f"Error getting case types: {str(e)}"

async def get_connection_status() -> str:
    """Get connection status as a resource"""
    url = f"{config.api_url}/casetypes"
    
    try:
        headers = await get_pega_auth_headers()
        
        async with httpx.AsyncClient(verify=config.VERIFY_SSL) as client:
            start_time = time.time()
            response = await client.get(url, headers=headers)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                return f"""Connected to Pega
Response Time: {response_time:.1f}ms
Status: Ready for requests"""
            else:
                return f"""Connection Error
Error: HTTP {response.status_code}
Status: Check configuration"""
                
    except Exception as e:
        return f"""Connection Error
Error: {str(e)}
Status: Check configuration""" 