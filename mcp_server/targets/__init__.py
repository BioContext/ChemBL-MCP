"""
Target-related functions for ChEMBL MCP server.
"""

from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from ..utils import target_client, activity_client, format_target_info

# Reference to the MCP server instance, set when tools are registered
mcp = None

async def search_targets_impl(target_name: Optional[str] = None, uniprot_id: Optional[str] = None, limit: int = 5) -> str:
    """Implementation for searching targets."""
    try:
        filters = {}
        if target_name:
            filters['target_pref_name__icontains'] = target_name
        if uniprot_id:
            filters['target_components__accession'] = uniprot_id
            
        results = target_client.filter(**filters)
        
        if not results:
            return "No targets found matching the criteria."
            
        formatted_results = []
        for tgt in results[:limit]:
            formatted_results.append(format_target_info(tgt))
            
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error searching targets: {str(e)}"

async def get_target_details_impl(chembl_id: str) -> str:
    """Implementation for getting target details."""
    try:
        result = target_client.get(chembl_id)
        
        if not result:
            return f"No target found with ID {chembl_id}"
            
        # Get components information if available
        components = result.get('target_components', [])
        
        # Format the target details
        target_info = format_target_info(result)
        
        # Add component information if available
        if components:
            component_info = "\nComponents:\n"
            for i, comp in enumerate(components, 1):
                component_info += f"{i}. {comp.get('component_description', 'N/A')}"
                accession = comp.get('accession', None)
                if accession:
                    component_info += f" (UniProt: {accession})"
                component_info += "\n"
            target_info += component_info
        
        return f"Target Details:\n{target_info}"
    except Exception as e:
        return f"Error retrieving target details: {str(e)}"

async def get_molecule_targets_impl(chembl_id: str) -> str:
    """Implementation for getting molecule targets."""
    try:
        results = activity_client.filter(molecule_chembl_id=chembl_id)
        
        if not results:
            return f"No target information found for molecule {chembl_id}"
            
        targets = {}
        for res in results:
            target_id = res.get('target_chembl_id')
            if target_id and target_id not in targets:
                targets[target_id] = {
                    'name': res.get('target_pref_name', 'N/A'),
                    'organism': res.get('target_organism', 'N/A'),
                    'activity_type': res.get('standard_type', 'N/A'),
                    'activity_value': f"{res.get('standard_value', 'N/A')} {res.get('standard_units', '')}"
                }
                
        if not targets:
            return f"No target information found for molecule {chembl_id}"
            
        formatted_results = []
        for target_id, info in list(targets.items())[:5]:  # Limit to 5 targets
            target_info = f"""
Target: {info['name']}
ChEMBL ID: {target_id}
Organism: {info['organism']}
Activity: {info['activity_type']} = {info['activity_value']}
"""
            formatted_results.append(target_info)
            
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error retrieving target information: {str(e)}"

def register_target_tools(mcp_instance: FastMCP):
    """Register all target-related tools with the MCP server."""
    global mcp
    mcp = mcp_instance
    
    @mcp.tool()
    async def search_targets(target_name: Optional[str] = None, uniprot_id: Optional[str] = None, limit: int = 5) -> str:
        """Search for targets in ChEMBL database.
        
        Args:
            target_name: Name of the target (optional)
            uniprot_id: UniProt accession ID (optional)
            limit: Maximum number of results to return
        """
        return await search_targets_impl(target_name, uniprot_id, limit)
    
    @mcp.tool()
    async def get_target_details(chembl_id: str) -> str:
        """Get detailed information about a target by its ChEMBL ID.
        
        Args:
            chembl_id: ChEMBL ID of the target
        """
        return await get_target_details_impl(chembl_id)
    
    @mcp.tool()
    async def get_molecule_targets(chembl_id: str) -> str:
        """Get known targets for a molecule by its ChEMBL ID.
        
        Args:
            chembl_id: ChEMBL ID of the molecule (e.g., 'CHEMBL25')
        """
        return await get_molecule_targets_impl(chembl_id)
    
    return {
        "search_targets": search_targets,
        "get_target_details": get_target_details,
        "get_molecule_targets": get_molecule_targets,
    } 