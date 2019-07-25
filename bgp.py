from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml
from LabConnection import *
import threading
from init import *

class BGP :


  def init_bgp(self):
    threads = []
    l = LabConnection() 
    with open('yamlfiles/'+'console.yaml') as f:
        o = yaml.safe_load(f)
        print "Configuring EIGRP on all routers"
        for router in o["routermapping"]:
            commands = l.render('bgp_init.j2',router+'.yaml')
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

  def bgp_topo(self):

       print "N WLLA OMNI \n"
       print "N - Is the next hop reachable \n"
       print "Weight >  Local Preference >  Locally injected > AS Path \n " 
       print "Origin >  MED > Neighbor Type >  IGP metric \n \n\n\n" 

       print "             Topology \n \n"
       print "         R6-------------ibgp-------------R4   "
       print "         |   AS 100      |                |   "
       print "         |               |                |   "
       print "         |              R1                |   "
       print "         |               |                |   "
       print "         |               |                |   " 
       print "         |               |                |   " 
       print "         |   R2---------R3---------------R5   "
       print "       ebgp             AS 200            |   "
       print "         |                                |   "
       print "         |                               R8   "
       print "         |                                |   "
       print "         |                              ebgp  "
       print "         |                                |   " 
       print "AS 300   R7------ebgp-----R9------------R10   "
       print "                                 AS 54"       


    #def basic_routing():
     
    #def auto_summary():

    #def multi_af():


    #def auth():

    #def key_chain():

    
    #def unicast_updates():


    
    

