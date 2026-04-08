---
tags:
  - openenv
---

# Code Debugging Environment

An [OpenEnv](https://openenv.dev)-compatible evaluation environment that tests an AI agent's ability to identify and fix buggy Python code.

## Motivation

Debugging is a core software engineering skill. This environment provides a reproducible, deterministic benchmark for evaluating how well an AI agent can:

- Identify syntax errors
- Spot logical bugs
- Handle edge cases

Reward scores between `0.0` and `1.0` make the environment suitable for reinforcement learning experiments, model benchmarking, and automated evaluation pipelines.

---

## Data Models

### Observation

Presented to the agent at the start of each task.

| Field | Type | Description |
|---|---|---|
| `task_id` | `str` | Unique identifier for the task |
| `buggy_code` | `str` | The Python code containing a bug |
| `description` | `str` | Human-readable description of what to fix |

### Action

Submitted by the agent after inspecting the observation.

| Field | Type | Description |
|---|---|---|
| `fixed_code` | `str` | The agent's corrected version of the code |

### Reward

Returned by the environment after grading.

| Field | Type | Description |
|---|---|---|
| `value` | `float` | Score in `[0.0, 1.0]` |

---

## Tasks

| Task ID | Difficulty | Bug Type | Description |
|---|---|---|---|
| `easy_syntax` | Easy | Syntax error | Missing colon in `is_even` function definition |
| `medium_logic` | Medium | Logical bug | `is_positive` uses `>=` instead of `>`, incorrectly treating 0 as positive |
| `hard_edge` | Hard | Edge case | `average` crashes on empty list with `ZeroDivisionError` |

---

## Reward Scoring

| Condition | Score |
|---|---|
| Syntax invalid | `0.0` |
| Syntax valid, runtime error | `0.1` |
| Syntax valid, 0 tests pass | `0.1` |
| Syntax valid, some tests pass | `0.5` |
| All tests pass | `1.0` |

---

## Setup

```bash
pip install -r requirements.txt
```

**requirements.txt** includes:
- `pydantic>=2.0`
- `openai>=1.0`
- `hypothesis>=6.0`

---

## Running Locally

Set your OpenAI API key (the script reads `HF_TOKEN`):

```bash
export HF_TOKEN=sk-...
python run_baseline.py
```

Expected output:

```
[easy_syntax] score: 1.00
[medium_logic] score: 1.00
[hard_edge] score: 1.00

Average score: 1.00
```

---

## Running Tests

```bash
python -m pytest env/ test_baseline.py -v
```

---

## Docker

Build:

```bash
docker build -t code-debugging-env .
```

Run:

```bash
docker run -e HF_TOKEN=sk-... code-debugging-env
```

---

## Baseline Results

Results using `gpt-4o-mini` (temperature=0):

| Task | Score |
|---|---|
| `easy_syntax` | 1.00 |
| `medium_logic` | 1.00 |
| `hard_edge` | 1.00 |
| **Average** | **1.00** |

*Actual results may vary depending on model version and API availability.*
