"""
Module: src.repository

Description:
    - Performs File I/O with manifests
"""

import json
from pathlib import Path

from src.logger import get_logger
from src.schemas import DirectoryManifest, FileManifest
from src.utils import _directory_id

REPOSITORY: str = ".manifests"

logger = get_logger(__name__)


def save(manifest: DirectoryManifest, repo_path: Path = Path(REPOSITORY)) -> Path:
    # create repo
    if not repo_path.exists():
        repo_path.mkdir(parents=True, exist_ok=True)

    # get manifest id
    id: str = manifest.id
    logger.info(f"Saving Manifest for {str(manifest.root_path.absolute())}")

    # file path
    file_path: Path = Path(repo_path, f"{id}.json")
    logger.info(f"Save Path: {str(file_path)}")

    # Convert Manifest to Dict
    manifest_data: dict = {
        "id": manifest.id,
        "root_path": str(manifest.root_path),
        "allowed_types": manifest.allowed_types,
        "files": [
            {"path": str(p.path), "type": p.type, "hash": p.hash}
            for p in manifest.files
        ],
        "count": manifest.count,
        "created_on": manifest.created_on,
    }

    with file_path.open("w") as f:
        json.dump(manifest_data, f, indent=2)

    logger.info("Save Complete")

    return file_path


def load(root_path: Path) -> DirectoryManifest:
    # Validate if directory exists
    if not root_path.exists() or not root_path.is_dir():
        logger.info(f"Directory: {str(root_path)} is Invalid")
        raise NotADirectoryError

    # get file path
    manifest_path: Path = Path(REPOSITORY, f"{_directory_id(root_path)}.json")

    # validate
    if not manifest_path.exists() or not manifest_path.is_file():
        logger.error(f"Manifest {str(manifest_path)} is Invalid")
        raise FileNotFoundError

    # load the maqnifest
    with manifest_path.open("r") as f:
        data: dict = json.load(f)
    logger.info(f"Loaded Manifest: {str(manifest_path)}")

    # rebuild manifest
    manifest = DirectoryManifest(
        id=data["id"],
        root_path=Path(data["root_path"]),
        allowed_types=data["allowed_types"],
        files=tuple(
            [
                FileManifest(path=Path(p["path"]), type=p["type"], hash=p["hash"])
                for p in data["files"]
            ]
        ),
        count=data["count"],
        created_on=data["created_on"],
    )
    logger.info("Manifest Rebuilded")

    return manifest
