"""
Module: src.builder.py

Description:
    - Builds Manifests
"""

import hashlib
from datetime import datetime
from pathlib import Path

from src.logger import get_logger
from src.schemas import DirectoryManifest, FileManifest
from src.utils import _directory_id

logger = get_logger(__name__)


def _file_hash(path: Path) -> str:
    """
    Generates the file hash which also includes the file path
    in the hashing process
    """
    sha256 = hashlib.sha256()

    # Update hash with the file path and a null separator to prevent collisions
    sha256.update(str(path).encode("utf-8"))
    sha256.update(b"\0")

    # Stream the file contents in chunks (1MB)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(2**20), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def scan_directory(path: Path, allowed_types: list[str]) -> tuple[Path, ...]:
    """
    Recursively goes through all the files in a directory and it's sub-directories
    and returns the list of files that have matched with the patterns in `allowed_types`
    """
    return tuple(
        [
            p
            for pattern in allowed_types
            for p in path.rglob(pattern, case_sensitive=False)
            if p.is_file()
        ]
    )


def build_file_manifest(path: Path) -> FileManifest:
    return FileManifest(
        path=path, type=path.suffix.lower().lstrip("."), hash=_file_hash(path)
    )


def build_directory_manifest(
    root_path: Path, allowed_types: list[str] | None = None
) -> DirectoryManifest:
    """
    Recursively scans a directory and builds a Manifest of all eligible files

    Args:
        - `root_path`: Path of the Directory to Scan
        - `allowed_types`: List of allowed types eg: *.pdf, *.md or *.* for all
    """
    # validate root_path
    if not root_path.is_dir() or not root_path.exists():
        logger.error(f"Directory: {str(root_path.absolute())} is Invalid")
        raise NotADirectoryError

    # validate allowed_types
    allowed_types = allowed_types or ["*.*"]

    # generate ID for Directory Manifest
    id: str = _directory_id(root_path)
    logger.info(f"Building Manifest for {str(root_path)} ({id})")

    # generate the file manifests
    file_manifests: tuple[FileManifest, ...] = tuple(
        [build_file_manifest(path) for path in scan_directory(root_path, allowed_types)]
    )
    logger.info(f"Scan Complete, Found {len(file_manifests)} matches")

    # timestamp
    created_on: str = datetime.now().isoformat()

    manifest = DirectoryManifest(
        id=id,
        root_path=root_path,
        allowed_types=allowed_types,
        files=file_manifests,
        count=len(file_manifests),
        created_on=created_on,
    )

    logger.info(f"Created Manifest for {str(root_path)} ({id})")

    return manifest
