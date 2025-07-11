"""
Pega API Tools - Business Logic Functions
"""

import os
import httpx
import logging
import time
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration
# ============================================================================

class Config:
    """Simple configuration class"""
    BASE_URL = os.getenv("PEGA_BASE_URL", "")
    CLIENT_ID = os.getenv("PEGA_CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("PEGA_CLIENT_SECRET", "")
    APP_ALIAS = os.getenv("APP_ALIAS", "")
    API_BASE_PATH = os.getenv("API_BASE_PATH", "/prweb/app/{app_alias}/api/application/v2")
    OAUTH2_TOKEN_URL = os.getenv("OAUTH2_TOKEN_URL", "/prweb/PRRestService/oauth2/v1/token")
    VERIFY_SSL = os.getenv("VERIFY_SSL", "true").lower() == "true"
    MAX_CONNECTIONS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    @property
    def token_url(self) -> str:
        return f"{self.BASE_URL}{self.OAUTH2_TOKEN_URL}"
    
    @property
    def api_url(self) -> str:
        api_path = self.API_BASE_PATH.replace("{app_alias}", self.APP_ALIAS)
        return f"{self.BASE_URL}{api_path}"
    
    def is_configured(self) -> bool:
        return bool(self.BASE_URL and self.CLIENT_ID and self.CLIENT_SECRET and self.APP_ALIAS)

config = Config()

# ============================================================================
# OAuth Token Management
# ============================================================================

# Global token cache
_access_token: Optional[str] = None
_token_expires_at: float = 0

async def get_pega_auth_headers() -> Dict[str, str]:
    """Get authenticated headers - reuses cached token"""
    global _access_token, _token_expires_at
    
    # Check if token is still valid (with 60s buffer)
    if _access_token and time.time() < _token_expires_at - 60:
        return {
            "Authorization": f"Bearer {_access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    # Re-authenticate when needed
    async with httpx.AsyncClient() as client:
        response = await client.post(
            config.token_url,
            data={
                'grant_type': 'client_credentials',
                'client_id': config.CLIENT_ID,
                'client_secret': config.CLIENT_SECRET
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            _access_token = token_data.get('access_token')
            _token_expires_at = time.time() + token_data.get('expires_in', 3600)
            logger.info("Authentication successful")
            return {
                "Authorization": f"Bearer {_access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        else:
            logger.error(f"Authentication failed: {response.status_code}")
            raise Exception(f"Authentication failed: {response.status_code}")

# ============================================================================
# Business Logic Functions (ServiceNow Style)
# ============================================================================

async def verify_pega_connectivity() -> str:
    """Verify connectivity to Pega Platform"""
    url = f"{config.api_url}/casetypes"
    
    try:
        headers = await get_pega_auth_headers()
        
        async with httpx.AsyncClient() as client:
            start_time = time.time()
            response = await client.get(url, headers=headers)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                output = f"Connected to Pega successfully in {response_time:.1f}ms"
            else:
                output = f"Connection failed: {response.status_code}"
            
            return output
            
    except Exception as e:
        logger.error(f"Connectivity error: {e}")
        return f"Connection error: {str(e)}"

async def get_case_types() -> str:
    """Get available case types"""
    url = f"{config.api_url}/casetypes"
    
    try:
        headers = await get_pega_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                case_types = data.get('caseTypes', [])
                
                if case_types:
                    output = f"Found {len(case_types)} case types:\n"
                    for i, ct in enumerate(case_types, 1):
                        name = ct.get('name', 'Unknown')
                        case_id = ct.get('ID', ct.get('id', 'No ID'))
                        output += f"  {i}. {name} (ID: {case_id})\n"
                else:
                    output = "No case types found"
            else:
                output = f"Failed to get case types: {response.status_code}"
            
            return output
            
    except Exception as e:
        logger.error(f"Error getting case types: {e}")
        return f"Error getting case types: {str(e)}"

async def create_case(case_type_id: str) -> str:
    """Create a new case"""
    url = f"{config.api_url}/cases"
    payload = {"caseTypeID": case_type_id}
    
    try:
        headers = await get_pega_auth_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code in [200, 201]:
                data = response.json()
                case_id = data.get('ID', data.get('id', 'Unknown'))
                output = f"Case created successfully with ID: {case_id}"
            else:
                output = f"Failed to create case: {response.status_code}"
            
            return output
            
    except Exception as e:
        logger.error(f"Error creating case: {e}")
        return f"Error creating case: {str(e)}" 