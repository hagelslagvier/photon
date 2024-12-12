from __future__ import annotations

from typing import Any, TypeVar

from sqlalchemy.orm import DeclarativeBase as OriginalBase

T = TypeVar("T", bound="DeclarativeBase")


def _get_primary_key(cls: type[T]) -> list[str]:
    primary_key = [c.name for c in cls.__mapper__.primary_key]
    return primary_key


def _get_attributes(cls: type[T]) -> list[str]:
    primary_key = set(cls._get_primary_key())  # type: ignore
    attributes = {c.name for c in cls.__mapper__.columns} | {
        r.key for r in cls.__mapper__.relationships
    }
    safe_attributes = list(attributes - primary_key)
    return safe_attributes


def new(cls: type, **kwargs: Any) -> type:
    safe_kwargs = {k: v for k, v in kwargs.items() if k in cls._get_attributes()}  # type: ignore
    return cls(**safe_kwargs)


def update(self: T, **kwargs: Any) -> None:
    safe_kwargs = {k: v for k, v in kwargs.items() if k in self._get_attributes()}  # type: ignore
    for k, v in safe_kwargs.items():
        setattr(self, k, v)


def inzichtify(original: type) -> type:
    setattr(original, "_get_primary_key", classmethod(_get_primary_key))
    setattr(original, "_get_attributes", classmethod(_get_attributes))
    setattr(original, "new", classmethod(new))
    setattr(original, "update", update)
    return original


@inzichtify
class DeclarativeBase(OriginalBase):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}
