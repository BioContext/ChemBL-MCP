"""
MCP Server implementation for ChEMBL using chembl_webresource_client.
"""

from typing import Any, List, Dict, Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with proper configuration
mcp = FastMCP(
    name="chembl",
    description="MCP server for accessing ChEMBL database",
    version="0.1.0"
)

# Import module registration functions
from .molecules import register_molecule_tools
from .targets import register_target_tools
from .assays import register_assay_tools
from .activities import register_activity_tools
from .documents import register_document_tools

# Register all tools with the MCP server
molecule_tools = register_molecule_tools(mcp)
target_tools = register_target_tools(mcp)
assay_tools = register_assay_tools(mcp)
activity_tools = register_activity_tools(mcp)
document_tools = register_document_tools(mcp)

# Combine all tools for reference
all_tools = {
    **molecule_tools,
    **target_tools,
    **assay_tools,
    **activity_tools,
    **document_tools,
}

# Re-export all tool functions for backward compatibility
from .molecules import search_molecule_impl as search_molecule
from .molecules import get_molecule_details_impl as get_molecule_details
from .molecules import get_molecule_sdf_impl as get_molecule_sdf
from .molecules import get_similar_molecules_impl as get_similar_molecules
from .molecules import search_molecule_substructure_impl as search_molecule_substructure
from .targets import search_targets_impl as search_targets
from .targets import get_target_details_impl as get_target_details
from .targets import get_molecule_targets_impl as get_molecule_targets
from .assays import search_assays_impl as search_assays
from .assays import get_assay_details_impl as get_assay_details
from .activities import get_bioactivities_impl as get_bioactivities
from .activities import get_activity_details_impl as get_activity_details
from .documents import get_document_info_impl as get_document_info
from .documents import get_document_compounds_impl as get_document_compounds

# Main entry point for running the server directly
if __name__ == "__main__":
    mcp.run(transport='stdio') 