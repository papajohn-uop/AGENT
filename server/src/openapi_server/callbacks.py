import json
import subprocess

# global variable containing callbacks
callbacks = {}

# API for registering callbacks
def register_callback(event, callback):
    if event not in callbacks:
        callbacks[event] = callback

# a function that is called when some event is triggered on an object
def process_event(event):
    if  event in callbacks:
        # this object/event pair has a callback, call it
        callback = callbacks[event]
        print("Callback registered-->", callback)
        callback()
    else:
        print("No callback registered")


def _execCMD(action_command):
    print(type(action_command))
    print(action_command)
    process = subprocess.Popen([action_command],
                        #we need shell= true to pass the command as string and not as list
                        shell=True, 
                        stdout=subprocess.PIPE,
                        universal_newlines=True)
    while True:
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



'''
  "start": "service lte start",
        "restart": "service lte restart",
        "stop": "service lte stop",
        "status": "service lte status",
        "touch": "touch nikos.txt",
'''
def start():
    _execCMD("sudo /home/lime/5G_SA_service_start.sh")

def restart():
    _execCMD("sudo /home/lime/5G_SA_service_start.sh")

def stop():
    _execCMD("sudo /home/lime/5G_SA_service_stop.sh")

def status():
    _execCMD("service lte status")    

def touch():
    _execCMD('touch ./test.txt ')    



def echo():
    _execCMD("echo 'papajohn' >>./test.txt ; echo $(date -u) >>./test.txt ")    

########################

