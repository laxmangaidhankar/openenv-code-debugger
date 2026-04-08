"""
Property-based tests for the Grader class using Hypothesis.

Feature: code-debugging-environment
"""

from hypothesis import given, settings
import hypothesis.strategies as st

from env.graders.grader import Grader
from env.tasks import TaskRegistry


def is_valid_syntax(code: str) -> bool:
    try:
        compile(code, "<string>", "exec")
        return True
    except SyntaxError:
        return False


grader = Grader()
registry = TaskRegistry()
all_tasks = registry.get_all()


# ---------------------------------------------------------------------------
# Property 1: Reward is always in range [0.0, 1.0]
# Tag: Feature: code-debugging-environment, Property 1: reward always in [0.0, 1.0]
# Validates: Requirements 5.5
# ---------------------------------------------------------------------------

@given(st.text())
@settings(max_examples=100)
def test_reward_always_in_range(fixed_code: str):
    """Property 1: For any fixed_code string and any task, reward ∈ [0.0, 1.0]."""
    for task in all_tasks:
        reward = grader.grade(task, fixed_code)
        assert 0.0 <= reward <= 1.0, (
            f"Reward {reward} out of range for task {task.task_id!r} "
            f"with fixed_code={fixed_code!r}"
        )


# ---------------------------------------------------------------------------
# Property 2: Grader is deterministic
# Tag: Feature: code-debugging-environment, Property 2: grader is deterministic
# Validates: Requirements 4.7
# ---------------------------------------------------------------------------

@given(st.text())
@settings(max_examples=100)
def test_grader_is_deterministic(fixed_code: str):
    """Property 2: Calling grade() twice with the same inputs returns the same result."""
    for task in all_tasks:
        reward_1 = grader.grade(task, fixed_code)
        reward_2 = grader.grade(task, fixed_code)
        assert reward_1 == reward_2, (
            f"Non-deterministic result for task {task.task_id!r}: "
            f"{reward_1} != {reward_2} with fixed_code={fixed_code!r}"
        )


# ---------------------------------------------------------------------------
# Property 3: Syntax-invalid code scores 0.0
# Tag: Feature: code-debugging-environment, Property 3: syntax-invalid code scores 0.0
# Validates: Requirements 4.2, 5.1
# ---------------------------------------------------------------------------

@given(st.text().map(lambda s: "def (" + s))
@settings(max_examples=100)
def test_syntax_invalid_code_scores_zero(fixed_code: str):
    """Property 3: Any string that fails compile() must score exactly 0.0."""
    # Confirm the generated string is indeed syntactically invalid
    assert not is_valid_syntax(fixed_code), (
        f"Expected invalid syntax but got valid code: {fixed_code!r}"
    )
    for task in all_tasks:
        reward = grader.grade(task, fixed_code)
        assert reward == 0.0, (
            f"Expected 0.0 for syntax-invalid code on task {task.task_id!r}, "
            f"got {reward} with fixed_code={fixed_code!r}"
        )
