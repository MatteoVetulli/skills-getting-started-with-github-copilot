import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client():
    return TestClient(app)
