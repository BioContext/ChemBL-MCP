"""
Assay-related functions for ChEMBL MCP server.
"""

from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from ..utils import assay_client, format_assay_info

# Reference to the MCP server instance, set when tools are registered
mcp = None

async def search_assays_impl(assay_type: Optional[str] = None, target_id: Optional[str] = None) -> str:
    """Implementation for searching assays."""
    try:
        filters = {}
        if assay_type:
            filters['assay_type'] = assay_type
        if target_id:
            filters['target_chembl_id'] = target_id
            
        results = assay_client.filter(**filters)
        
        if not results:
            return "No assays found matching the criteria."
            
        formatted_results = []
        for assay in results[:5]:  # Limit to 5 results
            formatted_results.append(format_assay_info(assay))
            
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error searching assays: {str(e)}"

async def get_assay_details_impl(chembl_id: str) -> str:
    """Implementation for getting assay details."""
    try:
        result = assay_client.get(chembl_id)
        
        if not result:
            return f"No assay found with ID {chembl_id}"
            
        # Get basic assay information
        assay_info = f"""
Assay Details:
ChEMBL ID: {result.get('assay_chembl_id', 'N/A')}
Description: {result.get('description', 'N/A')}
Assay Type: {result.get('assay_type', 'N/A')}
Assay Organism: {result.get('assay_organism', 'N/A')}
Target ChEMBL ID: {result.get('target_chembl_id', 'N/A')}
Target Name: {result.get('target_pref_name', 'N/A')}
Document ChEMBL ID: {result.get('document_chembl_id', 'N/A')}
"""
        
        return assay_info
    except Exception as e:
        return f"Error retrieving assay details: {str(e)}"

def register_assay_tools(mcp_instance: FastMCP):
    """Register all assay-related tools with the MCP server."""
    global mcp
    mcp = mcp_instance
    
    @mcp.tool()
    async def search_assays(assay_type: Optional[str] = None, target_id: Optional[str] = None) -> str:
        """Search for assays in ChEMBL database.
        
        Args:
            assay_type: Type of assay (e.g., 'B' for biochemical, 'F' for functional)
            target_id: ChEMBL ID of the target (optional)
        """
        return await search_assays_impl(assay_type, target_id)
    
    @mcp.tool()
    async def get_assay_details(chembl_id: str) -> str:
        """Get detailed information about an assay by its ChEMBL ID.
        
        Args:
            chembl_id: ChEMBL ID of the assay
        """
        return await get_assay_details_impl(chembl_id)
    
    return {
        "search_assays": search_assays,
        "get_assay_details": get_assay_details,
    } 