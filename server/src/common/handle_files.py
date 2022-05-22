import json

from openapi_server.models.resource_create import ResourceCreate
from openapi_server.models.resource_update import ResourceUpdate
from openapi_server.models.characteristic import Characteristic

from openapi_server.models.resource_administrative_state_type import ResourceAdministrativeStateTypeEnum
from openapi_server.models.resource_operational_state_type import ResourceOperationalStateTypeEnum
from openapi_server.models.resource_status_type import ResourceStatusTypeEnum
from openapi_server.models.resource_usage_state_type import ResourceUsageStateTypeEnum

from  openapi_server import callbacks
import inspect

import string
import random

import requests

import os

class FileHandler:
    def __init__(self):
        self.agent_conf_file="agent_conf.cfg"
        self.gnodeb_conf_file="../../myconf.cfg"
        self.action_params=None
        self.action_present=None
        self.allowed_actions=list()
        self.commands=dict()
        self.allowed_params=None
        self.resource_data=None
        self.server=None
        self.resourceID=None
        self.registered=None
        self.resource_status=None #Status of the resource
        self.resource=None #this will be the resource obj
        
          
    def read_conf(self):
        with open(self.agent_conf_file, "r") as jsonfile:
            data = json.load(jsonfile)
            if "server" in data:
                self.server=data["server"]
            if "commands" in data:
                self.commands=data["commands"]
                for key in data["commands"]:
                    self.allowed_actions.append(key)
            self.allowed_params=data["allowed_params"]
            if "resource_data" in data:
                self.resource_data=data["resource_data"]
            if "resourceID" in data:
                self.resourceID=data["resourceID"]
            if "resource_status" in data:
                self.resource_status=data["resource_status"]
            if "Registered" in data:
                self.registered=data["Registered"]

        
    


    def write_conf_file(self):
        if self.action_params is not None:
        #clear file contents
            with open("../../myconf.cfg", 'r+') as conf:
                conf.truncate(0)

            #start wirtitng file
            for param in self.action_params:
                if param in self.allowed_params:
                    with open("../../myconf.cfg", mode="a") as conf:
                        if param in ["PRMT_AMF_ADDR","PRMT_GTP_ADDR" , "PRMT_PLMN" , "PRMT_MOD_UL" , "PRMT_MOD_DL"]:
                            conf.write("#define  {} \"{}\"\n".format(param,self.action_params[param]))
                        else:
                            conf.write("#define  {} {}\n".format(param,self.action_params[param]))

                else:
                    print("Yeah  this param is not available... ",param)


    #create a resource in order to register
    def __createResource(self):
        #TODO: Check if entries exist in cfg
        #create a random name so that DB does not get an error when testing
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits +string.ascii_lowercase, k = 5))    
        print(self.resource_data)
        #selfResource=ResourceCreate(name=self.resource_data["name"]+ran)
        #Send fixed name. This must be unique
        selfResource=ResourceCreate(name=self.resource_data["name"],)
        selfResource.category=self.resource_data["category"]
        selfResource.description=self.resource_data["description"]
        selfResource.resource_version="0.0.1"
        selfResource.resource_characteristic=[]
        if "ip" in self.resource_data:
            resourceIP_Char=Characteristic(name="IP",value={"value":self.resource_data["ip"]})
            resourceIP_Char.id="string"
            resourceIP_Char.value_type="string"
            selfResource.resource_characteristic.append(resourceIP_Char)
        if "location" in self.resource_data:
            resourceLoc_Char=Characteristic(name="location",type="array",value={"value":self.resource_data["location"]})
            resourceLoc_Char.id="string"
            resourceLoc_Char.value_type="array"
            selfResource.resource_characteristic.append(resourceLoc_Char)
        #Add gtp iface addres to suppoort multiple amfs
        if "gtp_iface" in self.resource_data:
            gtp_iface_Char=Characteristic(name="gtp_iface",value={"value":self.resource_data["gtp_iface"]})
            gtp_iface_Char.id="string"
            gtp_iface_Char.value_type="string"
            selfResource.resource_characteristic.append(gtp_iface_Char)


        if self.allowed_actions is not None:
            resourceAction_Char=Characteristic(name="supported_actions",type="list",value={"value":self.allowed_actions})  
            resourceAction_Char.id="string"
            resourceAction_Char.value_type="list"
            selfResource.resource_characteristic.append(resourceAction_Char)   
            print("Lets see if we have anything to register") 
            #register callbacks
            for action in self.allowed_actions:
                cmd2run=self.commands[action]
                if cmd2run is None:
                    myCB=action
                    if (hasattr(callbacks, myCB) and inspect.isfunction(getattr(callbacks, myCB))):
                        callbacks.register_callback(action, getattr(callbacks, action))
                    else:
                        print("No callback to register for-->",myCB)


        if self.resource_status:
            print("DDDDDDDDDDDDD")
            #TODO: if the key is erroneous in agetn_Cfg (i.e. state=unlked) there is an excpetion. Must fix it
            administrative_state=ResourceAdministrativeStateTypeEnum[self.resource_status["administrativeState"]].value if "administrativeState" in self.resource_status else None
            operational_state=ResourceOperationalStateTypeEnum[self.resource_status["operationalState"]].value if "administrativeState" in self.resource_status else None
            resource_status=ResourceStatusTypeEnum[self.resource_status["resourceStatus"]].value if "administrativeState" in self.resource_status else None
            usage_state=ResourceUsageStateTypeEnum[self.resource_status["usageState"]].value if "administrativeState" in self.resource_status else None
            selfResource.administrative_state=administrative_state
            selfResource.operational_state=operational_state
            selfResource.resource_status=resource_status
            selfResource.usage_state=usage_state
            print("******************")
        return selfResource   

    def __alreadyRegistered(self):
            print("Seems we are registered already")
            #TODO: At this point we should send a GET to the server with our ID to create the selfResourse
            #If the GET fails (i.e. the server has deleted us) we should register again
            #If the device exists we should check whether there is any configuration change locally and PATCH if required
            #As a QnD solution, lets PATCH every time. Jsu change operational_state field
            # print("LEts PATCH and change operational_state to show we are live")
            # resourcePATCH=self.__createResource()
            #reregister callbacks
            for action in self.allowed_actions:
                cmd2run=self.commands[action]
                if cmd2run is None:
                    myCB=action
                    if (hasattr(callbacks, myCB) and inspect.isfunction(getattr(callbacks, myCB))):
                        callbacks.register_callback(action, getattr(callbacks, action))
                    else:
                        print("No callback to register for-->",myCB)
            resourcePATCH=ResourceUpdate( operational_state=ResourceOperationalStateTypeEnum["enable"].value, resource_status=ResourceStatusTypeEnum["available"].value)
            x = requests.patch(self.server+"/resource/"+self.resource_data["name"], data=resourcePATCH.json() )
            #TODO: check response


    #This will create the request to self register
    def selfRegister(self):
        print("Trying to self register")
        #check if registered already
        if  self.registered:
            self.__alreadyRegistered()
            return

        selfResource=self.__createResource() 
                
        #TODO check that server is actually there
        if self.server is not None:
            #Send post req to server
            #TODO: check that IP has http in front otherwise add it
            print(selfResource)
            try:
                x = requests.post(self.server+"/resource", data=selfResource.json() )
                if(x.status_code==201):
                    print("Self register success")
                    if "id" in x.json():
                        self.resourceID=x.json()["id"]

                        tmpData=None
                        with open(self.agent_conf_file, 'r') as jsonfile:
                            tmpData = json.load(jsonfile)
                            tmpData["Registered"]=True
                            tmpData["resourceID"]=self.resourceID

                        os.remove(self.agent_conf_file)
                        with open(self.agent_conf_file, 'w') as jsonfile:
                            json.dump(tmpData, jsonfile, indent=4)

                        #all good
                        self.resource=selfResource

                    else:
                        print("This is strange")
                #When a device with the same name has already been registered
                # 409 Conflict is returned buy the server. 
                elif (x.status_code==409):
                    print("Conflict. Same device name already registered")
                else:
                    #TODO: Check what went wring and handle
                    print("Oooops")
            except requests.exceptions.RequestException as e:
                print("OOOPS")
                print(repr(e))


  #This will create the request to self unregister
    def unregister(self):
        print("Trying to self unregister")
        #TODO: At this point we should send a GET to the server with our ID to create the selfResourse
        #If the GET fails (i.e. the server has deleted us) we should register again
        #If the device exists we should check whether there is any configuration change locally and PATCH if required
        #As a QnD solution, lets PATCH every time. Jsu change operational_state field
        # print("LEts PATCH and change operational_state to show we are NOT live")
        # resourcePATCH=self.__createResource()
        resourcePATCH=ResourceUpdate(  operational_state=ResourceOperationalStateTypeEnum["disable"].value,resource_status=ResourceStatusTypeEnum["unknown"].value)
        x = requests.patch(self.server+"/resource/"+self.resource_data["name"], data=resourcePATCH.json() )
        #TODO: check response