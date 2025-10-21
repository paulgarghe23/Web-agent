import sys, os
import pytest
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

@pytest.fixture(autouse=True, scope="session")
def _enable_info_logs():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(levelname)s | %(name)s | %(message)s",
        filename="debug.log",
        filemode="w",
        )