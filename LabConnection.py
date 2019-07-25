from netmiko import ConnectHandler
from jinja2 import Environment,FileSystemLoader
import yaml
import threading


class LabConnection:


  def push(self,host,port,commands,device):

   cisco = {
    'device_type' : 'cisco_ios_telnet',
    'host' : host,
    'port' : port,
    'username':'username',
    'password': 'password',
    'global_delay_factor': 0.05,
    }
   
   netconnect = ConnectHandler(**cisco)
   if type(commands) == list:
     output = netconnect.send_config_set(commands)
     print "Pushing commands to ", device, "\n"
     print "-------------"+device+"----------------"+device+"----------------"+"--------------"+device+"--------"
     print output 
     print "-------------"+device+"----------------"+device+"----------------"+"--------------"+device+"--------"

   if type(commands) == str:
    host = netconnect.find_prompt()
    output =   host +  commands + '\n' +  netconnect.send_command(commands) + '\n' + '\n' + '\n'
    border1= '------------'+host+'---------'+host+'-----------------' + host+ '---------------'+host+'---------------------------' + '\n' + '\n' + '\n'
    border2= '------------'+host+'---------'+host+'-----------------' + host+ '---------------'+host+'---------------------------' + '\n' + '\n' + '\n' 
    print '\n' + '\n' + '\n' + border1 + output + border2
      
  def output(self,routers,commands):
     threads = []
     if routers == 'all':
        routers = ['R1','R2','R3','R4','R5','R6','R7','R8','R9','R10']
     if type(routers) == str:
        temp = routers
        routers = [temp]
     with open('yamlfiles/'+'console.yaml') as f:
        o = yaml.safe_load(f)
        for router in routers :
             threads.append(threading.Thread(target=self.push,args = (o["gns3_vmware_ip"],o["routermapping"][router],commands,router,)))
        for t in threads:
                t.start()

        for t in threads:
                t.join()

              
 
  def render(self,jinja_file,yaml_file):

    ENV = Environment( loader = FileSystemLoader('.'))
    template = ENV.get_template('jinjatemplates/'+jinja_file)
    with open('yamlfiles/'+yaml_file) as f:
        configuration = yaml.safe_load(f)
        output = template.render(configuration)
    return str(output).splitlines()



