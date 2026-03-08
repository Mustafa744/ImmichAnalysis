import httpx
from PIL import Image
from io import BytesIO
from tqdm import tqdm


class ImmichClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 3):
        self.base_url = base_url.rstrip("/")
        self.headers  = {"x-api-key": api_key}
        self.timeout  = timeout

    def get_thumbnail(self, asset_id: str, size: str = "preview") -> Image.Image | None:
        try:
            r = httpx.get(
                f"{self.base_url}/api/assets/{asset_id}/thumbnail",
                headers=self.headers,
                params={"size": size},
                timeout=self.timeout,
            )
            r.raise_for_status()
            return Image.open(BytesIO(r.content)).convert("RGB")
        except httpx.TimeoutException:
            tqdm.write(f"  [TIMEOUT]  {asset_id}")
        except httpx.HTTPStatusError as e:
            tqdm.write(f"  [HTTP {e.response.status_code}] {asset_id}")
        except Exception as e:
            tqdm.write(f"  [ERROR]    {asset_id}: {e}")
        return None

    def get_all_assets(self) -> list[dict]:
        """Fetch full asset list from Immich."""
        r = httpx.get(
            f"{self.base_url}/api/assets",
            headers=self.headers,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
