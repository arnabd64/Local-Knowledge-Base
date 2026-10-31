from pathlib import Path

from src.builder import build_directory_manifest
from src.diff import DiffOperator
from src.repository import load, save

if __name__ == "__main__":
    # parameters
    root_path: Path = Path("./src")
    allowed_types = ["*.py"]

    manifest = build_directory_manifest(root_path, allowed_types)
    disk_path = save(manifest)
    rebuild_manifest = load(root_path)

    diff = DiffOperator(
        existing=rebuild_manifest,
        new=build_directory_manifest(root_path, allowed_types),
    )

    action_list = diff.create_action_list()

    print(action_list)
