from typing import Optional
from domain.base import Base


class Agent(Base):
    id: Optional[str]
    name: Optional[str]
    team: Optional[str]

    class Config:
        orm_mode = True
