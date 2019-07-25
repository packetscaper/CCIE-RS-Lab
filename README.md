# CCIE-RS-Lab

## Introduction

A utility to help practice and study for CCIE-RS-Lab in a GNS3 environment.


## Topology

### GNS3 physical topology

![alt text](https://raw.githubusercontent.com/packetscaper/CCIE-RS-Lab/master/topologies/gns3_physical_topology.png)

### Logical Topology

![alt text](https://raw.githubusercontent.com/packetscaper/CCIE-RS-Lab/master/topologies/ip_addressing.png)



### OSPF Topology


![alt text](https://raw.githubusercontent.com/packetscaper/CCIE-RS-Lab/master/topologies/OSPF.png)



### BGP Topology


![alt text](https://raw.githubusercontent.com/packetscaper/CCIE-RS-Lab/master/topologies/BGP.png)


More details follow the INE workbooks from the below link <br>

https://ine.com/products/ccie-routing-switching-workbook





## Setup

1. Install GNS3 in a Windows machine - https://www.gns3.com/software/download
2. Install GNS3 VM in an ESXI - https://docs.gns3.com/1hEoK0rmtdBRnMaUaVoMHUbYwtDAltXYShiMJUp1GMxk/index.html
3. Install this utility in a linux or mac machine using git pull https://github.com/packetscaper/CCIE-RS-Lab.git 
4. Validate that there is connectivity between the linux or mac machine running this utility to the host running GNS3 as well as the GNS3 VM
4. Download the topology.gns3 file and open it in GNS3.
5. Initialize yamlfilefiles/console.yaml based on your environment <br>
   i.   gns3_vmware_ip is the ip over which the GNS3 VM can be accessed <br>
   ii.  gns3_host_ip is the ip over which gns3 utility runs. Generally a windows machine <br>
   iii. map the ports of the various routers as seen on your gns3 environment after opening the topology.gns3 <br>
6  Download topology.gns3 file and open it in GNS3.
7. Copy INE R&S v5 labs in the config folder.
8. Install Netmiko python library
      ```
      pip install netmiko
      
      ```
 
 For more details on setting up GNS3, the below links can be referred <br>
 
 https://davidbombal.com/gns3-download-install-getting-working/ <br>
 
 https://docs.gns3.com/1wdfvS-OlFfOf7HWZoSXMbG58C4pMSy7vKJFiKKVResc/index.html
 
 
## Usage

### Initialize the lab

Eg.

  ```
   #ipython
   : from init import *
   
   : start_all()
   
   : init_lab()
   
   : stop('R3')
   
   : stop('R3')
  
  ```

### Send and verify commands

Eg. 

  ```
   :send('all','show ip int br')
   
   :send(['R1','R2','R5'],'show cdp neighbor')
   
   :send(['R1','R5'],['router eigrp 1,'network 155.1.0.0 0.0.255.255'])
   
   :send('R1','show ip eigrp neighbor')
   
  ```

### Initialize routing labs

Eg. 
  ```
   :init_eigrp()
   
   :remove_eigrp()
   
   :init_ospf()
   
   :remove_ospf()
   
   :init_bgp()
   
   :reset_lab()
   
  ```

### Load INE labs

Eg.

  ```
   :lslab() # displays all the labs
   
   :lslab(ospf) # displays all the OSPF labs
   
   :load('bgp.full','all')  # loads the bgp.full lab. 
   
   
  ```


