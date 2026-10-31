"""
Module: src.diff

Description:
    - Compares Manifests and creates an Action List for each file
"""

from pathlib import Path

from src.logger import get_logger
from src.schemas import ActionList, Actions, DirectoryManifest, HashTable

logger = get_logger(__name__)


class DiffOperator:
    def __init__(self, existing: DirectoryManifest, new: DirectoryManifest) -> None:
        self.existing = existing
        self.new = new

    def create_action_list(self) -> tuple[ActionList, ...]:
        if self.existing.root_path != self.new.root_path:
            logger.error("Trying to compare Manifests of different Directories")
            raise ValueError

        logger.info("Creating Hash Tables")

        # create hash tables
        existing = HashTable(self.existing.files)
        new = HashTable(self.new.files)

        # perform diff operations
        _ignore: tuple[Path, ...] = existing & new
        _insert: tuple[Path, ...] = new - existing
        _delete: tuple[Path, ...] = existing - new

        # log
        logger.info(
            "Diff Stats: "
            f"Ignore: {len(_ignore)}, "
            f"Insert: {len(_insert)}, "
            f"Delete: {len(_delete)}; "
        )

        action_list = (
            [ActionList(file=f, action=Actions.IGNORE) for f in _ignore]
            + [ActionList(file=f, action=Actions.INSERT) for f in _insert]
            + [ActionList(file=f, action=Actions.DELETE) for f in _delete]
        )
        return tuple(action_list)
