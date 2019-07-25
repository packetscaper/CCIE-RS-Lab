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


More details follow the below workbooks <br>

https://ine.com/products/ccie-routing-switching-workbook





## Setup

1. Install GNS3 in a Windows machine - https://www.gns3.com/software/download
2. Install GNS3 VM in an ESXI - https://docs.gns3.com/1hEoK0rmtdBRnMaUaVoMHUbYwtDAltXYShiMJUp1GMxk/index.html
2. Download topology.gns3 file and open it in GNS3.
3. Issue git pull https://github.com/packetscaper/CCIE-RS-Lab.git in a linux machine
4. Initialize yamlfilefiles/console.yaml based on your environment.
5. Copy INE R&S v5 labs in the config folder.
5. Install Netmiko
      ```
      pip install netmiko
      
      ```
 
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


