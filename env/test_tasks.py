import pytest
from env.tasks import Task, TaskRegistry


@pytest.fixture
def registry():
    return TaskRegistry()


def test_get_all_returns_three_tasks(registry):
    tasks = registry.get_all()
    assert len(tasks) == 3


def test_all_tasks_have_required_fields(registry):
    for task in registry.get_all():
        assert task.task_id
        assert task.buggy_code
        assert task.description
        assert task.test_cases
        assert task.solution_fn_name


def test_get_by_id_easy(registry):
    task = registry.get_by_id("easy_syntax")
    assert task.task_id == "easy_syntax"
    assert task.solution_fn_name == "is_even"


def test_get_by_id_medium(registry):
    task = registry.get_by_id("medium_logic")
    assert task.task_id == "medium_logic"
    assert task.solution_fn_name == "is_positive"


def test_get_by_id_hard(registry):
    task = registry.get_by_id("hard_edge")
    assert task.task_id == "hard_edge"
    assert task.solution_fn_name == "average"


def test_get_by_id_unknown_raises_key_error(registry):
    with pytest.raises(KeyError):
        registry.get_by_id("nonexistent")


def test_easy_task_buggy_code_fails_compile(registry):
    task = registry.get_by_id("easy_syntax")
    with pytest.raises(SyntaxError):
        compile(task.buggy_code, "<string>", "exec")


def test_medium_task_buggy_code_runs_but_fails_test_case(registry):
    task = registry.get_by_id("medium_logic")
    ns = {}
    exec(compile(task.buggy_code, "<string>", "exec"), ns)
    # is_positive(0) should be False but buggy code returns True
    assert ns["is_positive"](0) is True  # confirms the bug


def test_hard_task_buggy_code_raises_on_empty_list(registry):
    task = registry.get_by_id("hard_edge")
    ns = {}
    exec(compile(task.buggy_code, "<string>", "exec"), ns)
    with pytest.raises(ZeroDivisionError):
        ns["average"]([])


def test_task_is_dataclass():
    task = Task(
        task_id="test",
        buggy_code="code",
        description="desc",
        test_cases=[],
        solution_fn_name="fn",
    )
    assert task.task_id == "test"
