import json

from openapi_server.models.resource_create import ResourceCreate
from openapi_server.models.characteristic import Characteristic

import string
import random

import requests

class FileHandler:
    def __init__(self):
        self.agent_conf_file="agent_conf.cfg"
        self.gnodeb_conf_file="../../myconf.cfg"
        self.action_params=None
        self.action_present=None
        self.allowed_actions=list()
        self.commands=dict()
        self.allowed_params=None
        self.resource=None
        self.server=None
        self.resourceID=None
          
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
            if "resource" in data:
                self.resource=data["resource"]
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

    #This will create the request to self register
    def selfRegister(self):
        print("Trying to self register")
        #TODO: Check if entries exist in cfg
        #create a random name so that DB does not get an error when testing
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits +string.ascii_lowercase, k = 5))    
        selfResource=ResourceCreate(name=self.resource["name"]+ran)
        selfResource.category=self.resource["category"]
        selfResource.description=self.resource["description"]
        selfResource.resource_version="0.0.1"
        selfResource.resource_characteristic=[]
        if "ip" in self.resource:
            resourceIP_Char=Characteristic(name="IP",value={"value":self.resource["ip"]})
            resourceIP_Char.id="string"
            resourceIP_Char.value_type="string"
            selfResource.resource_characteristic.append(resourceIP_Char)
        if "location" in self.resource:
            resourceLoc_Char=Characteristic(name="location",type="array",value={"value":self.resource["location"]})
            resourceLoc_Char.id="string"
            resourceLoc_Char.value_type="array"
            selfResource.resource_characteristic.append(resourceLoc_Char)    
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
            print(x.reason)
            print(x.status_code)
            if(x.status_code==200):
                print("Self register success")
                # print(x.text)
                # print(x.json())
                if "id" in x.json():
                    print(x.json()["id"])
                    self.resourceID=x.json()["id"]
                    print(self.resourceID)
                else:
                    print("This is strange")
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
