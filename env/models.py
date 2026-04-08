from pydantic import BaseModel


class Observation(BaseModel):
    task_id: str
    buggy_code: str
    description: str


class Action(BaseModel):
    fixed_code: str


class Reward(BaseModel):
    value: float
