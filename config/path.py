from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def root(*parts):
    return ROOT_DIR.joinpath(*parts)
