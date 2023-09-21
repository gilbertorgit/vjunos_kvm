# Build your own Juniper virtual topology - KVM environment

## Authors

**gilbertorgit**

## Description
To create a baseline configuration, there are two essential elements to consider:
1. S-Xs Interfaces
2. Devices with CORE and/or REFLECTOR roles (refer to the spreadsheet for details)

When a device is configured with S-Xs interfaces, the script is capable of configuring P2P physical addresses using IPv4 /31 and IPv6 /127 subnets.
Moreover, when a device has the 'CORE' and/or 'REFLECTOR' role assigned, additional configuration options are available.

By combining these elements, you gain the ability to create a comprehensive baseline configuration. 
Refer to Options 5, 6, 7, and 8 for further details.

* Option 5: Configure the topology with ISIS, LDP, RSVP, MPLS, BGP, and BFD.
* Option 6: Configure the topology with OSPF, LDP, RSVP, MPLS, BGP, and BFD.
* Option 7: Configure the topology with P2P and Loopback interfaces using the iso family.
* Option 8: Configure the topology with P2P and Loopback interfaces.
These options provide different configurations for the network topology, including various routing protocols (ISIS or OSPF), protocol dependencies (LDP, RSVP, MPLS), routing (BGP), and fault detection (BFD). 
Select the appropriate option based on your requirements and network setup.

**Currently supported roles:**
* CORE: Applies baseline configuration to the device.
* CORE, REFLECTOR: Configures the device with baseline settings and creates the BGP Router Reflector role.
* VR: Future use - The script does not take any action for this role.
* DC: Future use - The script does not take any action for this role.
These roles define the specific configuration and actions performed by the script. 
The CORE role applies the baseline configuration, while the CORE, REFLECTOR role additionally configures the device as a BGP Router Reflector. 
The VR and DC roles are reserved for future use and are currently not utilized by the script.

**REFLECTOR only is not supported** 

Use cases:
* When a topology has no 'CORE' roles, no configuration will be applied. 
  * Example 1 (Data Center devices have DC ROLE, so no configuration will be applied)
  * Example 2
  * Example 4
* When a topology has 'CORE' roles only, any option can be used. 
  * Options 5 and 6 configure a full mesh IBGP configuration. 
    * Example 6
    * Example 7
* When a topology has 'CORE' and at least 1 element with 'CORE, REFLECTOR', any option can be used. 
  * Using Options 5 and 6, 'CORE' devices will establish peering with 'CORE, REFLECTOR' devices.
  * Using Options 7 and 8, you can configure only P2P and Loopback interfaces, which can be ideal for setting up the baseline in a Spine/Leaf Topology. 
    * Example 3
    * Example 9
* It is possible to have more than one 'CORE,REFLECTOR'. 
  * Example 1 - VR0, VR1 and VR2 have CORE,REFLECTOR 
  * Example 4 - SPINE1 and SPINE2 have CORE,REFLECTOR

These use cases outline different scenarios and options based on the roles assigned in the topology. 
Consider these use cases to determine the appropriate configuration option based on the specific setup of your network.

## Topology examples

<p align="center">
  Example 1 - DC 3-Clos with vjunos-switch, Core with vMX, VR vSRX3 (Router Reflector and Customers), Apstra and CentOS Linux
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example1.png">
  
  Example 2 - DC 5-Clos with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example2.png">
  
  Example 3 - DC with vjunos-switch, VR vSRX3 (Simulate Customers)
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example3.png">
  
  Example 4 - Core with vMX and VR vSRX3 (Simulate Customers)
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example4.png">
  
  Example 5 - DC 3-Clos with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example5.png">
  
  Example 6 - Small Core with vMX and VR vSRX3 (Simulate Customers)
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example6.png">
  
  Example 7 - Core with vMX and VR vSRX3 (Simulate Customers)
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example7.png">

  Example 8 - DC 3-Clos with vjunos-evolved, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example8.png">

  Example 9 - DC 3-Clos with vjunos-evolved, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/virtual_lab_kvm/blob/main/lab1_byot/images/example9.png">
</p>