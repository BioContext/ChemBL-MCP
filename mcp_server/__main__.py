"""
Main entry point for the ChEMBL MCP server.
"""

from . import mcp

def run_server():
    """Entry point for running the ChEMBL MCP server."""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # Run the MCP server
    run_server() 