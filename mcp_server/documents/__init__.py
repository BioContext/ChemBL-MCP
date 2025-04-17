"""
Document-related functions for ChEMBL MCP server.
"""

from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from ..utils import document_client, molecule_client

# Reference to the MCP server instance, set when tools are registered
mcp = None

async def get_document_info_impl(chembl_id: str) -> str:
    """Implementation for getting document information."""
    try:
        result = document_client.get(chembl_id)
        
        if not result:
            return f"No document found with ID {chembl_id}"
            
        return f"""
Document Details:
Title: {result.get('title', 'N/A')}
ChEMBL ID: {result.get('document_chembl_id', 'N/A')}
Journal: {result.get('journal', 'N/A')}
Year: {result.get('year', 'N/A')}
Authors: {result.get('authors', 'N/A')}
DOI: {result.get('doi', 'N/A')}
PubMed ID: {result.get('pubmed_id', 'N/A')}
"""
    except Exception as e:
        return f"Error retrieving document information: {str(e)}"

async def get_document_compounds_impl(chembl_id: str, limit: int = 5) -> str:
    """Implementation for getting document compounds."""
    try:
        # Filter molecules by document_chembl_id
        results = molecule_client.filter(document_chembl_id=chembl_id)
        
        if not results:
            return f"No compounds found for document {chembl_id}"
            
        formatted_results = []
        for i, mol in enumerate(results[:limit], 1):
            mol_id = mol.get('molecule_chembl_id', 'N/A')
            name = mol.get('pref_name', 'N/A')
            formula = mol.get('molecule_properties', {}).get('full_molformula', 'N/A')
            
            compound_info = f"{i}. {name} ({mol_id}) - {formula}"
            formatted_results.append(compound_info)
            
        return f"Compounds in document {chembl_id}:\n\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"Error retrieving document compounds: {str(e)}"

def register_document_tools(mcp_instance: FastMCP):
    """Register all document-related tools with the MCP server."""
    global mcp
    mcp = mcp_instance
    
    @mcp.tool()
    async def get_document_info(chembl_id: str) -> str:
        """Get information about a document in ChEMBL database.
        
        Args:
            chembl_id: ChEMBL ID of the document
        """
        return await get_document_info_impl(chembl_id)
    
    @mcp.tool()
    async def get_document_compounds(chembl_id: str, limit: int = 5) -> str:
        """Get compounds mentioned in a document.
        
        Args:
            chembl_id: ChEMBL ID of the document
            limit: Maximum number of compounds to return
        """
        return await get_document_compounds_impl(chembl_id, limit)
    
    return {
        "get_document_info": get_document_info,
        "get_document_compounds": get_document_compounds,
    } 