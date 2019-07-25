import yaml
from LabConnection import *
import threading
import requests,json,time,yaml


class Gns3:

 def __init__(self):
   with open('yamlfiles/console.yaml') as f:
       o = yaml.safe_load(f)
       self.gns3_host = "http://"+o["gns3_host_ip"]+":3080/"
    

 def start(self,device):
    url = self.gns3_host+"v2/projects/"
    headers = {"Accept":"application/json","Content-Type":"application/json"}

    with open('topology.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
        url = url + project_id
    for node in json_output['topology']['nodes']:
            if node['name'] == device:
                node_id = node['node_id']
                print "starting ",device
    response = requests.request("POST",url+"/nodes/"+node_id+"/start")
 def stop(self,device):

    url = self.gns3_host+ "v2/projects/"
    headers = {"Accept":"application/json","Content-Type":"application/json"}

    with open('topology.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
        url = url + project_id
    for node in json_output['topology']['nodes']:
           if node['name'] == device:
                node_id = node['node_id']
                print "stopping ", device
    response = requests.request("POST",url+"/nodes/"+node_id+"/stop")


 def stop_all(self):
    threads =  []
    with open('topology.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]

    for node in json_output['topology']['nodes']:
          threads.append(threading.Thread(target=self.stop,args=(node['name'],)))

    for t in threads:
         t.start()

    
    for t in threads:
         t.join()


 def start_all(self):
    threads =  []
    with open('topology.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
    for node in json_output['topology']['nodes']:
          threads.append(threading.Thread(target=self.start,args=(node['name'],)))

    for t in threads:
         t.start()

    for t in threads:
         t.join()

 def reset_lab(self):
    print "reseting lab"

    self.stop_all()
    self.start_all()
                                                    
