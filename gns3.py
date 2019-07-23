import yaml
from LabConnection import *
import threading
import requests,json,time


class Gns3:


 def start(self,device):
    url = "http://192.168.56.1:3080/v2/projects/"
    headers = {"Accept":"application/json","Content-Type":"application/json"}

    with open('Route-Switch.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
        url = url + project_id
    for node in json_output['topology']['nodes']:
            if node['name'] == device:
                node_id = node['node_id']
    response = requests.request("POST",url+"/nodes/"+node_id+"/start")
 def stop(self,device):

    url = "http://192.168.56.1:3080/v2/projects/"
    headers = {"Accept":"application/json","Content-Type":"application/json"}

    with open('Route-Switch.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
        url = url + project_id
    for node in json_output['topology']['nodes']:
           if node['name'] == device:
                node_id = node['node_id']

    response = requests.request("POST",url+"/nodes/"+node_id+"/stop")


 def stop_all(self):
    threads =  []
    with open('Route-Switch.gns3') as f:
        json_output = json.loads(f.read())
        project_id = json_output["project_id"]
    for node in json_output['topology']['nodes']:
          threads.append(threading.Thread(target=self.stop,args=(node['name'],)))

    for t in threads:
         t.start()
 def start_all(self):
    threads =  []
    with open('Route-Switch.gns3') as f:
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
                                                    
