# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401


class EventSubscriptionInput(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    EventSubscriptionInput - a model defined in OpenAPI

        callback: The callback of this EventSubscriptionInput.
        query: The query of this EventSubscriptionInput [Optional].
    """

    callback: str
    query: Optional[str] = None

EventSubscriptionInput.update_forward_refs()
