from dataclasses import dataclass


@dataclass
class Task:
    task_id: str
    buggy_code: str
    description: str
    test_cases: list[dict]
    solution_fn_name: str


_TASKS = [
    Task(
        task_id="easy_syntax",
        buggy_code="\ndef is_even(n)\n    return n % 2 == 0\n",
        description="Fix the syntax error in the function definition.",
        test_cases=[
            {"args": [2], "expected": True},
            {"args": [3], "expected": False},
            {"args": [0], "expected": True},
        ],
        solution_fn_name="is_even",
    ),
    Task(
        task_id="medium_logic",
        buggy_code="\ndef is_positive(n):\n    return n >= 0\n",
        description="Fix the logical bug: the function should return True only for strictly positive numbers (greater than zero).",
        test_cases=[
            {"args": [1], "expected": True},
            {"args": [-1], "expected": False},
            {"args": [0], "expected": False},
        ],
        solution_fn_name="is_positive",
    ),
    Task(
        task_id="hard_edge",
        buggy_code="\ndef average(nums):\n    return sum(nums) / len(nums)\n",
        description="Fix the function so it handles an empty list by returning 0.0 instead of raising a ZeroDivisionError.",
        test_cases=[
            {"args": [[1, 2, 3]], "expected": 2.0},
            {"args": [[]], "expected": 0.0},
            {"args": [[-1, 1]], "expected": 0.0},
        ],
        solution_fn_name="average",
    ),
]


class TaskRegistry:
    def get_all(self) -> list[Task]:
        return list(_TASKS)

    def get_by_id(self, task_id: str) -> Task:
        for task in _TASKS:
            if task.task_id == task_id:
                return task
        raise KeyError(f"No task found with task_id: {task_id!r}")
