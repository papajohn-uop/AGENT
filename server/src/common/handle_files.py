import json

from openapi_server.models.resource_create import ResourceCreate
from openapi_server.models.characteristic import Characteristic

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
            if "Registered" in data:
                self.registered=data["Registered"]
        print("----------->")
        print(data["commands"])
        print("----------->")
        print(self.allowed_actions)
        
    


    def write_conf_file(self):
        if self.action_params is not None:
        #clear file contents
            with open("../../myconf.cfg", 'r+') as conf:
                conf.truncate(0)

            #start wirtitng file
            for param in self.action_params:
                if param in self.allowed_params:
                    with open("../../myconf.cfg", mode="a") as conf:
                        conf.write("#define {} {}\n".format(param,self.action_params[param]))

                else:
                    print("Yeah  this param is not available... ",param)


    #create a resource in order to register
    def __createResource(self):
        #TODO: Check if entries exist in cfg
        #create a random name so that DB does not get an error when testing
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits +string.ascii_lowercase, k = 5))    
        print(self.resource_data)
        selfResource=ResourceCreate(name=self.resource_data["name"]+ran)
        #Send fixed name. This must be unique
        selfResource=ResourceCreate(name=self.resource_data["name"])
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
        return selfResource   

    #This will create the request to self register
    def selfRegister(self):
        print("Trying to self register")
        #check if registered already
        if  self.registered:
            print("Seems we are registered already")
            #TODO: At this point we should send a GET to the server with our ID to create the selfResourse
            #If the GET fails (i.e. the server has deleted us) we should register again
            print(self.resource)
            return

        selfResource=self.__createResource() 
        print(selfResource)

        if self.allowed_actions is not None:
            resourceAction_Char=Characteristic(name="supported_actions",type="list",value={"value":self.allowed_actions})  
            resourceAction_Char.id="string"
            resourceAction_Char.value_type="list"
            selfResource.resource_characteristic.append(resourceAction_Char)    

        print(selfResource.json())
                
        #TODO check that server is actually there
        if self.server is not None:
            print(self.server)
            #Send post req to server
            #TODO: check that IP has http in front otherwise add it
            x = requests.post(self.server+"/resource", data=selfResource.json() )
            print("request complete")
            print(x)
            print(x.reason)
            print(x.status_code)
            if(x.status_code==201):
                print("Self register success")
                # print(x.text)
                # print(x.json())
                if "id" in x.json():
                    print(x.json()["id"])
                    self.resourceID=x.json()["id"]
                    print(self.resourceID)

                    tmpData=None
                    with open(self.agent_conf_file, 'r') as jsonfile:
                        tmpData = json.load(jsonfile)
                        tmpData["Test"]="Test"
                        tmpData["Registered"]=True
                        tmpData["resourceID"]=self.resourceID

                    os.remove(self.agent_conf_file)
                    with open(self.agent_conf_file, 'w') as jsonfile:
                        json.dump(tmpData, jsonfile, indent=4)

                    #all good
                    self.resource=selfResource
                    print(self.resource)

                else:
                    print("This is strange")
            #When a device with the same name has already been registered
            # 409 Conflict is returned buy the server. 
            elif (x.status_code==409):
                print("Conflict. Same device name already registered")
            else:
                #TODO: Check what went wring and handle
                print("Oooops")


  #This will create the request to self unregister
    def unregister(self):
        print("Trying to self unregister")
        #TODO: Check if entries exist in cfg
        #create a random name so that DB does not get an error when testing
           
        #TODO check that server is actually there
        if self.server is not None:
            print(self.server)
            #Send post req to server
            #TODO: check that IP has http in front otherwise add it
            x = requests.delete(self.server+"/resource/"+self.resourceID )
            print("request complete")
            print(x.reason)
            print(x.status_code)
            if(x.status_code==200):
                print("Self unregister success")
               
            else:
                #TODO: Check what went wring and handle
                print("Oooops")
