# Virtual Lab KVM(virt-install) Topologies  

* Supported Images:
  * vjunos-switch
  * vJunosEvolved
  * vSRX3
  * Apstra
  * CentOS

## Authors

**gilbertorgit**

### Current Virtual Lab Projects

* lab1_byot -> Build your own Topology
  * https://github.com/gilbertorgit/vjunos_kvm/tree/main/lab1_byot

## Very Important Info! 
* This project assumes that you have recompiled your kernel and removed the BR_GROUPFWD_RESTRICTED options. 
  * If this is not the case, you will need to update the main.py script located in the specific project directory
    * **From**
      * bridge_echo = 65535
    * **To**
      * bridge_echo = 16384

* To compile the kernel, you can refer to the following resources or documentation for detailed instructions:
 * Ubuntu 20.04 - https://github.com/gilbertorgit/kernel-20-04

## Considerations
This repository offers configuration examples intended for lab purposes only.

* Please note that this lab guide does not aim to cover best practices or production configurations.
* All the configurations provided in this guide are meant to serve as simple examples.

Following these instructions will enable you to obtain a copy of the project, allowing you to run it on your local machine for development and testing purposes

## Prerequisites
This test lab has been built and tested using:

```
1. Ubuntu 20.04 LTS
2. Server with:
  2.1. 128GB RAM
  2.2. I9 with 14 Cores and Intel(R) Xeon(R) Gold 5218 CPU @ 2.30GHz
  2.3. 500GB - SSD
3. vjunos-switch-23.1R1.7
4. vmx-22.4R1.10
5. apstra-4.1.2-269
6. CentOS-7-x86_64-GenericCloud.qcow2
```

***Please note that while we are downloading and copying packages and configurations within the /home/lab user directory, it's important to mention that I am using root user access for each step described here.***

## Pre-deployment Server Configs and Basic Packages
**Installation and Configuration of Packages**

```
sudo su -

cd /home/lab

apt -y install software-properties-common

add-apt-repository --yes ppa:deadsnakes/ppa

add-apt-repository --yes --update ppa:ansible/ansible

apt -y update

apt -y install ansible git

git clone https://github.com/gilbertorgit/vjunos_kvm.git

ansible-playbook vjunos_kvm/base-pkg-kvm/playbook.yml
```

**check kvm**

```
kvm-ok
```

```
cd vjunos_kvm/

python3.10 -m venv my-env

source my-env/bin/activate

pip install -r requirements.txt

deactivate
```

***If you are performing a new KVM server installation, please follow the steps below to change the virbr0 configuration and reload the server:***

**To change the default DHCP range of the virbr0 interface from .254 to .100, please follow the steps below:**
```
virsh net-edit default
------------------------------------------------------
from:
<range start='192.168.122.2' end='192.168.122.254'/>
to
<range start='192.168.122.2' end='192.168.122.100'/>
------------------------------------------------------
```

**To ensure that all changes are applied and functioning correctly, please reload your server.**

```
shutdown -r now
```

## Preparing the environment

### Supported Images

* vSRX: https://support.juniper.net/support/downloads/?p=vsrx3
* vEX -> vJunos-Switch: https://support.juniper.net/support/downloads/?p=vjunos
* Apstra - > AOS: https://support.juniper.net/support/downloads/?p=apstra
* Linux -> Centos-Generic-Cloud: https://cloud.centos.org/centos/7/images/ - CentOS-7-x86_64-GenericCloud.qcow2
* vJunosEvolved -> https://support.juniper.net/support/downloads/?p=vjunos-evolved

**Please copy all the images to the /opt/src_virtual_lab_images directory. An example is provided below:**

```
sudo su -

mkdir /opt/src_virtual_lab_images/
```

#### About Version

This automation script provides support for multiple virtual image flavors and versions

* To configure different versions, please follow these steps:
  * Create a directory for the specific version and copy the corresponding images into it. 
  * Add a 'version' column in the labX_device_info.xlsx file."

Here as you can see I'm creating a vMX and vSRX specific folder inside the image folders:

For vSRX:
* Create the folder using the following command:
  * mkdir /opt/src_virtual_lab_images/vsrx-<version>
    * 'vsrx-' is a constant name.
    * <version> is the specific version of vSRX.

For example:
* mkdir /opt/src_virtual_lab_images/vsrx-23.1R1.8
* mkdir /opt/src_virtual_lab_images/vsrx-21.2R1.9

**Below is a complete example:** 
```
mkdir /opt/src_virtual_lab_images/apstra-4.1.2-269
mkdir /opt/src_virtual_lab_images/linux
mkdir /opt/src_virtual_lab_images/vjunos-switch-23.1R1.8
mkdir /opt/src_virtual_lab_images/vsrx3-23.1R1.8
mkdir /opt/src_virtual_lab_images/vjunos-evolved-23.1R1.8

mv CentOS-7-x86_64-GenericCloud.qcow2 /opt/src_virtual_lab_images/linux
mv junos-vsrx3-x86-64-23.1R1.8.qcow2 /opt/src_virtual_lab_images/vsrx3-23.1R1.8
mv vjunos-switch-23.1R1.8.qcow2 /opt/src_virtual_lab_images/vjunos-switch-23.1R1.8
mv vJunosEvolved-23.1R1.8.qcow2  /opt/src_virtual_lab_images/vjunos-evolved-23.1R1.8

gunzip aos_server_4.1.2-269.qcow2.gz
mv aos_server_4.1.2-269.qcow2 /opt/src_virtual_lab_images/apstra-4.1.2-269
```

**Below is an example of the directory tree structure with a few directories:**

```
root@lab:~# ls -lR /opt/src_virtual_lab_images/
/opt/src_virtual_lab_images/:
total 24
drwxr-xr-x 2 root root 4096 Jun 15 19:20 apstra-4.1.2-269
drwxr-xr-x 2 root root 4096 Jun 15 19:18 linux
drwxr-xr-x 2 root root 4096 Jun 15 19:22 vjunos-evolved-23.1R1.8
drwxr-xr-x 2 root root 4096 Jun 15 19:19 vjunos-switch-23.1R1.8
drwxr-xr-x 2 root root 4096 Jun 15 19:22 vsrx3-23.1R1.8

/opt/src_virtual_lab_images/apstra-4.1.2-269:
total 2762612
-rw-r--r-- 1 root root 2828908544 Jan 12 00:01 aos_server_4.1.2-269.qcow2

/opt/src_virtual_lab_images/linux:
total 881732
-rw-r--r-- 1 root root 902889472 Nov 12  2022 CentOS-7-x86_64-GenericCloud.qcow2

/opt/src_virtual_lab_images/vjunos-evolved-23.1R1.8:
total 1865604
-rw-r--r-- 1 root root 1910374400 May  9 19:00 vJunosEvolved-23.1R1.8.qcow2

/opt/src_virtual_lab_images/vjunos-switch-23.1R1.8:
total 3867844
-rw-r--r-- 1 root root 3960668160 Apr 18 07:00 vjunos-switch-23.1R1.8.qcow2

/opt/src_virtual_lab_images/vsrx3-23.1R1.8:
total 828420
-rw-r--r-- 1 root root 848297984 Mar 24 03:46 junos-vsrx3-x86-64-23.1R1.8.qcow2
```

## For detailed instructions, please refer to the specific lab README.

* lab1_byot -> https://github.com/gilbertorgit/vjunos_kvm/tree/main/lab1_byot

