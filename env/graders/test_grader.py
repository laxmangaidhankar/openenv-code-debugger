import pytest
from env.graders.grader import Grader
from env.tasks import TaskRegistry

registry = TaskRegistry()
grader = Grader()

EASY_TASK = registry.get_by_id("easy_syntax")
MEDIUM_TASK = registry.get_by_id("medium_logic")
HARD_TASK = registry.get_by_id("hard_edge")


def test_syntax_invalid_returns_0():
    assert grader.grade(EASY_TASK, "def foo(\n") == 0.0


def test_runtime_error_returns_0_1():
    code = "def is_even(n):\n    raise ValueError('boom')"
    assert grader.grade(EASY_TASK, code) == 0.1


def test_correct_easy_task_returns_1():
    code = "def is_even(n):\n    return n % 2 == 0"
    assert grader.grade(EASY_TASK, code) == 1.0


def test_correct_medium_task_returns_1():
    code = "def is_positive(n):\n    return n > 0"
    assert grader.grade(MEDIUM_TASK, code) == 1.0


def test_correct_hard_task_returns_1():
    code = "def average(nums):\n    return sum(nums) / len(nums) if nums else 0.0"
    assert grader.grade(HARD_TASK, code) == 1.0


def test_partial_solution_returns_0_5():
    # Passes args [1] -> True, fails args [-1] -> False (returns True), fails args [0] -> False (returns True)
    # Actually passes 1 out of 3 -> partial
    code = "def is_positive(n):\n    return True"
    result = grader.grade(MEDIUM_TASK, code)
    assert result == 0.5
