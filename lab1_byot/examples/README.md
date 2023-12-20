# Build your own Juniper virtual topology - KVM environment

## Authors

**gilbertorgit**

## Description
To create a baseline configuration, there are two essential elements to consider:
1. Configure **CORE**, **CORE,LER**, **CORE,REFLECTOR**, **VR** or **DC** roles - Define a roles IS A MUST
2. Configure **S-Xs** or **D-Xs** virtual interfaces - Define a virtual interface IS NOT A MUST! You just need to fill the interfaces you need with S-Xs(S-1, S-2, etc.,) or D-Xs(D-1, D-2, etc.,) interfaces

When a device is configured with **S-Xs** interface and **CORE** or **CORE,REFLECTOR** role assigned , the script is capable of configuring P2P physical addresses using IPv4 /31 and IPv6 /127 subnets and additional configuration options are available, such as - topology based on ISIS, OSPF with MPLS enabled, etc., 

By combining these elements, you gain the ability to create a comprehensive baseline configuration. 
Refer to Options 5, 6, 7, and 8 for further details.

* Option 5: Configure the topology with ISIS, LDP, RSVP, MPLS, BGP, and BFD.
* Option 6: Configure the topology with OSPF, LDP, RSVP, MPLS, BGP, and BFD.
* Option 7: Configure the topology with P2P and Loopback interfaces using the iso family.
* Option 8: Configure the topology with P2P and Loopback interfaces.
These options provide different configurations for the network topology, including various routing protocols (ISIS or OSPF), protocol dependencies (LDP, RSVP, MPLS), routing (BGP), and fault detection (BFD). 
Select the appropriate option based on your requirements and network setup.

**Currently supported roles:**
* CORE: Enable script to apply additional configuration to the device but does not create any BGP configuration.
  * When configuring CORE + S-Xs interfaces you can use options 5-8, however with core only, the script will not create any BGP configuration.
  * It can be useful to configure a router as **LSR** (Label Switch Router)
* CORE,LER: Configures the device with additional settings and creates BGP peering.
  * When configuring CORE + S-Xs interfaces you can use options 5-8.
  * The script will create:
    * BGP peer with Router Reflector(if you have configured a **core,reflector** role in any of the virtual devices)
    * or a full-mesh BGP in case you have no **core,reflector** role device)
  * It can be useful to configure a router as **LER** (Label Switch Router)
* CORE,REFLECTOR: Configures the device with additional settings and creates BGP peerings with **CORE,LER** devices.
  * When configuring CORE + S-Xs interfaces you can use options 5-8.
* VR: The script does not take any action for this role.
* DC: The script does not take any action for this role.

**These roles define the specific configuration and actions performed by the script.**
* The CORE role enables the script to apply the Additional configuration but BGP
* The CORE,LER role enables the script to apply the Additional configuration
* The CORE,REFLECTOR role additionally configures the device as a BGP Router Reflector. 
* The VR and DC roles are reserved for future use and are currently not utilized by the script.

**What is covered in the Additional Configuration** 
* P2P and Loopback interfaces - IPv4 and IPv6
* ISO address ( for ISIS topology )
* OSPF
* ISIS
* IBGP - IPv4 Peering Only
* Load-Balance Policy
* AS Number
* MPLS(LDP,RSVP)
* BGP Config
* Next-Hop Self - BGP Policy

**REFLECTOR only is not supported** 

Use cases:
* When a topology has no 'CORE'/'CORE,LER'/'CORE,REFLECTOR' roles and 'S-Xs' interfaces, no configuration will be applied. 
  * Example 1
  * Example 3
  * Example 4
* When a topology has 'CORE' roles and 'S-Xs' interfaces you can use options 7 and 8 for interface configuration only. 
  * Example 2
  * Example 7
* When a topology has 'CORE,LER' and at least 1 element with 'CORE,REFLECTOR', any option can be used. 
  * Using Options 5 or 6, 'CORE,LER' devices will establish peering with 'CORE,REFLECTOR' devices.
  * Using Options 7 or 8, for interface configuration only.
    * Example 5
    * Example 6
    * Example 8

These use cases outline different scenarios and options based on the roles assigned in the topology. 
Consider these use cases to determine the appropriate configuration option based on the specific setup of your network.

## Topology examples

Please check **how_to** folder for further details on how to build your topology from scratch.

<p align="center">
  Example 1 - DC 5-Clos with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  cp examples/example1.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example1.png">
  
  Example 2 - DC 5-Clos with with vjunos-switch, VR vSRX3 (Simulate Customers)
  cp examples/example2.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example2.png">

  Example 3 - DC 3-Clos with vjunos-switch, VR vSRX3 (Simulate Customers) and Apstra
  cp examples/example3.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example3.png">

  Example 4 - DC 3-Clos with vjunos-evolved, VR vSRX3 (Simulate Customers)
  cp examples/example4.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example4.png">

  Example 5 - DC 3-Clos with vjunos-evolved, VR vSRX3 (Simulate Customers)
  cp examples/example5.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example5.png">

  Example 6 - DC 3-Clos with vjunos-switch and vjunos-evolved, Core with vjunos-router, VR vSRX3 (Router Reflector and Customers), Apstra and CentOS Linux
  cp examples/example6.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example6.png">

  Example 7 - Simple Core with 4x vMX, VR(To simulate customers) 1x vSRX3 
  cp examples/example6.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example7.png">

  Example 8 - Core topology with 6x vMX and VR(To simulate customers) 1x vSRX3
  cp examples/example6.xlsx lab1_device_info.xlsx 
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/example8.png">
</p>