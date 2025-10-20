import sys, os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
