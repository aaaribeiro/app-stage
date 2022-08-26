from typing import Optional
from app.domain.base import Base


class Organization(Base):
    id: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True