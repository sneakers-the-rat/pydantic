from __future__ import annotations

import pytest

from datetime import date

from pydantic import BaseModel, Field

A = str
def test_recursive_naming():
    """
    Models that have an attribute with the same name as the type annotation
    should not raise a recursion error
    """

    class MyModel(BaseModel):
        a: A = Field(...)
        A: A = Field(...)

    assert MyModel.model_fields['a'].annotation is str
    assert MyModel.model_fields['A'].annotation is str

def test_issue_7327():
    """
    https://github.com/pydantic/pydantic/issues/7327
    """
    class Settings(BaseModel):
        name: str

    class Model(BaseModel):
        Settings: Settings = Field(..., title="a nice title")

    assert Model.model_fields['Settings'].annotation is Settings

def test_issue_7309():
    """
    https://github.com/pydantic/pydantic/issues/7309
    """

    class MyModel(BaseModel):
        date: date = Field()

    assert MyModel.model_fields['date'].annotation is date


