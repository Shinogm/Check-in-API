from pydantic import BaseModel
from enum import Enum
from typing import Annotated
from fastapi import Form

class UserTypeEnum(Enum):
    ADMIN = "admin"
    CLIENT = "client"
    NONE = "none"

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str | None = None

    @classmethod
    def as_form(
        cls,
        first_name: Annotated[str, Form(...)],
        last_name: Annotated[str, Form(...)],
        email: Annotated[str, Form(...)],
        password: Annotated[str | None, Form(...)] = None,
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
    
class ModifyUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str  | None = None
    password: str | None = None

    @classmethod
    def as_form(
        cls,
        first_name: Annotated[str | None, Form(...)] = None,
        last_name: Annotated[str | None, Form(...)] = None,
        email: Annotated[str | None, Form(...)] = None,
        password: Annotated[str | None, Form(...)] = None,
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
