"""
Main entry point for the ChEMBL MCP server.
"""

from . import mcp

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport='stdio') 