"""
Property-based tests for the Environment class using Hypothesis.

Feature: code-debugging-environment
"""

from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st

from env.environment import Environment
from env.models import Action


# ---------------------------------------------------------------------------
# Property 6: step advances task index
# Tag: Feature: code-debugging-environment, Property 6: step advances task index
# Validates: Requirements 2.4
# ---------------------------------------------------------------------------

@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(st.integers(min_value=1, max_value=3))
def test_step_advances_task_index(n: int) -> None:
    """After reset(), calling step() n times should result in _task_index == n."""
    env = Environment()
    env.reset()
    for i in range(n):
        env.step(Action(fixed_code="pass"))
        assert env._task_index == i + 1


# ---------------------------------------------------------------------------
# Property 7: reset restores initial state
# Tag: Feature: code-debugging-environment, Property 7: reset restores initial state
# Validates: Requirements 2.5
# ---------------------------------------------------------------------------

@settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(st.integers(min_value=1, max_value=3))
def test_reset_restores_initial_state(n: int) -> None:
    """After stepping n times, reset() restores _task_index to 0 and returns first task."""
    env = Environment()
    env.reset()
    for _ in range(n):
        env.step(Action(fixed_code="pass"))
    obs = env.reset()
    assert env._task_index == 0
    assert obs.task_id == "easy_syntax"


# ---------------------------------------------------------------------------
# Property 8: Observation fields non-empty after reset
# Tag: Feature: code-debugging-environment, Property 8: observation fields non-empty after reset
# Validates: Requirements 1.1, 2.1
# ---------------------------------------------------------------------------

@settings(max_examples=10)
@given(st.none())
def test_observation_fields_non_empty_after_reset(_: None) -> None:
    """The Observation returned by reset() must have non-empty task_id, buggy_code, description."""
    env = Environment()
    obs = env.reset()
    assert obs.task_id != ""
    assert obs.buggy_code != ""
    assert obs.description != ""
