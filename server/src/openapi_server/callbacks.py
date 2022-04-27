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
    _execCMD("echo 'papajohn' >>./test.txt ; echo $(date -u) >>./test.txt ")    
    #_execCMD("echo \"echo docker >>./test.txt\" >test_docker.txt ")    
    # _execCMD("echo  $(date -u) >>./test.txt ")    
    # _execCMD("sh ./script_in_host.sh ")    
    # _execCMD("echo 2 >>./test.txt ")    
    #_execCMD("./script_on_host.sh ")    
    #_execCMD("../script_on_host_parent.sh ")    
    # _execCMD("echo 3 >>./test.txt ")    
########################

TARGET_PATH="~/Amarisoft_LTE/enb/config/"
TARGET_FILE="dummy_link_gnb.cfg "
def changeConf(config):
    cmd="echo 'Uplink Configuration' >>./test.txt ; "
    cmd=cmd + "ln -sf " 
    cmd=cmd + TARGET_PATH
    cmd=cmd + config
    cmd=cmd + TARGET_PATH 
    cmd=cmd + TARGET_FILE
    print("in change conf")
    print(cmd)
    return cmd

def ul_config():
    cmd=changeConf("LimeNet5G_N78_UL.cfg ")
    _execCMD(cmd)
    # _execCMD("echo 'Uplink Configuration' >>./test.txt ; ln -sf ~/Amarisoft_LTE/enb/config/LimeNet5G_N78_UL.cfg ~/Amarisoft_LTE/enb/config/dummy_link_gnb.cfg ")    

def st_config():
    cmd=changeConf("LimeNet5G_N78.cfg ")
    _execCMD(cmd)
    # _execCMD("echo 'Standard Configuration' >>./test.txt ; ln -sf ~/Amarisoft_LTE/enb/config/LimeNet5G_N78.cfg ~/Amarisoft_LTE/enb/config/dummy_link_gnb.cfg")    

def ulmimo_config():
    cmd=changeConf("LimeNet5G_N78_UL_MIMO.cfg ")
    _execCMD(cmd)
    # _execCMD("echo 'Uplink Mimo Configuration' >>./test.txt ;  ln -sf ~/Amarisoft_LTE/enb/config/LimeNet5G_N78_UL_MIMO.cfg ~/Amarisoft_LTE/enb/config/dummy_link_gnb.cfg ")    


def twoslice_config():
    cmd=changeConf("LimeNet5G_N78_2slices.cfg ")
    _execCMD(cmd)
    # _execCMD("echo 'Two slice Configuration' >>./test.txt ;  ln -sf ~/Amarisoft_LTE/enb/config/LimeNet5G_N78_2slices.cfg ~/Amarisoft_LTE/enb/config/dummy_link_gnb.cfg ")    


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