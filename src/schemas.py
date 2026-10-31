"""
Module: src.schemas
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileManifest:
    path: Path
    type: str
    hash: str


@dataclass(frozen=True, slots=True)
class DirectoryManifest:
    id: str
    root_path: Path
    allowed_types: list[str]
    files: tuple[FileManifest, ...]
    count: int
    created_on: str
