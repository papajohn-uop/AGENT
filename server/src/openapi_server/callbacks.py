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
#    process = subprocess.Popen(["echo \"", action_command,"\" >>./test.txt"],
    print(type(action_command))
    print(action_command)
    process = subprocess.Popen(["echo \""+ str(action_command)+"\" >./pipe_cmd.txt"],
    #process = subprocess.Popen([action_command],
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
# def echo():
#     _execCMD("echo $(date -u) >> nikos.txt")


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
    # _execCMD("echo touch > ./docker_command.txt ")    
    # _execCMD("ls -la")    


def echo():
    _execCMD("echo 1 >>./test.txt ")    
    #_execCMD("echo \"echo docker >>./test.txt\" >test_docker.txt ")    
    # _execCMD("echo  $(date -u) >>./test.txt ")    
    # _execCMD("sh ./script_in_host.sh ")    
    # _execCMD("echo 2 >>./test.txt ")    
    #_execCMD("./script_on_host.sh ")    
    #_execCMD("../script_on_host_parent.sh ")    
    # _execCMD("echo 3 >>./test.txt ")    
########################


def set_generic_config():
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