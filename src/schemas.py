"""
Module: src.schemas
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Actions(Enum):
    IGNORE = "Ignore"
    INSERT = "Insert"
    DELETE = "Delete"


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


@dataclass(frozen=True, slots=True)
class ActionList:
    file: Path
    action: Actions


class HashTable:
    def __init__(self, manifests: tuple[FileManifest, ...]) -> None:
        self.table: dict[str, Path] = {file.hash: file.path for file in manifests}

    def _get_keys(self) -> set[str]:
        return set(self.table.keys())

    def __and__(self, other: "HashTable") -> tuple[Path, ...]:
        """
        Returns  file paths which are common in both tables. (self intersection other)
        """
        # get the keys
        self_keys = self._get_keys()
        other_keys = other._get_keys()

        # intersection operation
        common_keys = tuple(self_keys.intersection(other_keys))

        return tuple([self.table[key] for key in common_keys])

    def __sub__(self, other: "HashTable") -> tuple[Path, ...]:
        """
        Returns file paths which are only present in the self table
        """
        # get the keys
        self_keys = self._get_keys()
        other_keys = other._get_keys()

        # difference operation
        diff_keys = self_keys.difference(other_keys)

        return tuple([self.table[key] for key in diff_keys])
