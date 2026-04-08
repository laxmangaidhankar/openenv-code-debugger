from env.models import Observation, Action, Reward
from env.tasks import TaskRegistry
from env.graders.grader import Grader


class Environment:
    def __init__(self) -> None:
        self._registry = TaskRegistry()
        self._tasks = self._registry.get_all()
        self._grader = Grader()
        self._task_index = 0

    def reset(self) -> Observation:
        self._task_index = 0
        task = self._tasks[0]
        return Observation(
            task_id=task.task_id,
            buggy_code=task.buggy_code,
            description=task.description,
        )

    def step(self, action: Action) -> tuple[Observation | None, Reward, bool, dict]:
        # Already done — all tasks exhausted
        if self._task_index >= len(self._tasks):
            return (None, Reward(value=0.0), True, {})

        current_task = self._tasks[self._task_index]
        reward_value = self._grader.grade(current_task, action.fixed_code)
        self._task_index += 1

        done = self._task_index >= len(self._tasks)

        if done:
            next_obs = None
        else:
            next_task = self._tasks[self._task_index]
            next_obs = Observation(
                task_id=next_task.task_id,
                buggy_code=next_task.buggy_code,
                description=next_task.description,
            )

        return (next_obs, Reward(value=reward_value), done, {})

    def state(self) -> dict:
        if self._task_index < len(self._tasks):
            task_id = self._tasks[self._task_index].task_id
        else:
            task_id = None
        return {
            "task_id": task_id,
            "task_index": self._task_index,
            "total_tasks": len(self._tasks),
        }
