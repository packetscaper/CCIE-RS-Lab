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
import pprint

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
    time.sleep(4)

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
            print("initializing", router)
            commands = l.render('init.j2',router+".yaml")
            threads.append(threading.Thread(target=l.push, args=(o["gns3_vmware_ip"],o["routermapping"][router],commands,router)))

   for t in threads :
        t.start()

   for t in threads:
        t.join()


def init_lab():
   stop_all()
   start_all()
   time.sleep(10)
   init_routers()


def send(routers,command):
   l.output(routers,command)    
 

def init_eigrp():
   init_lab()
   e.init_eigrp()

def init_ospf():
   stop_all()
   start_all()
   time.sleep(12)
   o.init_ospf()

def load_lab(devices,lab):
   g.reset_lab()
   threads = []
   threads.append(threading.Thread(target=init_L2_switch))
   if devices == 'all':
       devices = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10','SW1','SW2','SW3','SW4']
   commands = {} 
   final_commands = {}
   for d in devices:
       final_commands[d] = ['']
   path = "configs/ine.ccie.rsv5.workbook.initial.configs/advanced.foundation.labs/" + lab + '/'
   for d in devices:
     try:
       with open(path+d+'.txt') as f :
        commands[d] = f.readlines()
        for command in commands[d]:
            final_commands[d].append(command.replace('GigabitEthernet1','Ethernet0/0'))

     except IOError:
        print("No config found for" , d)
         
   with open('yamlfiles/console.yaml') as f:
       o = yaml.safe_load(f)
       print ("loading " + lab)
       for d in devices:
           if 'R' not in d:
             threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["switchmapping"][d],final_commands[d],d))) 
           else:
             threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][d],final_commands[d],d))) 

   time.sleep(5) 
 
   for t in threads:
         t.start()

   for t in threads:
         t.join()

   send('all',['int Ethernet 0/0','no shut'])

def load_lab_config(lab):
    threads = []
    with open("yamlfiles/excercies/"+lab) as f:
       tasks = yaml.load(f)
    with open('yamlfiles/console.yaml') as f:
       o = yaml.safe_load(f)
    for task in tasks:
  
      print("configuring ", task )
      config = tasks[task]
      for c in config:
            if 'R' in c:
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][c],config[c],c)))
            else :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["switchmapping"][c],config[c],c)))
 
    for t in threads:
         t.start()

    for t in threads:
         t.join()
    time.sleep(3)
    #routers = []
    #for c in config:
    #    if c != 'verify':
    #     routers.append(c) 
    
    #send(routers,config["verify"])
 
def load_config(config_dict):
    threads = []
    config= config_dict 
    with open('yamlfiles/console.yaml') as f:
       o = yaml.safe_load(f)
    for c in config:
        if c != 'verify':
            if 'R' in c:
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][c],config[c],c)))
            else :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["switchmapping"][c],config[c],c)))
 
    for t in threads:
         t.start()

    for t in threads:
         t.join()
    time.sleep(3)
    routers = []
    for c in config:
        if c != 'verify':
         routers.append(c) 
    
    send(routers,config["verify"])
 

def lslab(lab=None):
   if lab is None:
       command = "ls configs/ine.ccie.rsv5.workbook.initial.configs/advanced.foundation.labs"
   else:   
       command = 'ls configs/ine.ccie.rsv5.workbook.initial.configs/advanced.foundation.labs | grep ' + lab
   os.system(command)
   
def lslabconfig(topic=None,lab=None):
    if topic == None and lab == None :
     os.system('ls configs/ine.ccie.rsv5.workbook.initial.configs/advanced.foundation.labs/labs/')
    if topic != None and lab==None:
     os.system('ls configs/ine.ccie.rsv5.workbook.initial.configs/advanced.foundation.labs/labs/'+str(topic))
    if topic != None and lab != None :
     os.system('cat configs/ine.ccie.rsv5.workbook.initial.configs/advanced.foundation.labs/labs/'+str(topic) + '/' + str(lab))


def start_packet_capture(devices):
    threads = []
    with open("yamlfiles/packetcapture.yaml") as f:
        c = yaml.safe_load(f)
        commands = c["start"]
    for d in devices:
        with open('yamlfiles/console.yaml') as f:
         o = yaml.safe_load(f)
         if 'R' in d :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][d],commands,d)))
         else :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["switchmapping"][d],commands,d)))


    for t in threads:
         t.start()

    for t in threads:
         t.join()


def stop_packet_capture(devices):

    threads = []
    with open("yamlfiles/packetcapture.yaml") as f:
        c = yaml.safe_load(f)
        commands = c["stop"]
    for d in devices:
        with open('yamlfiles/console.yaml') as f:
         o = yaml.safe_load(f)
         if 'R' in d :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][d],commands,d)))
         else :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["switchmapping"][d],commands,d)))

    for t in threads:
         t.start()

    for t in threads:
         t.join()


def save_packet_capture(devices):
    print(" enter the file name ")
    input =input()
    threads = []
    commands = 'monitor capture buffer BUF export unix:' + input+'.pcap' 
    for d in devices:
        with open('yamlfiles/console.yaml') as f:
         o = yaml.safe_load(f)
         if 'R' in d :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][d],commands,d)))
         else :
              threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["switchmapping"][d],commands,d)))


    for t in threads:
         t.start()

    for t in threads:
         t.join()

def copy_packet_capture(devices):
    print ("Enter technology")
    tech = input()
    print ("Enter name of the capture")
    name = input()
    with open('topology.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
    for device in devices:
     for node in json_output['topology']['nodes']:
            if node['name'] == device:
                node_id = node['node_id']
                print ("copying captures from ",device)
                os.system('scp gns3@192.168.66.128:/opt/gns3/projects/'+project_id+'/project-files/iou/'+node_id+'/'+name+'.pcap packetcaptures/'+tech+'/'+device) 
                
 



def init_bgp():
   stop_all()
   start_all()
   time.sleep(8)
   b.init_bgp()

def lab():
 
  with open('yamlfiles/excercies/topics.yaml') as f:
      topics = yaml.load(f)

  print (" Choose from following topics")
  for topic_id in topics["topics"] : 
      print ("Enter", topic_id, " for ", topics["topics"][topic_id])
  topic_id = int(input())
  print (" Choose from following subtopic ")
  for subtopic_id in topics["subtopics"][topic_id]:
     print (subtopic_id, " for ", topics["subtopics"][topic_id][subtopic_id])
     
  subtopic_id = int(input())
  with open('yamlfiles/excercies/'+topics["topics"][topic_id]+'.yaml') as f:
      subtopic = topics["subtopics"][topic_id][subtopic_id]
      excercise = yaml.load(f)
  topic = topics["topics"][topic_id] 

  labs = {'bgp': init_bgp, 'mpls': init_lab, 'ospf': init_ospf, 'multicast': init_ospf, 'eigrp': init_eigrp, 'vpn':init_eigrp}
  labs[topic]() 
 
  for p in excercise[subtopic]["problem"] :
       print(p)
  print("press 1 to configure, press 2 to view sol, press any key to load sol")
  user_input = int(input())
  if user_input == 1:
    print ("configure the solution")
  elif user_input == 2 :
    pprint.pprint(excercise[subtopic]['solution'])
  else :
   load_config(excercise[subtopic]['solution'])




def load_config_from():
 
 print ("Enter the filename")
 file_name = input()

 with open("yamlfiles/excercies/workspace/"+file_name) as f:
   c = yaml.safe_load(f)
 print ("loading below configuration")
 pprint.pprint(c)
 time.sleep(5)

 load_config(c)

def r():
    print ("Enter router number ")
    i = input()
    print ("Press Ctrl + ] to exit")
    l.con("R"+i)


def help():
    print ("con() --- For Connecting to routers ")
    print ("lslab() --- For various Labs ")
    print ("lslab('bgp') --- For grep while searching ")
    print ("load_lab('all','multicast.init') --- For loading lab ")
    print ("lslabconfig()   ---- For lab configs ")
    print ("load_lab_config() ---- For loading lab config ")
    print ("lab() ------  For doing lab excercises")
