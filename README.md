# CCIE-RS-Lab

## Introduction

A utility to help practice and study for CCIE-RS-Lab in a GNS3 environment


## Setup

1. Setup GNS3 in a Windows machine
2. Download topology.gns3 file and open it in GNS3.
3. Issue git pull https://github.com/packetscaper/CCIE-RS-Lab.git in a linux machine
4. Initialize yamlfilefiles/console.yaml based on your environment.
5. Copy INE R&S v5 labs in the config folder.
5. Install Netmiko
      ```
      pip install netmiko
      
      ```
 
## Use

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

## Load INE labs

Eg.

  ```
   :lslab() # displays all the labs
   :lslab(ospf) # displays all the OSPF labs
   
   :load('bgp.full','all')  # loads the bgp.full lab. 
   
   
  ```


