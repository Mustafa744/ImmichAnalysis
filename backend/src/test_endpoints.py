import httpx
import asyncio
import json


async def test_endpoints():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/api/v1") as client:
        print("--- Testing Daily Timeline ---")
        res = await client.get("/timeline/daily")
        data = res.json()
        print(f"Daily timeline length (should be contiguous): {len(data)}")
        if len(data) > 0:
            print(f"Sample dict keys: {data[0].keys()}")

        print("\n--- Testing Moments Insights ---")
        res = await client.get("/insights/moments")
        data = res.json()
        print(f"Moments keys: {data.keys()}")
        if "golden_hour" in data:
            print(f"Golden hour subkeys: {data['golden_hour'].keys()}")

        print("\n--- Testing Color Histograms ---")
        res = await client.get("/colors/histograms")
        data = res.json()
        print(f"Result keys: {data.keys()}")
        print(f"r_hist len: {len(data.get('r_hist', []))} (should be 32)")

        print("\n--- Testing Top Locations ---")
        res = await client.get("/insights/top-locations")
        data = res.json()
        print(f"Length: {len(data)}")
        if len(data) > 0:
            print(f"First cluster keys: {data[0].keys()}")


if __name__ == "__main__":
    asyncio.run(test_endpoints())
