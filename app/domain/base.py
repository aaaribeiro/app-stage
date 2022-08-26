from pydantic import BaseModel


class Base(BaseModel):

    def fields_set(self):
        return self.__fields_set__