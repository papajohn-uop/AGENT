# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401
import enum

class  ResourceAdministrativeStateTypeEnum(enum.Enum):
   locked="locked"
   unlocked="unlocked"
   shutdown="shutdown"
   
class ResourceAdministrativeStateType(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    ResourceAdministrativeStateType - a model defined in OpenAPI

    """


ResourceAdministrativeStateType.update_forward_refs()
