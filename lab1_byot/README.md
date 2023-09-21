# Build your own Juniper virtual topology - KVM environment

## Authors

**gilbertorgit**

## Important Information
- The python script provided in this guide allows for the creation, deletion, start, and stop of all resources within the topology.
- It is crucial to maintain the names and file paths exactly as shown here to avoid potential issues.
- Ensure that you use the specified versions of the images, as using different versions may lead to complications.
- Default username and password information:
  - root/juniper123
  - lab/lab123
- You can modify these credentials by editing the python script.
- Lab Network IP and Interface information:
  - 192.168.122.0/24 -> default KVM bridge network (You can modify it by editing the lab1_device_info.xlsx)
    - mgmt_ip - The IP used for device configuration on the KVM, configured using virbr0 - 192.168.122.
  - virbr0 - default KVM bridge interface
- The script creates several virtual interfaces, which must also be configured accordingly in the .xlsx file. Examples of these virtual interfaces can be found in the provided topology.
  - S-X -> S-1/S-50: Virtual Interfaces for configuring core devices.
    - The script offers an option to automatically configure point-to-point (p2p) interfaces in the main routers. It will search for these interfaces to configure the p2p connections.
  - D-X -> D-1/D-50: Virtual Interfaces for configuring DataCenter devices and/or VR Devices (e.g., servers, routers with routing-instances configured to simulate CEs, etc.).
    - The script also provides an option to automatically configure p2p interfaces. 
    - You can configure the D-X interfaces to establish your DataCenter Fabric or adjacency with other devices, such as Virtual Linux, VR Devices to simulate customers, etc.
    - In this case, the script will not configure any p2p interfaces if D-X interfaces are detected.
  - dummy-X -> dummy-1/dummy-50: Interfaces for unused connections - No action needed, this is for informational purposes only.
  - fabric-X -> fabric-1/fabric-50: Used to connect vRE-vFPC on vMX Devices - No action needed, this is for informational purposes only.


## Prerequisites

Please check the main README

## Preparing the environment

Please check the main README

## Menu Options:

1. Start Topology: Launches the topology and starts the virtual network.
2. Stop Topology: Stops the running topology and shuts down the virtual network.
3. Create Topology: Sets up and creates the desired network topology. 
4. Delete Topology: Removes the existing network topology. 
5. Configure ISIS Topology: Configures the basic network topology using ISIS routing protocol. 
6. Configure OSPF Topology: Configures the basic network topology using OSPF routing protocol. 
7. Configure Interfaces only (ISO Family): Sets up P2P and Loopback interfaces with the iso family configuration. 
8. Configure Interfaces only: Configures basic P2P and Loopback interfaces in the network topology. 
9. Load Baseline Config: Overwrites the current configuration with a baseline configuration. 
10. Save Config: Retrieves and saves the device configurations.

These menu options provide convenient functionalities to manage and configure your network topology effectively.

## Command-line Usage:

* You can call the script directly from the command line with the following syntax:

```
python main.py <option>
```

1. Start Topology: python main.py 1 
2. Stop Topology: python main.py 2 
3. Create Topology: python main.py 3 
4. Delete Topology: python main.py 4 
5. Configure ISIS Topology: python main.py 5 
6. Configure OSPF Topology: python main.py 6 
7. Configure Interfaces only (ISO Family): python main.py 7 
8. Configure Interfaces only: python main.py 8 
9. Load Baseline Config: python main.py 9 
10. Save Config: python main.py 10


* Please, check the examples folder where you can find further info and topology examples. You can just copy/past and have a ready-to-go topology

```
cd /home/lab/virtual_lab_kvm/

source my-env/bin/activate

cd lab1_byot/
 
python main.py
---------------------------
(my-env) root@kvm-server:/home/lab/virtual_lab_kvm/lab1_byot# python main.py 
1 - Start Topology

2 - Stop Topology

3 - Create topology

4 - Delete topology

5 - Configure ISIS topology - Basic topology based on ISIS

6 - Configure OSPF topology - Basic topology based on OSPF

7 - Configure Interfaces only - Basic P2P and Loopback interfaces with iso family

8 - Configure Interfaces only - Basic P2P and Loopback interfaces

9 - Load Baseline Config - Overwrite current configuration with baseline config

10 - Save Config

Select one Option: 3 ->>> Will create from scratch
---------------------------
```

## Workaround

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
3. Issue the reboot command"
