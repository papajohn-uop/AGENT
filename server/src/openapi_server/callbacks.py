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
    #process = subprocess.Popen(['echo', self.action_command], 
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


########################
def echo():
    _execCMD("echo $(date -u) >> nikos.txt")


'''
  "start": "service lte start",
        "restart": "service lte restart",
        "stop": "service lte stop",
        "status": "service lte status",
        "touch": "touch nikos.txt",
'''
def start():
    _execCMD("service lte start")

def restart():
    _execCMD("service lte restart")

def stop():
    _execCMD("service lte stop")

def status():
    _execCMD("service lte status")    
########################


def set_generic_config():
    print("FFF")
    _execCMD("echo 'SET_GENERIC_CONFIG_FROM_CALLBACK' >> nikos.txt")


def myCallBack_2():
    print ("Callback2!")

def myCallBack_3():
    print ("Callback3!")


def cmd2():
    print ("\n\nCMD2 CB\n\n")


#register_callback("event1",myCallBack_1)


# call the onclick() method when the 'click' event happens on the button
#some_api.register_callback(button, 'click', onclick)

# print("Here...")
# print(callbacks)
# process_event("event1")
# process_event("event2")