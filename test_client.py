from mcp.client import MCPClient

async def main():
    # Create a client connected to the server
    client = MCPClient(transport='stdio')
    await client.connect()

    try:
        # Test molecule search
        result = await client.call('search_molecule', {'query': 'aspirin', 'limit': 3})
        print("Search results for 'aspirin':")
        print(result)
        print("\n" + "="*50 + "\n")

        # Test molecule details
        result = await client.call('get_molecule_details', {'chembl_id': 'CHEMBL25'})
        print("Details for CHEMBL25:")
        print(result)

    finally:
        await client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 