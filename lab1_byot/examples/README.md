# Build your own Juniper virtual topology - KVM environment

## Authors

**gilbertorgit**

## Description
To create a baseline configuration, there are two essential elements to consider:
1. Devices with CORE and/or REFLECTOR roles (refer to the spreadsheet for details)

When a device is configured with 'CORE' and/or 'REFLECTOR' role assigned, the script is capable of configuring P2P physical addresses using IPv4 /31 and IPv6 /127 subnets and additional configuration options are available, such as - topology based on ISIS, OSPF with MPLS enabled, etc., 

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
  * Example 1
  * Example 3
  * Example 4
* When a topology has 'CORE' and at least 1 element with 'CORE, REFLECTOR', any option can be used. 
  * Using Options 5, 'CORE' devices will establish peering with 'CORE, REFLECTOR' devices.
    * Example 5
  * Using Options 8, you can configure only P2P and Loopback interfaces, which can be ideal for setting up the baseline in a Spine/Leaf Topology. 
    * Example 2

These use cases outline different scenarios and options based on the roles assigned in the topology. 
Consider these use cases to determine the appropriate configuration option based on the specific setup of your network.

## Topology examples

<p align="center">
  Example 1 - DC 5-Clos with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example1.png">
  
  Example 2 - DC with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example2.png">

  Example 3 - DC 3-Clos with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example3.png">

  Example 4 - DC 3-Clos with vjunos-evolved, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example4.png">

  Example 5 - DC 3-Clos with vjunos-evolved, VR vSRX3 (Simulate Customers) and Apstra
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example5.png">

  Example 6 - DC 3-Clos with vjunos-switch and vjunos-evolved, Core with vjunos-router, VR vSRX3 (Router Reflector and Customers), Apstra and CentOS Linux
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example6.png">
</p>