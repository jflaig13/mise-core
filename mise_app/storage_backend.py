"""Storage backend abstraction for local/cloud storage."""
from pathlib import Path
import json
import os
from abc import ABC, abstractmethod
from typing import Optional
import logging

log = logging.getLogger(__name__)


class StorageBackend(ABC):
    """Abstract storage backend."""

    @abstractmethod
    def read_json(self, path: str) -> dict:
        pass

    @abstractmethod
    def write_json(self, path: str, data: dict) -> None:
        pass

    @abstractmethod
    def exists(self, path: str) -> bool:
        pass

    @abstractmethod
    def list_dir(self, path: str) -> list[str]:
        pass

    @abstractmethod
    def delete(self, path: str) -> bool:
        pass


class LocalStorage(StorageBackend):
    """Local filesystem storage."""

    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)

    def read_json(self, path: str) -> dict:
        file_path = self.base_dir / path
        with open(file_path) as f:
            return json.load(f)

    def write_json(self, path: str, data: dict) -> None:
        file_path = self.base_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def exists(self, path: str) -> bool:
        return (self.base_dir / path).exists()

    def list_dir(self, path: str) -> list[str]:
        dir_path = self.base_dir / path
        if not dir_path.exists():
            return []
        return [p.name for p in dir_path.iterdir()]

    def delete(self, path: str) -> bool:
        file_path = self.base_dir / path
        if file_path.exists():
            file_path.unlink()
            return True
        return False


class GCSStorage(StorageBackend):
    """Google Cloud Storage backend."""

    def __init__(self, bucket_name: str, base_prefix: str = ""):
        from google.cloud import storage
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.base_prefix = base_prefix.rstrip("/")

    def _blob_path(self, path: str) -> str:
        if self.base_prefix:
            return f"{self.base_prefix}/{path}"
        return path

    def read_json(self, path: str) -> dict:
        blob = self.bucket.blob(self._blob_path(path))
        content = blob.download_as_text()
        return json.loads(content)

    def write_json(self, path: str, data: dict) -> None:
        blob = self.bucket.blob(self._blob_path(path))
        blob.upload_from_string(
            json.dumps(data, indent=2),
            content_type="application/json"
        )

    def exists(self, path: str) -> bool:
        blob = self.bucket.blob(self._blob_path(path))
        return blob.exists()

    def list_dir(self, path: str) -> list[str]:
        prefix = self._blob_path(path).rstrip("/") + "/"
        blobs = self.bucket.list_blobs(prefix=prefix, delimiter="/")

        # Get immediate children only
        items = set()
        for blob in blobs:
            # Remove prefix and get first component
            rel_path = blob.name[len(prefix):]
            if "/" in rel_path:
                items.add(rel_path.split("/")[0])
            elif rel_path:
                items.add(rel_path)

        # Add prefixes (directories)
        for prefix_obj in blobs.prefixes:
            dir_name = prefix_obj.rstrip("/").split("/")[-1]
            items.add(dir_name)

        return list(items)

    def delete(self, path: str) -> bool:
        blob = self.bucket.blob(self._blob_path(path))
        if blob.exists():
            blob.delete()
            return True
        return False


# Singleton instance
_storage_backend: Optional[StorageBackend] = None


def get_storage_backend() -> StorageBackend:
    """Get storage backend based on environment."""
    global _storage_backend

    if _storage_backend is not None:
        return _storage_backend

    env = os.getenv("ENVIRONMENT", "development")

    if env == "production":
        bucket_name = os.getenv("GCS_BUCKET_NAME", "mise-production-data")
        log.info(f"Using GCS storage: {bucket_name}")
        _storage_backend = GCSStorage(bucket_name)
    else:
        base_dir = Path(__file__).parent / "data"
        log.info(f"Using local storage: {base_dir}")
        _storage_backend = LocalStorage(base_dir)

    return _storage_backend
