from typing import Optional
from pydantic import BaseModel


class Agent(BaseModel):
    id: Optional[str]
    name: Optional[str]
    team: Optional[str]

    class Config:
        orm_mode = True