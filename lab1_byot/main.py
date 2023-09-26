"""
---------------------------------
 Author: gilbertorgit
 Date: 02/2023
---------------------------------
"""

import sys
sys.path.append('../')
from time import sleep, time
from basicInfra import BasicInfra
from basicJuniper import BasicJuniper
from generateData import GenerateData
from devicesConsoleConfig import DevicesConfig
from configureJuniperDevice import ConfigureJuniperDevice


# Constants
BRIDGE_ECHO = 65535
INTERFACE_START = 1
INTERFACE_STOP = 101
DEVICE_TAB_LIST = ('SRX', 'VEX', 'VEVO', 'APSTRA', 'LINUX')


class MainScript:
    """
    This class is used to manage and configure a virtual network topology.

    It contains methods to create, delete, start, and stop the topology, as well as
    methods to apply different configurations to the topology.
    """

    def __init__(self):
        """
        Initializes the instance with a list of interface sets.
        """
        self.interface_sets = [
            {'interfaces': "S-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
            {'interfaces': "dummy-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
            {'interfaces': "fabric-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
        ]

        """
         self.interface_sets = [
             {'interfaces': "S-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
             {'interfaces': "D-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
             {'interfaces': "dummy-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
             {'interfaces': "fabric-", 'start': INTERFACE_START, 'stop': INTERFACE_STOP},
         ]
        """

    def create_logical_interfaces(self, vinfra, bridge_echo=None):
        """
        Creates logical interfaces for the given virtual infrastructure.
        """
        for interface_set in self.interface_sets:
            vinfra.define_logical_interfaces(interface_set['interfaces'], interface_set['start'], interface_set['stop'])
            vinfra.create_logical_interfaces(bridge_echo)

    def delete_logical_interfaces(self, vinfra):
        """
        Deletes logical interfaces for the given virtual infrastructure.
        """
        for interface_set in self.interface_sets:
            vinfra.define_logical_interfaces(interface_set['interfaces'], interface_set['start'], interface_set['stop'])
            vinfra.delete_interface()

    def create_and_configure_device(self):
        """
        Creates and configures a Juniper device.
        """
        number_int = (INTERFACE_STOP - INTERFACE_START) + 1
        dev = ConfigureJuniperDevice(number_int, INTERFACE_START)
        return dev

    def countdown(self, time_sec):
        """
        Displays a countdown timer.
        """
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            sleep(1)
            time_sec -= 1

        print("stop")

    def create_data(self):
        """
        Generates data for the virtual network topology.
        """
        vlab1_data = GenerateData()
        vlab1_data.generate_data_info('lab1_device_info.xlsx', *DEVICE_TAB_LIST)

        dict_list = [
            ('vsrx', vlab1_data.get_srx),
            ('vex', vlab1_data.get_vex),
            ('vevo', vlab1_data.get_vevo),
            ('apstra', vlab1_data.get_apstra),
            ('linux', vlab1_data.get_linux),
        ]

        return dict_list

    def start_topology(self):
        """
        Starts the virtual network topology.
        """

        print("#" * 150)
        print("#" * 100, "Start Virtual Topology")

        vinfra = BasicInfra('lab1_byot')
        vinfra.clean_memory()
        self.create_logical_interfaces(vinfra, BRIDGE_ECHO)

        dict_list = self.create_data()

        for name, data_dict in dict_list:
            if data_dict:
                vmx_hostname_list = vinfra.get_virtual_vm_hostname(data_dict)
                vinfra.get_virtual_machine_status("destroyed", *vmx_hostname_list)
                vinfra.start_stop_virtual_machine("start")

        # Check connectivity (vmx vsrx3)
        vlab1conf = DevicesConfig()
        self.countdown(180)

        print("-" * 50, "Test MGMT Connectivity")
        for name, data_dict in dict_list:
            if data_dict and name not in ['apstra', 'linux']:
                vlab1conf.check_ping(data_dict)

    def stop_topology(self):
        """
        Stops the virtual network topology.
        """
        print("#" * 150)
        print("#" * 100, "Stop Virtual Topology")
    
        vinfra = BasicInfra('lab1_byot')
        vlab1 = BasicJuniper('lab1_byot')
        vlab1_data = GenerateData()
        tab_list = DEVICE_TAB_LIST
        vlab1_data.generate_data_info('lab1_device_info.xlsx', *tab_list)
        vex_dict = vlab1_data.get_vex

        # Shutdown vjunos-switch

        if vex_dict:
            vlab1.shutdown_vjunos_switch(vex_dict)
            print("Wait 30 seconds to shutdown vjunos-switch")
            self.countdown(30)

        dict_list = self.create_data()

        for name, data_dict in dict_list:
            if data_dict:
                vmx_hostname_list = vinfra.get_virtual_vm_hostname(data_dict)
                vinfra.get_virtual_machine_status("running", *vmx_hostname_list)
                vinfra.start_stop_virtual_machine("destroy")

        self.delete_logical_interfaces(vinfra)

        vinfra.clean_memory()

    def create_topology(self):
        """
        Creates the virtual network topology.
        """
    
        print("#" * 150)
        print("#" * 100, "Create Virtual Topology - lab1_byot")

        # Create objects, device info dictonary etc.
        vinfra = BasicInfra('lab1_byot')
        vlab1 = BasicJuniper('lab1_byot')

        vinfra.clean_memory()

        self.create_logical_interfaces(vinfra, BRIDGE_ECHO)

        dict_list = self.create_data()

        device_list_map = {
            'vsrx': vlab1.create_srx,
            'vex': vlab1.create_vex,
            'vevo': vlab1.create_vevo,
            'apstra': vlab1.create_aos,
            'linux': vinfra.createVirtualVms,
        }

        for name, data_dict in dict_list:
            if data_dict:
                print(f"Creating {name}...")
                create_to_call = device_list_map.get(name)
                if create_to_call:
                    try:
                        create_to_call(data_dict)
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print(f"Unknown type: {name}")

        # Check connectivity
        vlab1conf = DevicesConfig()
        self.countdown(420)

        print("-" * 50, "Test MGMT Connectivity")
        for name, data_dict in dict_list:
            if data_dict and name not in ['apstra', 'linux']:
                vlab1conf.check_ping(data_dict)

        # Save Baseline config
        print("-" * 50, "Save Baseline config")
        for name, data_dict in dict_list:
            if data_dict and name not in ['apstra', 'linux']:
                vlab1.create_baseline_config(data_dict)

    def delete_topology(self):
        """
        dDeletes the virtual network topology.
        """
    
        print("#" * 150)
        print("#" * 100, "Delete Virtual Topology")
    
        vinfra = BasicInfra('lab1_byot')

        dict_list = self.create_data()

        for name, data_dict in dict_list:
            if data_dict:
                vinfra.delete_virtual_lab(data_dict)

        self.delete_logical_interfaces(vinfra)

        vinfra.clean_memory()

    def configure_isis_topology(self):
        """
        Applies an ISIS base configuration to the topology.
        """
    
        print("#" * 150)
        print("#" * 100, "Apply lab1_byot ISIS base configuration")

        """
        Create topology with ISIS as IGP
        """

        dev = self.create_and_configure_device()
        dev.get_data()
        dev.configure_loopback_interface_iso()
        dev.configure_physical_interface_iso()
        dev.configure_policies()
        dev.configure_protocols_iso()
        dev.configure_basic_bgp()
        dev.configure_bgp_ibgp_neighbor_client_to_rr()
        dev.configure_bgp_ibgp_neighbor_rr_to_client()

    def configure_ospf_topology(self):
        """
        Applies an OSPF base configuration to the topology.
        """
        print("#" * 150)
        print("#" * 100, "Apply lab1_byot OSPF base configuration")

        """
        Create topology with OSPF as IGP
        """

        # # Define number of interfaces
        # number_int = (interface_stop - interface_start) + 1
        #
        # # Call configureJuniperDevice, which will configure a lot of things
        # dev = ConfigureJuniperDevice(number_int, interface_start)

        dev = self.create_and_configure_device()
        dev.get_data()
        dev.configure_loopback_interface()
        dev.configure_physical_interface()
        dev.configure_policies()
        dev.configure_protocols()
        dev.configure_basic_bgp()
        dev.configure_bgp_ibgp_neighbor_client_to_rr()
        dev.configure_bgp_ibgp_neighbor_rr_to_client()

    def configure_interfaces_topology_iso(self):
        """
        Applies a basic P2P and Loopback interfaces configuration with ISO support.
        """
        print("#" * 150)
        print("#" * 100, "Apply lab1_byot P2P and Loopback basic configuration with ISIS support")

        """
        Configure interfaces loopback and p2p only - IPv4 and IPv6 and ISO
        """

        dev = self.create_and_configure_device()
        dev.get_data()
        dev.configure_loopback_interface_iso()
        dev.configure_physical_interface_iso()

    def configure_interfaces_topology(self):
        """
        Applies a basic P2P and Loopback interfaces configuration.
        """
        print("#" * 150)
        print("#" * 100, "Apply lab1_byot P2P and Loopback basic configuration")

        """
        Configure interfaces loopback and p2p only - IPv4 and IPv6
        """

        dev = self.create_and_configure_device()
        dev.get_data()
        dev.configure_loopback_interface()
        dev.configure_physical_interface()

    def configure_baseline(self):
        """
        Overwrites the current configuration with the baseline configuration.
        """
        print("#" * 150)
        print("#" * 100, "Apply lab1_byot baseline configuration overwrite")

        """
        Script load overwrite the baseline configuration creating during the basic configuration step when creating the
        topology from scratch. 
        """

        print("#" * 150)
        print("#" * 100, "Create Virtual Topology - lab1_byot")

        # Create objects, device info dictonary etc.
        vlab1 = BasicJuniper('lab1_byot')

        dict_list = self.create_data()

        for name, data_dict in dict_list:
            if data_dict and name not in ['apstra', 'linux']:
                vlab1.load_baseline(data_dict)

    def get_device_config(self):
        """
        Retrieves and saves the device configuration.
        """
        print("#" * 150)
        print("#" * 100, "Get and Save labconfig")

        # call class to send the main config to R1, R2 and VR-Device(vSRX RI simulating Servers)
        vlab1 = BasicJuniper('lab1_byot')

        dict_list = self.create_data()

        for name, data_dict in dict_list:
            if data_dict and name not in ['apstra', 'linux']:
                vlab1.save_config_local(data_dict)

    def save_baseline(self):
        """
        Retrieves and saves the device configuration.
        """
        print("#" * 150)
        print("#" * 100, "Get and Save labconfig")

        # call class to send the main config to R1, R2 and VR-Device(vSRX RI simulating Servers)
        vlab1 = BasicJuniper('lab1_byot')

        dict_list = self.create_data()

        print("-" * 50, "Save Baseline config")
        for name, data_dict in dict_list:
            if data_dict and name not in ['apstra', 'linux']:
                vlab1.create_baseline_config(data_dict)


if __name__ == "__main__":

    def run_and_measure_time(func):
        start_time = time()
        func()
        run_time = time() - start_time
        run_time_min = run_time / 60
        print(f'Time to configure: {run_time_min:2f}')

    a = MainScript()

    functions_map = {
        '1': ("Start Topology", a.start_topology),
        '2': ("Stop Topology", a.stop_topology),
        '3': ("Create topology", a.create_topology),
        '4': ("Delete topology", a.delete_topology),
        '5': ("Configure ISIS topology - Basic topology based on ISIS", a.configure_isis_topology),
        '6': ("Configure OSPF topology - Basic topology based on OSPF", a.configure_ospf_topology),
        '7': ("Configure Interfaces only - Basic P2P and Loopback interfaces with iso family",
              a.configure_interfaces_topology_iso),
        '8': ("Configure Interfaces only - Basic P2P and Loopback interfaces", a.configure_interfaces_topology),
        '9': ("Load Baseline Config - Overwrite current configuration with baseline config", a.configure_baseline),
        '10': ("Save Config", a.get_device_config),
        '11': ("Create Router baseline config", a.save_baseline),
    }

    if len(sys.argv) > 1:
        select_function = sys.argv[1]
    else:
        for k, v in functions_map.items():
            print(f"{k} - {v[0]}\n")
        select_function = input("Select one Option: ") or None

    if select_function in functions_map:
        if select_function in ['3', '4']:
            print(f"Are you sure you want to {functions_map[select_function][0]}?")
            confirm = input("Type 'yes' or 'no': ").lower()
            if confirm not in ['yes', 'y']:
                print("Operation cancelled.")
                exit()
        run_and_measure_time(functions_map[select_function][1])
    else:
        print("Wrong option!! Nothing to do!")
