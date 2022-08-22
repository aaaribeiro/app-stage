from typing import Optional
from pydantic import BaseModel


class Organization(BaseModel):
    id: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True