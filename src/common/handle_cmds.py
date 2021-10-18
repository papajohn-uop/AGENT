import json

class CmdHandler:
    def __init__(self):
        self.action=None
        self.action_command=None


    def executeCMD(self):
        print("Execute a cmd")
        print("***********")
        print(self.action)
        print(self.action_command)
        print("***********")


