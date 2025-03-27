import pathlib
from typing import Final


ROOT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[2]

ENV_FILE_PATH = ROOT_DIR.joinpath(".env")
