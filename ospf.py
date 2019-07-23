from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml
from LabConnection import *
import threading
from init import *

class Ospf :


  def init_ospf(self):

    threads = []
    l = LabConnection() 
    with open('yamlfiles/'+'console.yaml') as f:
        o = yaml.safe_load(f)
        print "Configuring ospf on all routers"
        for router in o["routermapping"]:
            commands = l.render('ospf_init.j2',router+'.yaml')
            threads.append(threading.Thread(target=l.push,args=(o["gnsip"],o["routermapping"][router],commands,router,)))

    for t in threads:
         t.start()

    for t in threads:
         t.join()

  def remove_ospf(self):
       threads = []
       l = LabConnection()
       print "Removing ospf from all routers"
       with open('yamlfiles/' + 'console.yaml') as f:
         o = yaml.safe_load(f)
         for router in o["routermapping"]:
            commands = ['no router ospf 1'] 
            threads.append(threading.Thread(target=l.push,args=(o["gnsip"],o["routermapping"][router],commands,router,)))


       for t in threads:
         t.start()


       for t in threads:
         t.join()

       print "Removed OSPF from all routers"

    

