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
    
    self.bgp_topo()

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

       print "\n \n N WLLA OMNI \n"
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
       print "  AS 100    ==>   R1 --ebgp--R3      R6----bgp--R7      R4---ebgp---R5"
       print "  AS 200    ==>   R2---ebgp---R10    R3---ebgp---R1     R3---ebgp----R7    R5---ebgp---R4    R8----ebgp---R10" 
       print "  AS 300    ==>   R7---ebgp---R6     R7--ebgp---R6      R7---ebgp----R9 "
       print "  AS 54     ==>   R9---ebgp---R7     R10---ebgp---R8    R10----ebgp---R2"

  

  def best_path_selection_weight(self):
      l = LabConnection()
      commands = []
      with open('yamlfiles/bgp_route_selection_excercise.yaml') as f:
           o = yaml.safe_load(f)
      print "==================================================================================================="
      print "==================================Weight_Example===================================================" 

      l.output('R7','show ip bgp 150.1.9.9')
      print "R7 prefers R9 (shortest AS) \n Increasing weight for routes learnt from R3 for AS 54 \n \n"
      print "Traffic from R7 towards AS 54 should exit via R3"
      commands = o["R7"]["weight_from_r3"]
      l.output('R7',commands) 
      time.sleep(2)
      l.output('R7','show ip bgp 150.1.9.9')
      print "Reverting configuration"
      commands = o["R7"]["no_weight_from_r3"]
      l.output('R7',commands)
      time.sleep(2)

      l.output('R7','show ip bgp 150.1.9.9')
      print "==================================================================================================="
      print "=======================================Weight_Example==============================================" 


  
  def best_path_selection_local_preference(self):
      l = LabConnection()
      commands = []
      with open('yamlfiles/bgp_route_selection_excercise.yaml') as f:
           o = yaml.safe_load(f)
      print "==================================================================================================="
      print "==================================Local_Preference_Example=========================================" 
      l.output(['R1','R6','R4'],'show ip bgp 150.1.9.9')
      print "R6 prefers R7 \n R1 prefers R3 \n R4 prefers R5', Neighbor Type ebgp over ibgp  \n"
      print "Traffic from AS 100 towards AS 54 should exit via R7 AS 300"
      commands = o["R6"]["local_preference_from_r7"]
      l.output('R6',commands) 
      l.output(['R1','R6','R4'],'clear ip bgp * soft')
      time.sleep(2)
      l.output(['R1','R6','R4'],'show ip bgp 150.1.9.9')
      print "Reverting configuration"
      commands = o["R6"]["no_local_preference_from_r7"]
      l.output('R6',commands)
      l.output(['R1','R6','R4'],'clear ip bgp * soft')
      time.sleep(2)
      l.output(['R1','R6','R4'],'show ip bgp 150.1.9.9')
      print "================================================================================================="
      print "===========================================Local_Preference_Example=============================="
     

    
  def best_path_selection_as_prepend(sself):
      l = LabConnection()
      commands = []
      with open('yamlfiles/bgp_route_selection_excercise.yaml') as f:
           o = yaml.safe_load(f)
      print "==================================================================================================="
      print "==================================AS_Prepend_Example=========================================" 
      l.output(['R1','R6','R4'],'show ip bgp 150.1.9.9')
      print "R6 prefers R7 \nR1 prefers R3 \nR4 prefers R5 \nNeighbor Type ebgp over ibgp  \n"
      print "Configure AS 200 such that traffic from AS 100 towards AS 54 should exit via R7 AS 300 "
      commands = o["R3"]["as_prepend_to_r1"]
      l.output('R3',commands)
      commands = o["R5"]["as_prepend_to_r4"]
      l.output('R5',commands)
      l.output(['R1','R6','R4'],'clear ip bgp * soft')
      time.sleep(2)
      l.output(['R1','R6','R4'],'show ip bgp 150.1.9.9')
      print "Reverting configuration"
      commands = o["R3"]["no_as_prepend_to_r1"]
      l.output('R3',commands)
      commands = o["R5"]["no_as_prepend_to_r4"]
      l.output('R5',commands)
      l.output(['R1','R6','R4'],'clear ip bgp * soft')
      time.sleep(2)
      l.output(['R1','R6','R4'],'show ip bgp 150.1.9.9')
      print "================================================================================================="
      print "===========================================AS_Prepend_Example=============================="
     

    #def basic_routing():
     
    #def auto_summary():

    #def multi_af():


    #def auth():

    #def key_chain():

    
    #def unicast_updates():


    
    

