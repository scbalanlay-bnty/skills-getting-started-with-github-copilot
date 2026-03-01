import sys
from pathlib import Path
import copy
import pytest
from fastapi.testclient import TestClient

# Ensure `src` is importable and import app and activities module-level objects
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from app import app, activities

# Keep an original snapshot to restore between tests
original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` dict before each test (test isolation)."""
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
