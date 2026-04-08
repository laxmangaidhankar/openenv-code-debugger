from env.tasks import Task


class Grader:
    def grade(self, task: Task, fixed_code: str) -> float:
        # Step 1: Syntax check
        try:
            compile(fixed_code, "<string>", "exec")
        except SyntaxError:
            return 0.0

        # Step 2: exec() into isolated namespace
        namespace: dict = {}
        try:
            exec(compile(fixed_code, "<string>", "exec"), namespace)
        except Exception:
            return 0.1  # 0.3 - 0.2 penalty

        # Step 3: Run each test case
        passed = 0
        total = len(task.test_cases)
        had_runtime_error = False

        for tc in task.test_cases:
            try:
                result = namespace[task.solution_fn_name](*tc["args"])
                if result == tc["expected"]:
                    passed += 1
            except Exception:
                had_runtime_error = True

        # Step 4: Score assignment
        if passed == total:
            return 1.0
        elif 1 <= passed < total:
            return 0.5
        elif had_runtime_error:
            return 0.1
        else:
            # 0 passed, no runtime error
            return 0.1
