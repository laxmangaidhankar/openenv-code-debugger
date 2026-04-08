import pytest
from pydantic import ValidationError

from env.models import Action, Observation, Reward


def test_observation_valid():
    obs = Observation(task_id="t1", buggy_code="def f(): pass", description="Fix it")
    assert obs.task_id == "t1"
    assert obs.buggy_code == "def f(): pass"
    assert obs.description == "Fix it"


def test_action_valid():
    action = Action(fixed_code="def f(): return 1")
    assert action.fixed_code == "def f(): return 1"


def test_reward_valid():
    reward = Reward(value=0.75)
    assert reward.value == 0.75


def test_observation_invalid_types():
    with pytest.raises(ValidationError):
        Observation(task_id=123, buggy_code=None, description=True)


def test_action_invalid_type():
    with pytest.raises(ValidationError):
        Action(fixed_code=42)


def test_reward_invalid_type():
    with pytest.raises(ValidationError):
        Reward(value="not-a-float")
