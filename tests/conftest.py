"""Tests run fully offline: demo mode, a temp var/ dir, and a fake Meta transport where a test needs one."""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ["DEMO_MODE"] = "1"
os.environ["MODEL_API_KEY"] = ""
os.environ.setdefault("DEFECT_FORGE_VAR", tempfile.mkdtemp(prefix="defect-forge-test-"))
sys.path.insert(0, str(ROOT / "backend"))
