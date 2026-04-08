"""Unit tests for the Environment class."""

import pytest
from env.environment import Environment
from env.models import Action, Observation, Reward


@pytest.fixture
def env():
    return Environment()


def test_reset_returns_first_task_observation(env):
    obs = env.reset()
    assert isinstance(obs, Observation)
    assert obs.task_id == "easy_syntax"


def test_step_returns_done_after_all_tasks(env):
    env.reset()
    action = Action(fixed_code="pass")
    done = False
    for _ in range(3):
        _, _, done, _ = env.step(action)
    assert done is True


def test_state_returns_correct_keys(env):
    env.reset()
    s = env.state()
    assert "task_id" in s
    assert "task_index" in s
    assert "total_tasks" in s


def test_state_task_index_starts_at_zero(env):
    env.reset()
    assert env.state()["task_index"] == 0


def test_step_beyond_last_task_returns_done(env):
    env.reset()
    action = Action(fixed_code="pass")
    for _ in range(3):
        env.step(action)
    _, _, done, _ = env.step(action)
    assert done is True


def test_step_returns_reward(env):
    env.reset()
    action = Action(fixed_code="pass")
    _, reward, _, _ = env.step(action)
    assert isinstance(reward, Reward)
    assert 0.0 <= reward.value <= 1.0
