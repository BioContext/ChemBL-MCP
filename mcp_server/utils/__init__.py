"""
Utility functions for ChEMBL MCP server.
"""

from typing import Dict, Any, List, Optional
from chembl_webresource_client.new_client import new_client

# Base URL for ChEMBL API
BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

def format_response(title: str, data: List[str], show_count: bool = False) -> str:
    """Format a list of data items into a readable text response.
    
    Args:
        title: Title for the response
        data: List of data items to format
        show_count: Whether to show the count of items
    
    Returns:
        Formatted text response
    """
    result = f"{title}\n"
    
    for i, item in enumerate(data, 1):
        result += f"{i}. {item}\n"
    
    if show_count:
        result += f"\nTotal items: {len(data)}"
    
    return result

def format_molecule_info(molecule: Dict[str, Any]) -> str:
    """Format molecule information into a readable text.
    
    Args:
        molecule: Dictionary containing molecule information
        
    Returns:
        Formatted molecule information
    """
    properties = molecule.get('molecule_properties', {})
    return f"""
Molecule: {molecule.get('pref_name', 'N/A')}
ChEMBL ID: {molecule.get('molecule_chembl_id', 'N/A')}
Formula: {properties.get('full_molformula', 'N/A')}
Weight: {properties.get('full_mwt', 'N/A')}
LogP: {properties.get('alogp', 'N/A')}
HBA: {properties.get('hba', 'N/A')}
HBD: {properties.get('hbd', 'N/A')}
PSA: {properties.get('psa', 'N/A')}
Rule of 5 Violations: {properties.get('num_ro5_violations', 'N/A')}
Aromatic Rings: {properties.get('aromatic_rings', 'N/A')}
"""

def format_target_info(target: Dict[str, Any]) -> str:
    """Format target information into a readable text.
    
    Args:
        target: Dictionary containing target information
        
    Returns:
        Formatted target information
    """
    return f"""
Target: {target.get('target_pref_name', 'N/A')}
ChEMBL ID: {target.get('target_chembl_id', 'N/A')}
Type: {target.get('target_type', 'N/A')}
Organism: {target.get('target_organism', 'N/A')}
"""

def format_assay_info(assay: Dict[str, Any]) -> str:
    """Format assay information into a readable text.
    
    Args:
        assay: Dictionary containing assay information
        
    Returns:
        Formatted assay information
    """
    return f"""
Assay: {assay.get('assay_description', 'N/A')}
ChEMBL ID: {assay.get('assay_chembl_id', 'N/A')}
Type: {assay.get('assay_type', 'N/A')}
Target: {assay.get('target_pref_name', 'N/A')}
"""

def format_activity_info(activity: Dict[str, Any]) -> str:
    """Format activity information into a readable text.
    
    Args:
        activity: Dictionary containing activity information
        
    Returns:
        Formatted activity information
    """
    return f"""
Activity Type: {activity.get('standard_type', 'N/A')}
Value: {activity.get('standard_value', 'N/A')} {activity.get('standard_units', '')}
Target: {activity.get('target_pref_name', 'N/A')}
Assay: {activity.get('assay_description', 'N/A')}
Relation: {activity.get('standard_relation', 'N/A')}
Activity ID: {activity.get('activity_id', 'N/A')}
"""

# Create client instances
molecule_client = new_client.molecule
target_client = new_client.target
assay_client = new_client.assay
activity_client = new_client.activity
document_client = new_client.document

# Set JSON as default format
molecule_client.set_format('json')
target_client.set_format('json')
assay_client.set_format('json')
activity_client.set_format('json')
document_client.set_format('json') 