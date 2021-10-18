# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.error import Error
from openapi_server.models.resource import Resource
from openapi_server.models.resource_create import ResourceCreate
from openapi_server.models.resource_update import ResourceUpdate

import uuid

#from  common import handle_files
from  openapi_server import main

router = APIRouter()


@router.post(
    "/resource",
    responses={
        201: {"model": Resource, "description": "Created"},
        400: {"model": Error, "description": "Bad Request"},
        401: {"model": Error, "description": "Unauthorized"},
        403: {"model": Error, "description": "Forbidden"},
        405: {"model": Error, "description": "Method Not allowed"},
        409: {"model": Error, "description": "Conflict"},
        500: {"model": Error, "description": "Internal Server Error"},
    },
    tags=["resource"],
    summary="Creates a Resource",
)
async def create_resource(
    resource: ResourceCreate = Body(None, description="The Resource to be created"),
) -> Resource:
    """This operation creates a Resource entity."""
    return({"Nope":"Agent does not do POST"})

@router.delete(
    "/resource/{id}",
    responses={
        204: {"description": "Deleted"},
        400: {"model": Error, "description": "Bad Request"},
        401: {"model": Error, "description": "Unauthorized"},
        403: {"model": Error, "description": "Forbidden"},
        404: {"model": Error, "description": "Not Found"},
        405: {"model": Error, "description": "Method Not allowed"},
        409: {"model": Error, "description": "Conflict"},
        500: {"model": Error, "description": "Internal Server Error"},
    },
    tags=["resource"],
    summary="Deletes a Resource",
)
async def delete_resource(
    id: str = Path(None, description="Identifier of the Resource"),
) -> None:
    """This operation deletes a Resource entity."""
    ...
    return({"Nope":"Agent does not do DELETE yet"})



@router.get(
    "/resource",
    responses={
        200: {"model": List[Resource], "description": "Success"},
        400: {"model": Error, "description": "Bad Request"},
        401: {"model": Error, "description": "Unauthorized"},
        403: {"model": Error, "description": "Forbidden"},
        404: {"model": Error, "description": "Not Found"},
        405: {"model": Error, "description": "Method Not allowed"},
        409: {"model": Error, "description": "Conflict"},
        500: {"model": Error, "description": "Internal Server Error"},
    },
    tags=["resource"],
    summary="List or find Resource objects",
)
async def list_resource(
    fields: str = Query(None, description="Comma-separated properties to be provided in response"),
    offset: int = Query(None, description="Requested index for start of resources to be provided in response"),
    limit: int = Query(None, description="Requested number of resources to be provided in response"),
) -> List[Resource]:
    ...
    return({"Nope":"Agent does not do GET yet"})


@router.patch(
    "/resource/{id}",
    responses={
        200: {"model": Resource, "description": "Updated"},
        400: {"model": Error, "description": "Bad Request"},
        401: {"model": Error, "description": "Unauthorized"},
        403: {"model": Error, "description": "Forbidden"},
        404: {"model": Error, "description": "Not Found"},
        405: {"model": Error, "description": "Method Not allowed"},
        409: {"model": Error, "description": "Conflict"},
        500: {"model": Error, "description": "Internal Server Error"},
    },
    tags=["resource"],
    summary="Updates partially a Resource",
)
async def patch_resource(
    id: str = Path(None, description="Identifier of the Resource"),
    resource: ResourceUpdate = Body(None, description="The Resource to be updated"),
) -> Resource:
    """This operation updates partially a Resource entity."""
    ...
    print("Lets patch something")
    #Basically we have to check whether there is an action ResourceCharacteristic
    #Lets create a temp Resource
    #TODO: Check for each member value (if exists)
    newResource=Resource(id=str(uuid.uuid1()),href="")
    newResource.category=resource.category
    newResource.name=resource.name
    newResource.description=resource.description
    
    newResource.resource_characteristic=resource.resource_characteristic
    action_present=None
    for characteristic in newResource.resource_characteristic:
        characteristic.id=str(uuid.uuid1())
        #Check if there is an action
        if(characteristic.name=="action"):
            main.fileHandler.action_present=characteristic.value["value"]
        #Check if there is an action
        if(characteristic.name=="action_parameters"):
            main.fileHandler.action_params=characteristic.value["value"]


    if main.fileHandler.action_params is not None:
            main.fileHandler.write_conf_file()

    if main.fileHandler.allowed_actions is not None:
        print("--------------->")
        print(main.fileHandler.allowed_actions)
        if main.fileHandler.action_present  not in main.fileHandler.allowed_actions:
            print("Yeah I do not how to do this.... ")
            print(main.fileHandler.action_present)
            return None



    #TODO: Check for success/fail of command
    return newResource


@router.get(
    "/resource/{id}",
    responses={
        200: {"model": Resource, "description": "Success"},
        400: {"model": Error, "description": "Bad Request"},
        401: {"model": Error, "description": "Unauthorized"},
        403: {"model": Error, "description": "Forbidden"},
        404: {"model": Error, "description": "Not Found"},
        405: {"model": Error, "description": "Method Not allowed"},
        409: {"model": Error, "description": "Conflict"},
        500: {"model": Error, "description": "Internal Server Error"},
    },
    tags=["resource"],
    summary="Retrieves a Resource by ID",
)
async def retrieve_resource(
    id: str = Path(None, description="Identifier of the Resource"),
    fields: str = Query(None, description="Comma-separated properties to provide in response"),
) -> Resource:
    """This operation retrieves a Resource entity. Attribute selection is enabled for all first level attributes."""
    ...
    return({"Nope":"Agent does not do /id  GET yet"})