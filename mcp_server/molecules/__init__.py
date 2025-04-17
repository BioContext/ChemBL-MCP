"""
Molecule-related functions for ChEMBL MCP server.
"""

from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from ..utils import molecule_client, format_molecule_info

# Reference to the MCP server instance, set when tools are registered
mcp = None

async def search_molecule_impl(query: str, limit: int = 5) -> str:
    """Implementation for searching molecules in ChEMBL database."""
    try:
        results = molecule_client.search(query)
        
        if not results:
            return "No molecules found matching the query."
            
        formatted_results = []
        for mol in results[:limit]:
            formatted_results.append(format_molecule_info(mol))
            
        return "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error searching molecules: {str(e)}"

async def get_molecule_details_impl(chembl_id: str) -> str:
    """Implementation for getting molecule details."""
    try:
        result = molecule_client.get(chembl_id)
        
        if not result:
            return f"No molecule found with ID {chembl_id}"
            
        return format_molecule_info(result)
    except Exception as e:
        return f"Error retrieving molecule details: {str(e)}"

async def get_molecule_sdf_impl(chembl_id: str) -> str:
    """Implementation for getting molecule SDF."""
    try:
        molecule_client.set_format('sdf')
        result = molecule_client.get(chembl_id)
        molecule_client.set_format('json')  # Reset to JSON format
        
        if not result:
            return f"No SDF data found for molecule {chembl_id}"
            
        return f"SDF data for {chembl_id}:\n\n{result}"
    except Exception as e:
        return f"Error retrieving SDF data: {str(e)}"

async def get_similar_molecules_impl(chembl_id: str, similarity_threshold: float = 0.7) -> str:
    """Implementation for getting similar molecules."""
    try:
        results = molecule_client.filter(similarity=chembl_id).filter(similarity_threshold=similarity_threshold)
        
        if not results:
            return f"No similar molecules found for {chembl_id} at threshold {similarity_threshold}"
            
        formatted_results = []
        for mol in results[:5]:  # Limit to 5 results
            formatted_results.append(format_molecule_info(mol))
            
        return f"Similar molecules to {chembl_id} (threshold: {similarity_threshold}):\n\n" + "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error finding similar molecules: {str(e)}"

async def search_molecule_substructure_impl(smiles: str) -> str:
    """Implementation for searching molecules by substructure."""
    try:
        results = molecule_client.filter(substructure=smiles)
        
        if not results:
            return f"No molecules found containing substructure {smiles}"
            
        formatted_results = []
        for mol in results[:5]:  # Limit to 5 results
            formatted_results.append(format_molecule_info(mol))
            
        return f"Molecules containing substructure {smiles}:\n\n" + "\n---\n".join(formatted_results)
    except Exception as e:
        return f"Error searching by substructure: {str(e)}"

def register_molecule_tools(mcp_instance: FastMCP):
    """Register all molecule-related tools with the MCP server."""
    global mcp
    mcp = mcp_instance
    
    @mcp.tool()
    async def search_molecule(query: str, limit: int = 5) -> str:
        """Search for molecules in ChEMBL database.
        
        Args:
            query: Search query string (e.g., 'aspirin', 'CHEMBL25')
            limit: Maximum number of results to return
        """
        return await search_molecule_impl(query, limit)
    
    @mcp.tool()
    async def get_molecule_details(chembl_id: str) -> str:
        """Get detailed information about a molecule by its ChEMBL ID.
        
        Args:
            chembl_id: ChEMBL ID of the molecule (e.g., 'CHEMBL25')
        """
        return await get_molecule_details_impl(chembl_id)
    
    @mcp.tool()
    async def get_molecule_sdf(chembl_id: str) -> str:
        """Get SDF (Structure Data File) for a molecule.
        
        Args:
            chembl_id: ChEMBL ID of the molecule
        """
        return await get_molecule_sdf_impl(chembl_id)
    
    @mcp.tool()
    async def get_similar_molecules(chembl_id: str, similarity_threshold: float = 0.7) -> str:
        """Get molecules similar to a reference molecule.
        
        Args:
            chembl_id: ChEMBL ID of the reference molecule
            similarity_threshold: Similarity threshold (0.0 to 1.0)
        """
        return await get_similar_molecules_impl(chembl_id, similarity_threshold)
    
    @mcp.tool()
    async def search_molecule_substructure(smiles: str) -> str:
        """Search for molecules containing a specific substructure.
        
        Args:
            smiles: SMILES notation of the substructure to search for
        """
        return await search_molecule_substructure_impl(smiles)
    
    return {
        "search_molecule": search_molecule,
        "get_molecule_details": get_molecule_details,
        "get_molecule_sdf": get_molecule_sdf,
        "get_similar_molecules": get_similar_molecules,
        "search_molecule_substructure": search_molecule_substructure
    } 