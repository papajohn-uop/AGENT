import json
import subprocess

class CmdHandler:
    def __init__(self):
        self.action=None
        self.action_command=None


    def _execCMD(self):
        #process = subprocess.Popen(['echo', self.action_command], 
        print("--->0")
        process = subprocess.Popen([self.action_command],
                           #we need shell= true to pass the command as string and not as list
                           shell=True, 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
        print("--->1")
        while True:
            print("--->2")
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    print(output.strip())
                break



    def executeCMD(self):
        print("Execute a cmd")
        print("***********")
        print(self.action)
        print(self.action_command)
        print("***********")
        self._execCMD()


