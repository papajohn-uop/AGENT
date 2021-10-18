import json

class FileHandler:
    def __init__(self):
        self.agent_conf_file="agent_conf.cfg"
        self.gnodeb_conf_file="../../myconf.cfg"
        self.action_params=None
        self.action_present=None
        self.allowed_actions=list()
        self.allowed_params=None
          
    def read_conf(self):
        with open(self.agent_conf_file, "r") as jsonfile:
            data = json.load(jsonfile)
            for key in data["commands"]:
                self.allowed_actions.append(key)
            self.allowed_params=data["allowed_params"]
    


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
