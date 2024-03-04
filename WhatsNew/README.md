# What is new - vJunos KVM

To consume new functionalities please, update the project as there have been changes in a few scripts as well as the spreadsheet. 

**February 2024**
- New Linux Support
  - From now on, you can configure CentOS or Ubuntu Linux. Only cloud images are supported at this stage, as the script utilizes cloud-init.
  - Cloud-init examples config are under vm_config
    - In this version, you need to create a folder per VM, matching the hostname, and two files: meta-data and user-data.
    - There is no additional file support for configuration; only these two will be considered to create the Linux VMs.
  - Refer to the examples folder -> example9 -> LINUX TAB to get config example. 
    - Where the spreadsheet column matches the directory created, example:
        - type = centos, version = 7 -> centos-7 (directory to be created)
  - Default size is 15G for each Linux VM created, in case you need to increase it, go to  lab1_byot -> basicInfra.py and change:
    - linux_vmx_size = '15G' - Variable
- You need to create a specific directory following the same pattern used to create vMX, vSRX, etc. Below is an example:
  - Centos Example:
    - mkdir centos-7
      - cp CentOS-7-x86_64-GenericCloud.qcow2 centos-7/
  - Ubuntu Example: (validated with Jammy and Focal)
    - mkdir ubuntu-20.04 
      - cp focal-server-cloudimg-amd64.img /opt/src_virtual_lab_images/ubuntu-20.04/
      - http://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
    - mkdir ubuntu-22.04
      - cp jammy-server-cloudimg-amd64.img /opt/src_virtual_lab_images/ubuntu-22.04/
      - http://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img

**December 2023**
- New roles support
  - 'CORE'
    - When configure 'CORE' + 'S-Xs' interfaces you can use options 7 and 8 for interface configuration
  - 'CORE,LER' -> **LER**=Label Edge Router
    - When configuring 'CORE,LER' + 'S-Xs' interfaces 
      - you can use options 5-8 for additional configuration 
      - it will create BGP Peering
        - full-mesh IBGP when no 'CORE,REFLECTOR' is configured
        - IBGP with Router Reflector when 'CORE,REFLECTOR' is configured
  - 'CORE,REFLECTOR'
    - you can use options 5-8 for additional configuration
    - This device will be a router reflector and have peering with 'CORE,LER' devices
  - DC - no additional config is provided
  - VR - no additional config is provided
*Check examples folder for further info* -> https://github.com/gilbertorgit/vjunos_kvm/tree/main/lab1_byot/examples

- Juniper vMX support

**November 2023**
- Juniper vjunos-router support

**October 2023**
- Juniper vjunos-evolved support

