#!/usr/bin/env python3
"""
Simple test script to check if the ChemBL MCP server is working correctly
by inspecting the available tools.
"""

import asyncio
import importlib
import inspect
import sys
from mcp_server import mcp, all_tools

def test_server_tools():
    """Test that all expected tools are available in the server."""
    server_name = mcp.name
    
    print(f"Server Name: {server_name}")
    print("\nRegistered Tools:")
    
    # List all available tools from the all_tools dictionary
    tool_count = len(all_tools)
    for tool_name, tool_func in all_tools.items():
        print(f"  - {tool_name}: {tool_func.__doc__ if tool_func.__doc__ else 'No description'}")
    
    print(f"\nTotal Tools: {tool_count}")
    
    # Check expected module availability
    expected_modules = [
        "molecules", 
        "targets", 
        "assays", 
        "activities", 
        "documents"
    ]
    
    print("\nModule Status:")
    for module_name in expected_modules:
        try:
            module = importlib.import_module(f"mcp_server.{module_name}")
            print(f"  - {module_name}: Available")
        except ImportError as e:
            print(f"  - {module_name}: Not available ({e})")
    
    return tool_count > 0

if __name__ == "__main__":
    success = test_server_tools()
    print(f"\nTest Result: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1) 