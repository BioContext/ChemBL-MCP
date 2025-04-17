"""
Tests for the ChEMBL MCP server implementation.
"""

import pytest
from chembl_mcp_server import (
    search_molecule,
    get_molecule_targets,
    get_molecule_details,
    get_molecule_sdf,
    get_similar_molecules,
    search_molecule_substructure,
    search_assays,
    get_assay_details,
    get_bioactivities,
    get_activity_details,
    search_targets,
    get_target_details,
    get_document_info,
    get_document_compounds
)

# Test molecules
TEST_MOLECULE_ID = "CHEMBL25"  # Aspirin
TEST_SIMILAR_MOLECULE_ID = "CHEMBL25"  # Aspirin
TEST_SUBSTRUCTURE_SMILES = "CC(=O)O"  # Acetic acid substructure
TEST_TARGET_ID = "CHEMBL1824"  # COX-2
TEST_ASSAY_ID = "CHEMBL1217645"  # COX-2 assay
TEST_ACTIVITY_ID = "1234"  # Example activity ID (numeric ID)
TEST_DOCUMENT_ID = "CHEMBL1121427"  # Example document ID

@pytest.mark.asyncio
async def test_search_molecule():
    """Test molecule search functionality."""
    result = await search_molecule("aspirin")
    assert "Molecule" in result
    assert "ChEMBL ID" in result
    assert "Formula" in result
    assert "Weight" in result

@pytest.mark.asyncio
async def test_get_molecule_targets():
    """Test getting molecule targets."""
    result = await get_molecule_targets(TEST_MOLECULE_ID)
    assert "Target" in result
    assert "ChEMBL ID" in result
    assert "Organism" in result
    assert "Activity" in result

@pytest.mark.asyncio
async def test_get_molecule_details():
    """Test getting molecule details."""
    result = await get_molecule_details(TEST_MOLECULE_ID)
    assert "Molecule Details" in result
    assert "Name" in result
    assert "Formula" in result
    assert "Molecular Weight" in result
    assert "LogP" in result

@pytest.mark.asyncio
async def test_get_molecule_sdf():
    """Test getting molecule SDF format."""
    result = await get_molecule_sdf(TEST_MOLECULE_ID)
    assert "V3000" in result or "V2000" in result  # SDF format markers
    assert "M  END" in result  # SDF end marker

@pytest.mark.asyncio
async def test_get_similar_molecules():
    """Test finding similar molecules."""
    result = await get_similar_molecules(TEST_SIMILAR_MOLECULE_ID)
    assert "Molecule" in result
    assert "ChEMBL ID" in result
    assert "Similarity" in result

@pytest.mark.asyncio
async def test_search_molecule_substructure():
    """Test substructure search."""
    result = await search_molecule_substructure(TEST_SUBSTRUCTURE_SMILES)
    assert "Molecule" in result
    assert "ChEMBL ID" in result
    assert "Formula" in result

@pytest.mark.asyncio
async def test_search_assays():
    """Test assay search."""
    result = await search_assays(assay_type="B", target_id=TEST_TARGET_ID)
    assert "Assay" in result
    assert "ChEMBL ID" in result
    assert "Type" in result
    assert "Target" in result

@pytest.mark.asyncio
async def test_get_assay_details():
    """Test getting assay details."""
    result = await get_assay_details(TEST_ASSAY_ID)
    assert "Assay Details" in result
    assert "Description" in result
    assert "Type" in result
    assert "Category" in result

@pytest.mark.asyncio
async def test_get_bioactivities():
    """Test getting bioactivity data."""
    result = await get_bioactivities(TEST_MOLECULE_ID, activity_type="IC50")
    assert "Activity Type" in result
    assert "Value" in result
    assert "Target" in result
    assert "Assay" in result

@pytest.mark.asyncio
async def test_get_activity_details():
    """Test getting activity details."""
    # First get an activity ID from our test molecule
    activities = await get_bioactivities(TEST_MOLECULE_ID)
    assert "Activity Type" in activities
    
    # Extract the activity ID from the response
    activity_id = activities.split("Activity ID: ")[1].split("\n")[0].strip()
    assert activity_id != "N/A"
    
    # Now test the activity details
    result = await get_activity_details(activity_id)
    assert "Activity Details" in result
    assert "Molecule" in result
    assert "Target" in result
    assert "Type" in result
    assert "Value" in result

@pytest.mark.asyncio
async def test_search_targets():
    """Test target search."""
    result = await search_targets(target_name="COX-2")
    assert "Target" in result
    assert "ChEMBL ID" in result
    assert "Type" in result
    assert "Organism" in result

@pytest.mark.asyncio
async def test_get_target_details():
    """Test getting target details."""
    result = await get_target_details(TEST_TARGET_ID)
    assert "Target Details" in result
    assert "Name" in result
    assert "Type" in result
    assert "Organism" in result
    assert "Target Components" in result

@pytest.mark.asyncio
async def test_get_document_info():
    """Test getting document information."""
    result = await get_document_info(TEST_DOCUMENT_ID)
    assert "Document Details" in result
    assert "Title" in result
    assert "Journal" in result
    assert "Year" in result

@pytest.mark.asyncio
async def test_get_document_compounds():
    """Test getting document compounds."""
    result = await get_document_compounds(TEST_DOCUMENT_ID)
    assert "Compound" in result
    assert "ChEMBL ID" in result
    assert "Formula" in result

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling for invalid inputs."""
    # Test invalid molecule ID
    result = await get_molecule_details("INVALID_ID")
    assert "No molecule found" in result or "Error" in result
    
    # Test invalid target ID
    result = await get_target_details("INVALID_ID")
    assert "No target found" in result or "Error" in result
    
    # Test invalid assay ID
    result = await get_assay_details("INVALID_ID")
    assert "No assay found" in result or "Error" in result

@pytest.mark.asyncio
async def test_pagination():
    """Test pagination in search functions."""
    # Test molecule search with different limits
    result_5 = await search_molecule("aspirin", limit=5)
    result_10 = await search_molecule("aspirin", limit=10)
    
    # Count the number of results
    count_5 = result_5.count("---")
    count_10 = result_10.count("---")
    
    assert count_5 <= 5
    assert count_10 <= 10
    assert count_10 >= count_5 