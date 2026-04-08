import os  # MUST be at the top
from dotenv import load_dotenv
load_dotenv()

import openai
from env.environment import Environment
from env.models import Action

# CONFIG
MODEL = "gpt-4o-mini"
SEED = 42
TEMPERATURE = 0

MAX_API_CALLS = 10
MAX_TOKENS = 300
TIMEOUT_SECONDS = 15

api_call_count = 0

def get_fixed_code(client: openai.OpenAI, task_id: str, buggy_code: str, description: str) -> str:
    global api_call_count
    if api_call_count >= MAX_API_CALLS:
        print(f"[{task_id}] API call limit reached. Skipping...")
        return ""
    api_call_count += 1
    prompt = (
        f"You are a Python debugging assistant.\n\n"
        f"Task description: {description}\n\n"
        f"Buggy code:\n```python\n{buggy_code}\n```\n\n"
        f"Return ONLY the corrected Python code. No explanation. No markdown."
    )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            seed=SEED,
            max_tokens=MAX_TOKENS,
            timeout=TIMEOUT_SECONDS,
        )
        fixed = response.choices[0].message.content or ""
        if fixed.startswith("```"):
            lines = fixed.splitlines()
            fixed = "\n".join(line for line in lines if not line.startswith("```"))
        return fixed.strip()
    except Exception as exc:
        print(f"[{task_id}] API error: {exc}")
        return ""

def main() -> None:
    # ===== API KEY HANDLING =====
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise EnvironmentError(
            "❌ HF_TOKEN not set. Add it in .env (local) or Hugging Face Secrets."
        )
    print("✅ Token loaded, proceeding with environment setup")
    client = openai.OpenAI(api_key=token)

    env = Environment()
    print("✅ Environment initialized")

    print(f"Model : {MODEL}")
    print(f"Seed  : {SEED}")
    print(f"Temp  : {TEMPERATURE}")
    print(f"Max Calls : {MAX_API_CALLS}")
    print("-" * 40)

    obs = env.reset()
    scores: list[float] = []
    step_count = 0
    MAX_STEPS = 10

    while True:
        if step_count >= MAX_STEPS:
            print("⚠️ Max steps reached. Stopping execution.")
            break
        task_id = obs.task_id
        fixed_code = get_fixed_code(client, task_id, obs.buggy_code, obs.description)
        next_obs, reward, done, _ = env.step(Action(fixed_code=fixed_code))
        print(f"[{task_id}] score: {reward.value:.2f}")
        scores.append(reward.value)
        step_count += 1
        if done or next_obs is None:
            break
        obs = next_obs

    avg = sum(scores) / len(scores) if scores else 0.0
    print("-" * 40)
    print(f"Average score: {avg:.2f}  (across {len(scores)} tasks)")
    print(f"Total API calls used: {api_call_count}/{MAX_API_CALLS}")
    print("🏁 Baseline script finished successfully")


if __name__ == "__main__":
    main()
