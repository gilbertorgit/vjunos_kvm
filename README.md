# vJunos KVM

vjunos_kvm -> Is a collection of Python scripts that facilitates the creation of virtual topology using Juniper virtual devices based on KVM (virt-install) environment. 
We are not reinventing the wheel it is just a personal project to help deploying VMs on vanilla KVM environment.

* Supported Images:
  * vjunos-switch
  * vjunos-router
  * vJunos-Evolved from version **23.2R1-S1.8** 
  * vSRX3
  * vMX
  * Apstra
  * CentOS 7 - Cloud Image
    * https://cloud.centos.org/centos/7/images/
  * Ubuntu - Cloud Image
    * http://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
    * http://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img

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

* Although the purpose of this project is not to teach how to compile the kernel, as there are many references available on this topic, you can refer to the following documentation for instructions:"
 * Ubuntu 20.04 - https://github.com/gilbertorgit/kernel-20-04

## Considerations
This repository offers configuration examples intended for lab purposes only.

* Please note that this lab guide does not aim to cover best practices or production configurations.
* All the configurations provided in this guide are meant to serve as simple examples.

Following these instructions will enable you to obtain a copy of the project, allowing you to run it on your local machine for development and testing purposes

## Prerequisites
This test lab has been built and tested using:

```
1. Ubuntu 20.04 LTS or 22.04.3
2. Server with:
  2.1. 128GB RAM
  2.2. I9 with 14 Cores and Intel(R) Xeon(R) Gold 5218 CPU @ 2.30GHz
  2.3. 500GB - SSD
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
* vJunos-Switch: https://support.juniper.net/support/downloads/?p=vjunos
* vJunos-Router: TBC
* vJunosEvolved -> https://support.juniper.net/support/downloads/?p=vjunos-evolved
* vMX: https://support.juniper.net/support/downloads/?p=vmx
* Apstra - > AOS: https://support.juniper.net/support/downloads/?p=apstra
* Linux -> Centos-Generic-Cloud: https://cloud.centos.org/centos/7/images/ - CentOS-7-x86_64-GenericCloud.qcow2

**Please copy all the images to the /opt/src_virtual_lab_images directory. An example is provided below:**

```
sudo su -

mkdir /opt/src_virtual_lab_images/
```

#### About Version

This automation script provides support for multiple virtual image flavors and versions

* To configure different versions, please follow these steps:
  * Create a directory for the specific version and copy the corresponding images into it. 
  * Add a 'version' column in the labX_device_info.xlsx file.

Here as you can see I'm creating a vMX and vSRX specific folder inside the image folders:

For vSRX:
* Create the folder using the following command:
  * mkdir /opt/src_virtual_lab_images/vsrx-<version>
    * 'vsrx-' is a constant name.
    * '<version>' is the specific version of vSRX.

For example:
* mkdir /opt/src_virtual_lab_images/vsrx-23.1R1.8
* mkdir /opt/src_virtual_lab_images/vsrx-21.2R1.9

**Below is a complete example:** 
```

## Create directories
mkdir /opt/src_virtual_lab_images/apstra-4.1.2-269

mkdir /opt/src_virtual_lab_images/centos-7

mkdir /opt/src_virtual_lab_images/ubuntu-20.04

mkdir /opt/src_virtual_lab_images/ubuntu-22.04

mkdir /opt/src_virtual_lab_images/vjunos-switch-23.2R1.14

mkdir /opt/src_virtual_lab_images/vjunos-router-23.2R1.14

mkdir /opt/src_virtual_lab_images/vsrx3-23.1R1.8

mkdir /opt/src_virtual_lab_images/vjunos-evolved-23.2R1-S1.8

mkdir /opt/src_virtual_lab_images/vmx-22.4R2.8


## Move images
mv CentOS-7-x86_64-GenericCloud.qcow2 /opt/src_virtual_lab_images/linux

mv junos-vsrx3-x86-64-23.1R1.8.qcow2 /opt/src_virtual_lab_images/vsrx3-23.1R1.8

mv vJunos-switch-23.2R1.14.qcow2 /opt/src_virtual_lab_images/vjunos-switch-23.2R1.14

mv vJunos-router-23.2R1.14.qcow2 /opt/src_virtual_lab_images/vjunos-router-23.2R1.14

mv vJunosEvolved-23.2R1.15.qcow2  /opt/src_virtual_lab_images/vjunos-evolved-23.2R1-S1.8


gunzip aos_server_4.1.2-269.qcow2.gz
mv aos_server_4.1.2-269.qcow2 /opt/src_virtual_lab_images/apstra-4.1.2-269


tar -xzvf vmx-bundle-22.4R2.8.tgz
mv vmx/images/junos-vmx-x86-64-22.4R2.8.qcow2 /opt/src_virtual_lab_images/vmx-22.4R2.8/
mv vmx/images/vmxhdd.img /opt/src_virtual_lab_images/vmx-22.4R2.8/
mv vmx/images/metadata-usb-re.img /opt/src_virtual_lab_images/vmx-22.4R2.8/
mv vmx/images/vFPC-20221102.img /opt/src_virtual_lab_images/vmx-22.4R2.8/

```

**Below is an example of the directory tree structure with a few directories:**

```
root@kvm-server:/home/lab/vjunos_kvm# ls -lR /opt/src_virtual_lab_images/
/opt/src_virtual_lab_images/:
total 1110328
drwxr-xr-x 2 root root       4096 Jun 19 10:51 apstra-4.1.2-269
drwxr-xr-x 2 root root      4096 Feb 14 13:59 centos-7
drwxr-xr-x 2 root root      4096 Feb 14 16:42 ubuntu-20.04
drwxr-xr-x 2 root root      4096 Feb 14 16:44 ubuntu-22.04
drwxr-xr-x 2 root root       4096 Sep 21 13:54 vjunos-evolved-23.2R1-S1.8
drwxr-xr-x 2 root root       4096 Sep 21 13:57 vjunos-switch-23.2R1.14
drwxr-xr-x 2 root root 4096 Jun 15 19:21 vmx-22.4R2.8
drwxr-xr-x 2 root root       4096 Jun 19 10:49 vsrx3-23.1R1.8

/opt/src_virtual_lab_images/apstra-4.1.2-269:
total 2762612
-rw-r--r-- 1 root root 2828908544 Jan 12  2023 aos_server_4.1.2-269.qcow2

/opt/src_virtual_lab_images/centos-7:
total 881732
-rw-r--r-- 1 root root 902889472 Feb 14 13:59 CentOS-7-x86_64-GenericCloud.qcow2

/opt/src_virtual_lab_images/ubuntu-20.04:
total 628100
-rw-r--r-- 1 libvirt-qemu kvm 643170304 Feb  7 22:26 focal-server-cloudimg-amd64.img

/opt/src_virtual_lab_images/ubuntu-22.04:
total 661252
-rw-r--r-- 1 libvirt-qemu kvm 677117952 Feb  7 02:58 jammy-server-cloudimg-amd64.img

/opt/src_virtual_lab_images/vjunos-evolved-23.1R1.8:
total 1865604
-rw-r--r-- 1 root root 1910374400 May  9 19:00 vJunosEvolved-23.2R1-S1.8.qcow2

/opt/src_virtual_lab_images/vjunos-evolved-23.2R1.15:
total 1701124
-rw-r--r-- 1 root root 1741946880 Aug  3 06:32 vJunosEvolved-23.2R1.15.qcow2

/opt/src_virtual_lab_images/vmx-22.4R2.8:
total 9855308
-rw-r--r-- 1 930 930 1191313408 Mar 19 06:35 junos-vmx-x86-64-22.4R2.8.qcow2
-rw-r--r-- 1 930 930   10485760 Feb  3 10:03 metadata-usb-re.img
-rw-r--r-- 1 930 930 8889827328 Feb  3 10:03 vFPC-20221102.img
-rw-r--r-- 1 930 930     196736 Feb  3 10:03 vmxhdd.img

/opt/src_virtual_lab_images/vsrx3-23.1R1.8:
total 828420
-rw-r--r-- 1 root root 848297984 Mar 24 03:46 junos-vsrx3-x86-64-23.1R1.8.qcow2
```

## For detailed instructions, please refer to the specific lab README.

* lab1_byot -> https://github.com/gilbertorgit/vjunos_kvm/tree/main/lab1_byot


## Virtual Devices - Workaround

As mentioned, this project is for lab purposes. Due to the nature of the VMX image, which is resource-intensive, deploying load of VMX images on the same server can lead to issues. 
These may include problems with the VMX image itself, syncing issues between VCP and VFP, or challenges with basic configurations that scripts typically handle via the console.
Therefore, if you encounter issues with VMX, you may need to configure it manually.

### 1 - VMX Boot issues

Due to unexpected reasons, often related to disk performance, the VMX may not boot properly at times, and you might encounter connectivity errors. These typically appear when the script is checking the connectivity and/or generating the baseline configuration to be saved into the virtual devices.

You can verify this by attempting to log in via console as the "lab" user. If there's an issue, you might encounter an error like the one shown below: 
```
md9.uzip: UZIP(zlib) inflate() failed
g_vfs_done():md9.uzip[READ(offset=75661312, length=2048)]error = 86
vm_fault: pager read error, pid 23069 (cli)
pid 23069 (cli), uid (0):  Path `/var/tmp/cli.core.4.gz' failed on initial open test, error = 14
```

If this is the case, there is no need to recreate the entire topology. However, you should reboot the affected devices one by one to resolve the issue. It is recommended to perform this process individually and then verify connectivity after each reboot.

To do so, you must connect as a root user using console and reboot the VCP virtual image only. Here are the steps:

1. Use the command virsh console <domain> (for example, lab1_vcp_r6)
2. Enter the username and password (root/juniper123)
3. Issue the reboot command or virsh destroy <domain> + virsh start <domain>

Make sure you run option 11 to generate the baseline config, so you can use option 9 in case you want to load the basic configuration (MGMT_IP + Hostname)


### 2 - VMX Problem with Basic Configuration provided by the script

The script may fail to configure the basic settings, and you might receive an 'unreachable' status at the end of the configuration script.
In that case, you will need to apply the basic configuration manually.

1. Use the command virsh console <domain> (for example, lab1_vcp_r6)
2. Enter the username "root" and enter
3. Enter: "cli" and "edit"
4. Start configuring the VMX based on the information you have provided in your spreadsheet. 

**Below is the basic configuration you need to apply:**
```
set system host-name <HOSTNAME>
set system root-authentication encrypted-password "$1$aic0re1C$iga3zkJvFaG7rP7tDP/P91"
set system commit synchronize
set system login user lab uid 2000
set system login user lab class super-user
set system login user lab authentication encrypted-password "$1$aic0re1C$i719d/4ZQchOhadfrUQxR."
set system services ssh root-login allow
set system services netconf ssh
set system syslog file interactive-commands interactive-commands any
set system syslog file messages any notice
set system syslog file messages authorization info
set interfaces fxp0 unit 0 family inet address <MGMT_IP>
set protocols lldp port-id-subtype interface-name
set protocols lldp interface all
```

Make sure you run option 11 to generate the baseline config, so you can use option 9 in case you want to load the basic configuration (MGMT_IP + Hostname)


### 3 - VMX VCP - VFP Sync

Sometimes, you may face interface issues, where there is no interface up (ge-0/0/0, ge-0/0/1, etc.,). It may be related with VCP and VFP sync.
You can find information about it in Juniper VMX official documentation. 

In that case, please check the below. 

1. Use the command virsh console <domain> (for example, lab1_vcp_r6)
2. Enter the username "root" or "lab"
3. Verify "show chassis FPC" and "show interfaces terse" to verify if the interfaces are up
4. If you have an output different from the below, you may need to reboot the VFP and VCP images
```
lab@lab3_pod1_leaf_1> show chassis fpc 
                     Temp  CPU Utilization (%)   CPU Utilization (%)  Memory    Utilization (%)
Slot State            (C)  Total  Interrupt      1min   5min   15min  DRAM (MB) Heap     Buffer
  0  Online           Testing   3         0        3      3      3    1023       19          0
```
* It's worth mentioning that VCP and VFP may take some time to sync. However, this is usually completed by the time the script finishes
```
virsh vcp_image_name destroy
virsh vfp_image_name destroy
virsh vcp_image_name start
virsh vfp_image_name start
```

Make sure you run option 11 to generate the baseline config, so you can use option 9 in case you want to load the basic configuration (MGMT_IP + Hostname)

### 4 - Test script -> unreachable status 

In case you are deploying a large number of VMs, it may take more time than usual to finish the process for all the VMs and get them to a fully running stage. In these cases, you may observe that many or most of the VMs are listed as 'unreachable.'

'Unreachable' means that the test script attempted to ping the VM but was unable to reach the destination due to an unexpected reason. 
This could be due to any of the issues mentioned above, a problem during the VM setup process, or because the VMs were not yet ready.

It's advisable to connect through the console to check if the VM is functioning correctly, whether the configuration is in place, and if you can reach the gateway, etc.

You can use the same process described above to connect to the VM's console and check its status.

```
-------------------------------------------------- Test MGMT Connectivity
lab1_vcp_r1 - MGMT Network: 192.168.122.51 is unreachable
lab1_vcp_r2 - MGMT Network: 192.168.122.52 is unreachable
lab1_vcp_r3 - MGMT Network: 192.168.122.53 is unreachable
lab1_vcp_r4 - MGMT Network: 192.168.122.54 is unreachable
lab1_vcp_r5 - MGMT Network: 192.168.122.55 is unreachable
lab3_pod1_leaf_1 - MGMT Network: 192.168.122.61 is unreachable
lab3_pod1_leaf_2 - MGMT Network: 192.168.122.62 is unreachable
```