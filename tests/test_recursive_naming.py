# from __future__ import annotations

import pytest
import pdb
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

    # test with defaults present in field object
    class MyOtherModel(BaseModel):
        a: A = Field('FirstValue')
        A: A = Field('SecondValue')

    assert MyOtherModel.model_fields['a'].annotation is str
    assert MyOtherModel.model_fields['A'].annotation is str
    assert MyOtherModel().a == 'FirstValue'
    assert MyOtherModel().A == 'SecondValue'

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

def test_issue_7327_comment_1715813268_1():
    """
    https://github.com/pydantic/pydantic/issues/7327#issuecomment-1715813268
    """
    class MyModel(BaseModel):
        A: A = 'default'

    assert MyModel.model_fields['A'].annotation is str
    assert MyModel().A == 'default'

class SettingsA:
    pass
def test_issue_7327_comment_1715813268_2():
    """
    https://github.com/pydantic/pydantic/issues/7327#issuecomment-1715813268
    """
    # First the original case in the comments
    class MyClass(BaseModel, arbitrary_types_allowed=True):
        class SettingsA:
            pass

        my_settings: list[SettingsA]

    assert MyClass.model_fields['my_settings'].annotation == list[MyClass.SettingsA]

    # then an additional case to check that we aren't getting
    # the global-global namespace, just the parent-global namespace relative
    # to the scope evaluating the annotation
    class MyOtherClass(BaseModel, arbitrary_types_allowed=True):
        SettingsB: SettingsA = Field(default_factory=SettingsA)
        class SettingsA(BaseModel):
            SettingsA: SettingsA = Field(default_factory=SettingsA)

    assert MyOtherClass.SettingsA.model_fields['SettingsA'].annotation is MyOtherClass.SettingsA


def test_issue_7327_comment_1715813268_3():
    """
    https://github.com/pydantic/pydantic/issues/7327#issuecomment-1715813268
    """

    class MyClass(BaseModel, arbitrary_types_allowed=True):
        class SettingsB:
            pass

        my_settings: list[SettingsB]

    assert MyClass.model_fields['my_settings'].annotation == list[MyClass.SettingsB]
