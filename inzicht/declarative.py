from typing import Any, Self

from sqlalchemy.orm import DeclarativeBase as OriginalBase


class DeclarativeBase(OriginalBase):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    @classmethod
    def _get_primary_key(cls) -> list[str]:
        primary_key = [c.name for c in cls.__mapper__.primary_key]
        return primary_key

    @classmethod
    def _get_attributes(cls) -> list[str]:
        primary_key = set(cls._get_primary_key())
        attributes = {c.name for c in cls.__mapper__.columns} | {
            r.key for r in cls.__mapper__.relationships
        }
        safe_attributes = list(attributes - primary_key)
        return safe_attributes

    @classmethod
    def new(cls, **kwargs: Any) -> Self:
        safe_kwargs = {k: v for k, v in kwargs.items() if k in cls._get_attributes()}
        return cls(**safe_kwargs)

    def update(self, **kwargs: Any) -> None:
        safe_kwargs = {k: v for k, v in kwargs.items() if k in self._get_attributes()}
        for k, v in safe_kwargs.items():
            setattr(self, k, v)
