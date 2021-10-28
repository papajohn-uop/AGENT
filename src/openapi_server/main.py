# coding: utf-8

"""
    API Resource Inventory Management

    ## TMF API Reference: TMF639 - Resource Inventory   ### Release : 19.5 - December 2019  Resource Inventory  API goal is to provide the ability to manage Resources.  ### Operations Resource Inventory API performs the following operations on the resources : - Retrieve an entity or a collection of entities depending on filter criteria - Partial update of an entity (including updating rules) - Create an entity (including default values and creation rules) - Delete an entity (for administration purposes) - Manage notification of events

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""


from fastapi import FastAPI

# from openapi_server.apis.events_subscription_api import router as EventsSubscriptionApiRouter
# from openapi_server.apis.notification_listeners__client_side_api import router as NotificationListenersClientSideApiRouter
from openapi_server.apis.resource_api import router as ResourceApiRouter

from  common import handle_files,handle_cmds


app = FastAPI(
    title="AGENT API Resource Inventory Management",
    description="## TMF API Reference: TMF639 - Resource Inventory   ### Release : 19.5 - December 2019  Resource Inventory  API goal is to provide the ability to manage Resources.  ### Operations Resource Inventory API performs the following operations on the resources : - Retrieve an entity or a collection of entities depending on filter criteria - Partial update of an entity (including updating rules) - Create an entity (including default values and creation rules) - Delete an entity (for administration purposes) - Manage notification of events",
    version="4.0.0",
)

# app.include_router(EventsSubscriptionApiRouter)
# app.include_router(NotificationListenersClientSideApiRouter)
app.include_router(ResourceApiRouter)


fileHandler=handle_files.FileHandler()
cmdHandler=handle_cmds.CmdHandler()

@app.on_event("startup")
async def startup_event():
    print("****************************************************") 
    print("*Start up")
    print("*Steps to take:")
    print("*Initialize self (read from text files)")
    print("*Self register")
    print("****Create Resource for self register")
    print("****************************************************") 

    fileHandler.read_conf()
    fileHandler.selfRegister()

    
    

@app.on_event("shutdown")
def shutdown_event():
   print("****************************************************") 
   print("Shut down")
   print("Unregister")
   print("****************************************************") 
   with open("../log.txt", mode="a") as log:
       log.write("Application shutdown")