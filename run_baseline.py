"""
Baseline inference script for the Code Debugging Environment.

Reads HF_TOKEN from environment variable (or .env file), uses the OpenAI API
to attempt fixing each buggy code task, and reports a reproducible baseline
score across all tasks.

Reproducibility is ensured by:
- temperature=0  (greedy decoding, no randomness)
- seed=42        (deterministic sampling on supported models)
- Fixed model name pinned at call time
"""

import os

from dotenv import load_dotenv

load_dotenv()  # load .env file if present, before reading env vars

import openai

from env.environment import Environment
from env.models import Action

# Pinned for reproducibility — change only intentionally
MODEL = "gpt-4o-mini"
SEED = 42
TEMPERATURE = 0


def get_fixed_code(client: openai.OpenAI, task_id: str, buggy_code: str, description: str) -> str:
    """Call the OpenAI API and return the fixed code string."""
    prompt = (
        f"You are a Python debugging assistant.\n\n"
        f"Task description: {description}\n\n"
        f"Buggy code:\n```python\n{buggy_code}\n```\n\n"
        f"Return ONLY the corrected Python code. "
        f"Do not include any explanation, comments, or markdown fences."
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        seed=SEED,
    )
    fixed = response.choices[0].message.content or ""
    # Strip markdown fences if the model included them anyway
    if fixed.startswith("```"):
        lines = fixed.splitlines()
        fixed = "\n".join(line for line in lines if not line.startswith("```"))
    return fixed.strip()


def main() -> None:
    # Read API key from environment variable HF_TOKEN
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise EnvironmentError(
            "HF_TOKEN environment variable is not set.\n"
            "Add it to your .env file:  HF_TOKEN=sk-...\n"
            "Or set it in your shell:   set HF_TOKEN=sk-...  (CMD)\n"
            "                           $env:HF_TOKEN='sk-...'  (PowerShell)"
        )

    client = openai.OpenAI(api_key=token)
    env = Environment()

    print(f"Model : {MODEL}")
    print(f"Seed  : {SEED}")
    print(f"Temp  : {TEMPERATURE}")
    print("-" * 40)

    obs = env.reset()
    scores: list[float] = []

    while True:
        task_id = obs.task_id

        fixed_code = ""
        try:
            fixed_code = get_fixed_code(client, task_id, obs.buggy_code, obs.description)
        except Exception as exc:
            print(f"[{task_id}] API error: {exc}")
            fixed_code = ""

        next_obs, reward, done, _ = env.step(Action(fixed_code=fixed_code))

        print(f"[{task_id}] score: {reward.value:.2f}")
        scores.append(reward.value)

        if done or next_obs is None:
            break
        obs = next_obs

    avg = sum(scores) / len(scores) if scores else 0.0
    print("-" * 40)
    print(f"Average score: {avg:.2f}  (across {len(scores)} tasks)")


if __name__ == "__main__":
    main()
