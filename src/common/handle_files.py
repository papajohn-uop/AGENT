import json

from openapi_server.models.resource_create import ResourceCreate
from openapi_server.models.characteristic import Characteristic

import string
import random

class FileHandler:
    def __init__(self):
        self.agent_conf_file="agent_conf.cfg"
        self.gnodeb_conf_file="../../myconf.cfg"
        self.action_params=None
        self.action_present=None
        self.allowed_actions=dict()
        self.allowed_params=None
        self.resource=None
          
    def read_conf(self):
        with open(self.agent_conf_file, "r") as jsonfile:
            data = json.load(jsonfile)
            for key in data["commands"]:
                self.allowed_actions[key]=data["commands"][key]
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
        selfResource.resource_characteristic=[]
        if "ip" in self.resource:
            resourceIP_Char=Characteristic(name="IP",type="string",value={"value":self.resource["ip"]})
            selfResource.resource_characteristic.append(resourceIP_Char)
        if "location" in self.resource:
            resourceLoc_Char=Characteristic(name="IP",type="array",value={"value":self.resource["location"]})
            selfResource.resource_characteristic.append(resourceLoc_Char)    
        print(selfResource)

        if self.allowed_actions is not None:
            resourceAction_Char=Characteristic(name="supported_actions",type="list",value={"value":self.allowed_actions})  
            selfResource.resource_characteristic.append(resourceAction_Char)    
        


        print(selfResource.json())