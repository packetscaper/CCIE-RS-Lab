from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml
from LabConnection import *
import threading
from init import *

class Eigrp :


  def init_eigrp(self):
    threads = []
    l = LabConnection() 
    with open('yamlfiles/'+'console.yaml') as f:
        o = yaml.safe_load(f)
        print "Configuring EIGRP on all routers"
        for router in o["routermapping"]:
            commands = l.render('eigrp_init.j2',router+'.yaml')
            threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][router],commands,router)))

    for t in threads:
         t.start()

    for t in threads:
         t.join()

  def remove_eigrp(self):
       threads = []
       l = LabConnection()
       print "Removing EIGRP from all routers"
       with open('yamlfiles/' + 'console.yaml') as f:
         o = yaml.safe_load(f)
         for router in o["routermapping"]:
            commands = ['no router eigrp 100'] 
            threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][router],commands)))


       for t in threads:
         t.start()


       for t in threads:
         t.join()
       
       print "Removed EIGRP from all routers"


