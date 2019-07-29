from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml
from LabConnection import *
import threading
from eigrp import *
from ospf import *
from gns3 import *
from bgp import *
import requests,json,time,os

e = Eigrp()
l = LabConnection()
o = Ospf()
g = Gns3()
b = BGP()

def start(device):
   g.start(device)


def stop(device):
   g.stop(device)

def stop_all():
   g.stop_all()

def start_all():
   g.start_all()


def reset_lab():
    g.stop_all()
    g.start_all()
    g.time.sleep(4)

def init_L2_switch():
    l = LabConnection()
    commandset = []    
    for i in range(0,4):
        for j in range(0,4):
            command = ['int Et'+str(i)+'/'+str(j), 'switchport trunk encapsulation dot1q','switchport mode trunk']
            commandset = commandset + command

    with open('yamlfiles/console.yaml') as f:

        o = yaml.safe_load(f)
        for vlan in o["vlans"]:
            commandset.append('vlan ' + str(vlan))
        l.push(o["gns3_vmware_ip"],o["switchmapping"]["Sw0"],commandset,"L2Switch")


def init_routers():

   l = LabConnection()
   threads = []
   with open("yamlfiles/console.yaml") as f:
        o = yaml.safe_load(f)
        for router in o["routermapping"]:
            print "initializing", router
            commands = l.render('init.j2',router+".yaml")
            threads.append(threading.Thread(target=l.push, args=(o["gns3_vmware_ip"],o["routermapping"][router],commands,router)))

   for t in threads :
        t.start()

   for t in threads:
        t.join()


def init_lab():
   init_L2_switch()
   init_routers()


def send(routers,command):
   l.output(routers,command)    
 

def init_eigrp():
   init_lab()
   e.init_eigrp()


def remove_eigrp():
   e.remove_eigrp()

def init_ospf():
   init_lab()
   o.init_ospf()

def remove_ospf():
   o.remove_ospf()


def load(lab,routers):
   g.reset_lab()
   init_L2_switch()
   if routers == 'all':
       routers = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']
   commands = {} 
   final_commands = {}
   for r in routers:
       final_commands[r] = ['']
   path = "configs/ine.ccie.rsv5.workbook.initial.configs/advanced.technology.labs/" + lab + '/'
   for r in routers:
       with open(path+r+'.txt') as f :
        commands[r] = f.readlines()
        for command in commands[r]:
            final_commands[r].append(command.replace('GigabitEthernet1','Ethernet0/0'))
   threads = []
   with open('yamlfiles/console.yaml') as f:
       o = yaml.safe_load(f)
       print "loading " + lab
       for router in routers:
        threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][router],final_commands[router],router))) 
   for t in threads:
         t.start()

   for t in threads:
         t.join()

   send('all',['int Ethernet 0/0','no shut'])

def input_commands():
    print "Enter/Paste your commands. Ctrl-D to save it."
    contents = []
    while True:
     try:
        line = raw_input("")
     except EOFError:
        break
     contents.append(line)
    return contents
#def remove_ospf():



def save_lab():
    print "Saving lab"



def lslab(lab=None):
   if lab is None:
       command = "ls configs/ine.ccie.rsv5.workbook.initial.configs/advanced.technology.labs"
   else:   
       command = 'ls configs/ine.ccie.rsv5.workbook.initial.configs/advanced.technology.labs | grep ' + lab
   os.system(command)


def init_bgp():
  b.init_bgp()


def bgp_topo():
  b.bgp_topo()
  
