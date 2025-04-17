"""
Activity-related functions for ChEMBL MCP server.
"""

from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from ..utils import activity_client, format_activity_info

# Reference to the MCP server instance, set when tools are registered
mcp = None

async def get_bioactivities_impl(chembl_id: str, activity_type: Optional[str] = None) -> str:
    """Implementation for getting bioactivities."""
    try:
        filters = {'molecule_chembl_id': chembl_id}
        if activity_type:
            filters['standard_type'] = activity_type
            
        results = activity_client.filter(**filters)
        
        if not results:
            return f"No bioactivity data found for molecule {chembl_id}"
            
        formatted_results = []
        for act in results[:5]:  # Limit to 5 results
            formatted_results.append(format_activity_info(act))
            
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error retrieving bioactivity data: {str(e)}"

async def get_activity_details_impl(activity_id: str) -> str:
    """Implementation for getting activity details."""
    try:
        if not activity_id.isdigit():
            return f"Invalid activity ID format. Expected a number, got '{activity_id}'"
            
        # Filter by activity_id
        results = activity_client.filter(activity_id=activity_id)
        
        if not results:
            return f"No activity found with ID {activity_id}"
            
        # Get the first matching activity
        result = results[0]
            
        activity_info = f"""
Activity Details:
Activity ID: {result.get('activity_id', 'N/A')}
Type: {result.get('standard_type', 'N/A')}
Value: {result.get('standard_value', 'N/A')} {result.get('standard_units', '')}
Relation: {result.get('standard_relation', 'N/A')}
Target: {result.get('target_pref_name', 'N/A')} ({result.get('target_chembl_id', 'N/A')})
Molecule: {result.get('molecule_pref_name', 'N/A')} ({result.get('molecule_chembl_id', 'N/A')})
Assay: {result.get('assay_description', 'N/A')} ({result.get('assay_chembl_id', 'N/A')})
Document: {result.get('document_chembl_id', 'N/A')}
"""
        
        return activity_info
    except Exception as e:
        return f"Error retrieving activity details: {str(e)}"

def register_activity_tools(mcp_instance: FastMCP):
    """Register all activity-related tools with the MCP server."""
    global mcp
    mcp = mcp_instance
    
    @mcp.tool()
    async def get_bioactivities(chembl_id: str, activity_type: Optional[str] = None) -> str:
        """Get bioactivity data for a molecule.
        
        Args:
            chembl_id: ChEMBL ID of the molecule
            activity_type: Type of activity (e.g., 'IC50', 'Ki')
        """
        return await get_bioactivities_impl(chembl_id, activity_type)
    
    @mcp.tool()
    async def get_activity_details(activity_id: str) -> str:
        """Get detailed information about an activity by its ID.
        
        Args:
            activity_id: Activity ID
        """
        return await get_activity_details_impl(activity_id)
    
    return {
        "get_bioactivities": get_bioactivities,
        "get_activity_details": get_activity_details,
    } 