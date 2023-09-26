# How to build your own Juniper virtual topology - KVM environment

## Authors

**gilbertorgit**

1. Draw the Topology
   - You can use any tool, such as PowerPoint, Visio etc.,

<p align="center">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_1.png">
</p>

2. Fill the interfaces connection with “S-Xs” interfaces

<p align="center">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_2.png">
</p>

3. Replicate it to spreadsheet
   - as a good practice, create inside the example folders

<p align="center">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_3.png">
  <img src="https://github.com/gilbertorgit/vjunos_kvm/blob/main/lab1_byot/images/how_to_4.png">
</p>

4. Copy the example to the main spreadsheet
   - cp examples/example5.xlsx lab1_device_info.xlsx 

5. Run the script and have fun
   - python main.py
