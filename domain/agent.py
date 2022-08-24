from re import A
from typing import Optional
from pydantic import BaseModel


class Agent(BaseModel):
    id: Optional[str]
    name: Optional[str]
    team: Optional[str]

    def fields_set(self):
        return self.__fields_set__

    class Config:
        orm_mode = True


if __name__ == '__main__':
    agent = Agent(id='ANY')
    for field in agent.fields_set():
        print(getattr(agent, field))