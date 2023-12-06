# How to build your own Juniper virtual topology - KVM environment

## Authors

**gilbertorgit**

- Draw the topology. 
- Fill the interfaces with S-Xs and D-Xs interfaces. 
- Replicate it in a spreadsheet. 
  - If you have edited the DHCP range in the default virbr0, as recommended, remember to configure MGMT IPs starting from .101. 
  - When configuring VMX, it is good practice to include vcp and vfp0 in the hostname, so you can differentiate the images, as shown in the example below:
    - **lab1_vcp_r1**
    - **lab1_vfp0_r1**
- Copy the spreadsheet to the examples folder, so you can have the original topology saved for later use. 
- Copy the example to the main spreadsheet, located in the main project folder: vjunos_kvm/lab1_byot/lab1_device_info.xlsx. 
- Run the script and have fun!

1. Draw the Topology
   - You can use any tool, such as PowerPoint, Visio etc.,

<p align="center">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_1.png">
</p>

2. Fill the interfaces connection with “S-Xs” interfaces

<p align="center">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_2.png">
</p>

3. Replicate it to spreadsheet - Please, use the Examples as template! Don't change/add anything apart from new lines based on specific TAB examples
   - as a good practice, create inside the example folders

<p align="center">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_3.png">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_4.png">
</p>

4. Copy the example to the main spreadsheet
   - cp examples/new_topology_10.xlsx **lab1_device_info.xlsx** (this spreadsheet is located at the main lab1_byot folder -> /home/lab/vjunos_kvm/lab1_byot/)

5. Run the script and have fun
   - python main.py
