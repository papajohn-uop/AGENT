
allowed_params=[
        "PRMT_TDD", 
        "PRMT_TDD_CONFIG", 
        "PRMT_N_ANTENNA_DL",  
        "PRMT_BANDWIDTH",
        "PRMT_TX_GAIN",
        "PRMT_RX_GAIN",
        "PRMT_AMF_ADDR",
        "PRMT_GTP_ADDR",
        "PRMT_PLMN",
        "PRMT_TAC",
        "PRMT_MOD_UL",
        "PRMT_MOD_DL",
        "PRMT_BAND",
        "PRMT_NR_ARFCN" 
        ]


allowed_actions={"start":"COMMAND_TO_START","stop":"COMMAND_TO_STOP"}
import json

class FileHandler:
    def __init__(self):
        self.agent_conf_file="agent_conf.cfg"
        self.gnodeb_conf_file="../../myconf.cfg"
        self.action_params=None
        self.action_present=None
        self.allowed_actions=allowed_actions
    
    def read_conf(self):
        with open(self.agent_conf_file, "r") as jsonfile:
            data = json.load(jsonfile)
            print("Read successful")
            print(data)
            print(data["server"])
            print(data["commands"])
            for key in data["commands"]:
                print(key)
                print(data["commands"][key])
            print(data["allowed_params"])
            self.action_params=data["allowed_params"]
            print(self.action_params)



    def write_conf_file(self):
        if self.action_params is not None:
        #clear file contents
            with open("../../myconf.cfg", 'r+') as conf:
                conf.truncate(0)

            #start wirtitng file
            for param in self.action_params:
                if param in allowed_params:
                    print("YEAH. Nice param--->")
                    print("*******************************")
                    print(param,)
                    print("*******************************")
                    print(self.action_params)
                    print("*******************************")
                    print(self.action_params[param])
                    print("*******************************")
                    with open("../../myconf.cfg", mode="a") as conf:
                        conf.write("#define {} {}\n".format(param,self.action_params[param]))

                else:
                    print("Yeah  this param is not available... ",param)
