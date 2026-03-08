import json
import os


class ThumbnailCache:
    def __init__(self, path: str):
        self.path = path
        self.data: dict = {}
        if os.path.exists(path):
            self.load()

    def load(self):
        with open(self.path) as f:
            self.data = json.load(f)
        print(f"[cache] Loaded {len(self.data)} entries from {self.path}")

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def checkpoint(self, step: int, every: int = 200, total: int = 0):
        if step > 0 and step % every == 0:
            self.save()
            from tqdm import tqdm
            tqdm.write(f"  [cache] Checkpoint at {step}/{total} — {len(self.data)} cached")

    def __contains__(self, key: str) -> bool:
        return key in self.data

    def __getitem__(self, key: str):
        return self.data[key]

    def __setitem__(self, key: str, value):
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def missing_from(self, ids: list[str]) -> list[str]:
        """Return IDs not yet in cache."""
        return [i for i in ids if i not in self.data]
