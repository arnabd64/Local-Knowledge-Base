"""
Module: src.utils
"""

import hashlib
from pathlib import Path


def _directory_id(root_path: Path) -> str:
    input: bytes = str(root_path.absolute()).encode("utf-8")
    return hashlib.sha1(input).hexdigest()
