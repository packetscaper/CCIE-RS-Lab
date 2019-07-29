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
        print "Configuring BGP on all routers"
        for router in o["routermapping"]:
            commands = l.render('bgp_init.j2',router+'.yaml')
            threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][router],commands,router)))

    for t in threads:
         t.start()

    for t in threads:
         t.join()

  def remove_bgp(self):
       threads = []
       l = LabConnection()
       print "Removing bgp from all routers"
       with open('yamlfiles/' + 'console.yaml') as f:
         o = yaml.safe_load(f)
         for router in o["routermapping"]:
            commands = ['no router bgp'] 
            threads.append(threading.Thread(target=l.push,args=(o["gns3_vmware_ip"],o["routermapping"][router],commands)))


       for t in threads:
         t.start()


       for t in threads:
         t.join()
       
       print "Removed bgp from all routers"

  def bgp_topo(self):

       print "N WLLA OMNI \n"
       print "N - Is the next hop reachable \n"
       print "Weight >  Local Preference >  Locally injected > AS Path \n " 
       print "Origin >  MED > Neighbor Type >  IGP metric \n \n\n\n" 

       print "             Topology \n \n"
       print "         R6(100)------------ibgp--------------------R4(100)   "
       print "         |                   |                       |   "
       print "         |                   |                       |   "
       print "         |                  R1(RR,100)               |   "
       print "         |                   |                       |   "
       print "         |                   |                       |   " 
       print "         |                   |                       |   " 
       print "         |   R2(200)---------R3(RR,200)-------------R5(RR,200)   "
       print "       ebgp                                          |   "
       print "         |                                           |   "
       print "         |                                          R8(200)   "
       print "         |                                           |   "
       print "         |                                         ebgp  "
       print "         |                                           |   " 
       print "        R7(300)------ebgp-----R9(54)----ibgp--------R10(54)   "
       print "  \n \n                 "
       print "  AS 100    ==>   R1 --ebgp--R3      R6 ---bgp--R7      R4---ebgp---R5"
       print "  AS 200    ==>   R2---ebgp---R10    R3---ebgp --R1     R3---ebgp----R7    R5---ebgp---R4    R8----ebgp---R10" 
       print "  AS 300    ==>   R7---ebgp---R6     R7--ebgp---R6      R7---ebgp----R9 "
       print "  AS 54     ==>   R9---ebgp---R7     R10---ebgp---R8    R10----ebgp---R2"


    #def basic_routing():
     
    #def auto_summary():

    #def multi_af():


    #def auth():

    #def key_chain():

    
    #def unicast_updates():


    
    

