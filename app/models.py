from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(..., pattern=r"^\d{5}$")


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    tags: List[str] = []
    address: Optional[Address] = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )

    @field_validator("email")
    @classmethod
    def email_must_have_at(cls, v):
        if "@" not in v:
            raise ValueError("invalid email")
        return v.lower()

    @model_validator(mode="after")
    def check_age(self):
        if self.age is not None and self.age < 0:
            raise ValueError("age must not be negative")
        return self


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(extra="ignore")
