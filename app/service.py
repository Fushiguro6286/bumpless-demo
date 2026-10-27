import json
from typing import Any, Dict, List

from app.models import User, UserUpdate


class UserRow:
    """Stand-in for an ORM row object."""

    def __init__(self, **kw: Any) -> None:
        self.__dict__.update(kw)


def user_from_row(row: UserRow) -> User:
    return User.model_validate(row, from_attributes=True)


def to_payload(user: User) -> Dict[str, Any]:
    return user.model_dump(exclude_none=True)


def to_json(user: User) -> str:
    return user.model_dump_json()


def parse_users(data: List[Dict[str, Any]]) -> List[User]:
    return [User.model_validate(d) for d in data]


def parse_user_json(raw: str) -> User:
    return User.model_validate_json(raw)


def apply_update(user: User, update: UserUpdate) -> User:
    return user.model_copy(update=update.model_dump(exclude_unset=True))


def field_names() -> List[str]:
    return list(User.model_fields.keys())


def roundtrip(user: User) -> User:
    return User.model_validate(json.loads(user.model_dump_json()))
