import os
import pandas as pd


class ThumbnailCache:
    def __init__(self, path: str):
        self.path = path
        self.data: dict = {}
        
        # Load from parquet if exists
        if os.path.exists(self.path):
            self.load()
        # Fallback to json for backwards compatibility/migration
        elif os.path.exists(self.path.replace(".parquet", ".json")):
            print("[cache] Migrating from JSON to Parquet...")
            import json
            with open(self.path.replace(".parquet", ".json")) as f:
                self.data = json.load(f)
            self.save()

    def load(self):
        df = pd.read_parquet(self.path)
        self.data = df.to_dict(orient="index")
        print(f"[cache] Loaded {len(self.data)} entries from {self.path}")

    def save(self):
        if not self.data:
            return
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        pd.DataFrame.from_dict(self.data, orient="index").to_parquet(self.path)

    def checkpoint(self, step: int, every: int = 200, total: int = 0):
        if step > 0 and step % every == 0:
            self.save()
            from tqdm import tqdm
            tqdm.write(f"  [cache] Checkpoint at {step}/{total} — {len(self.data)} cached")

    def __contains__(self, key) -> bool:
        return str(key) in self.data

    def __getitem__(self, key):
        return self.data[str(key)]

    def __setitem__(self, key, value):
        self.data[str(key)] = value

    def __len__(self):
        return len(self.data)

    def missing_from(self, ids: list) -> list:
        """Return IDs not yet in cache."""
        return [i for i in ids if str(i) not in self.data]
