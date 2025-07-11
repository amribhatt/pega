#!/usr/bin/env python3
"""
Test script for Pega MCP Server Tools and Resources
Tests all tools and resources individually with detailed output
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import the tools and resources
from tools import verify_pega_connectivity, get_case_types, create_case, config
from resources import get_case_types_resource, get_connection_status

class TestResult:
    def __init__(self, name, success, message, details=None, raw_response=None):
        self.name = name
        self.success = success
        self.message = message
        self.details = details or ""
        self.raw_response = raw_response or ""

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")

def print_test_result(result):
    status = "PASS" if result.success else "FAIL"
    print(f"{status}: {result.name}")
    print(f"Message: {result.message}")
    if result.details:
        print(f"Details: {result.details}")
    
    # Always print raw response for debugging
    if hasattr(result, 'raw_response'):
        print(f"Raw Response: {result.raw_response}")
    
    print("-" * 40)

async def test_configuration():
    """Test configuration setup"""
    print_test_header("Configuration")
    
    # Check if configuration is valid
    if not config.is_configured():
        config_status = f"Missing required values. BASE_URL: {bool(config.BASE_URL)}, CLIENT_ID: {bool(config.CLIENT_ID)}, CLIENT_SECRET: {bool(config.CLIENT_SECRET)}, APP_ALIAS: {bool(config.APP_ALIAS)}"
        return TestResult(
            "Configuration",
            False,
            "Configuration is incomplete",
            config_status,
            f"Configuration Status: {config_status}"
        )
    
    config_info = f"BASE_URL: {config.BASE_URL}, APP_ALIAS: {config.APP_ALIAS}"
    return TestResult(
        "Configuration",
        True,
        "Configuration is valid",
        config_info,
        f"Configuration Info: {config_info}"
    )

async def test_connectivity():
    """Test Pega connectivity"""
    print_test_header("Pega Connectivity")
    
    try:
        result = await verify_pega_connectivity()
        
        if "successfully" in result.lower():
            return TestResult(
                "Connectivity",
                True,
                "Successfully connected to Pega Platform",
                result,
                f"Raw Connectivity Response: {result}"
            )
        else:
            return TestResult(
                "Connectivity",
                False,
                "Failed to connect to Pega Platform",
                result,
                f"Raw Connectivity Error: {result}"
            )
    except Exception as e:
        return TestResult(
            "Connectivity",
            False,
            f"Connectivity test failed with exception",
            str(e),
            f"Raw Exception: {str(e)}"
        )

async def test_get_case_types():
    """Test getting case types"""
    print_test_header("Get Case Types")
    
    try:
        result = await get_case_types()
        
        if "Found" in result and "case types" in result:
            return TestResult(
                "Get Case Types",
                True,
                "Successfully retrieved case types",
                result,
                f"Raw Case Types Response: {result}"
            )
        elif "No case types found" in result:
            return TestResult(
                "Get Case Types",
                True,
                "No case types found (this might be expected)",
                result,
                f"Raw Case Types Response: {result}"
            )
        else:
            return TestResult(
                "Get Case Types",
                False,
                "Failed to get case types",
                result,
                f"Raw Case Types Error: {result}"
            )
    except Exception as e:
        return TestResult(
            "Get Case Types",
            False,
            f"Get case types failed with exception",
            str(e),
            f"Raw Exception: {str(e)}"
        )

async def test_create_case():
    """Test case creation with a sample case type"""
    print_test_header("Create Case")
    
    try:
        # First get case types to find a valid one
        case_types_result = await get_case_types()
        
        if "Found" in case_types_result and "case types" in case_types_result:
            # Extract first case type ID from the result
            lines = case_types_result.split('\n')
            case_type_id = None
            
            for line in lines:
                if '(ID:' in line:
                    case_type_id = line.split('(ID:')[1].split(')')[0].strip()
                    break
            
            if case_type_id:
                result = await create_case(case_type_id)
                
                if "created successfully" in result.lower():
                    return TestResult(
                        "Create Case",
                        True,
                        "Successfully created a case",
                        result,
                        f"Raw Create Case Response: {result}"
                    )
                else:
                    return TestResult(
                        "Create Case",
                        False,
                        "Failed to create case",
                        result,
                        f"Raw Create Case Error: {result}"
                    )
            else:
                return TestResult(
                    "Create Case",
                    False,
                    "Could not extract case type ID from case types result",
                    case_types_result,
                    f"Raw Case Types Result: {case_types_result}"
                )
        else:
            return TestResult(
                "Create Case",
                False,
                "Cannot test case creation without available case types",
                case_types_result,
                f"Raw Case Types Result: {case_types_result}"
            )
    except Exception as e:
        return TestResult(
            "Create Case",
            False,
            f"Create case failed with exception",
            str(e),
            f"Raw Exception: {str(e)}"
        )

async def test_case_types_resource():
    """Test case types resource"""
    print_test_header("Case Types Resource")
    
    try:
        result = await get_case_types_resource()
        
        if result and len(result) > 0:
            return TestResult(
                "Case Types Resource",
                True,
                "Successfully retrieved case types resource",
                f"Resource length: {len(result)} characters",
                f"Raw Resource Response: {result}"
            )
        else:
            return TestResult(
                "Case Types Resource",
                False,
                "Case types resource returned empty or invalid data",
                result,
                f"Raw Resource Error: {result}"
            )
    except Exception as e:
        return TestResult(
            "Case Types Resource",
            False,
            f"Case types resource failed with exception",
            str(e),
            f"Raw Exception: {str(e)}"
        )

async def test_connection_status_resource():
    """Test connection status resource"""
    print_test_header("Connection Status Resource")
    
    try:
        result = await get_connection_status()
        
        if result and len(result) > 0:
            return TestResult(
                "Connection Status Resource",
                True,
                "Successfully retrieved connection status resource",
                f"Resource length: {len(result)} characters",
                f"Raw Resource Response: {result}"
            )
        else:
            return TestResult(
                "Connection Status Resource",
                False,
                "Connection status resource returned empty or invalid data",
                result,
                f"Raw Resource Error: {result}"
            )
    except Exception as e:
        return TestResult(
            "Connection Status Resource",
            False,
            f"Connection status resource failed with exception",
            str(e),
            f"Raw Exception: {str(e)}"
        )

async def run_all_tests():
    """Run all tests and return results"""
    print("Pega MCP Server - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_configuration,
        test_connectivity,
        test_get_case_types,
        test_create_case,
        test_case_types_resource,
        test_connection_status_resource
    ]
    
    results = []
    
    for test in tests:
        try:
            result = await test()
            results.append(result)
            print_test_result(result)
        except Exception as e:
            error_result = TestResult(
                test.__name__,
                False,
                f"Test failed with unexpected exception",
                str(e),
                f"Raw Exception: {str(e)}"
            )
            results.append(error_result)
            print_test_result(error_result)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in results if r.success)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\nAll tests passed!")
    else:
        print(f"\n{total - passed} test(s) failed. Check the details above.")
    
    return results

def main():
    """Main function to run tests"""
    try:
        # Check if .env exists
        env_file = Path(".env")
        if not env_file.exists():
            print("Error: .env file not found!")
            print("Please copy env.template to .env and configure your Pega credentials.")
            sys.exit(1)
        
        # Run tests
        results = asyncio.run(run_all_tests())
        
        # Exit with error code if any tests failed
        if not all(r.success for r in results):
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test suite failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 