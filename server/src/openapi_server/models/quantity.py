# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class Quantity(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Quantity - a model defined in OpenAPI

        amount: The amount of this Quantity [Optional].
        units: The units of this Quantity [Optional].
    """

    amount: Optional[float] = None
    units: Optional[str] = None

Quantity.update_forward_refs()