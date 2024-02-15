"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""

from basicJuniper import BasicJuniper
import subprocess
from re import search
from time import sleep
from exception_handler import *
import time

from basicJuniper import BasicJuniper

# Variable for Linux VM Size - Change it if you need more virtual disk space
linux_vmx_size = '15G'

class BasicInfra:

    def __init__(self, lab_name: str):
        self.lab_name = lab_name
        self.interface_list = []
        self.vrdc_list = []
        self.source_images = f'/opt/src_virtual_lab_images/'
        self.libvirt_images_path = '/var/lib/libvirt/images/'

    def countdown(self, time_sec):
        while time_sec:
            mins, secs = divmod(time_sec, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            sleep(1)
            time_sec -= 1

        print("stop")

    @staticmethod
    def clean_memory():

        """
        Clean linux memory
        """

        print("-" * 120)
        print("-" * 50, "Clean Memory")

        check_memory = 'free -g'
        free_memory = 'sync; echo 3 > /proc/sys/vm/drop_caches'
        subprocess.call(check_memory, shell=True)
        sleep(1)
        subprocess.call(free_memory, shell=True)
        subprocess.call(check_memory, shell=True)
        clean_known_hosts = 'echo > /root/.ssh/known_hosts'
        subprocess.call(clean_known_hosts, shell=True)
        sleep(1)

    def write_interfaces_to_file(self, file_path="interfaces.txt"):
        """
        Write the list of interfaces to a file
        """
        with open(file_path, 'w') as file:
            for interface in self.interface_list:
                file.write(f"{interface}\n")
        # print(f"Interface list has been written to {file_path}")

    def define_logical_interfaces(self, name="S-", int_start=1, int_stop=40):

        """
        Define virtual logical interfaces
        """
        print("-" * 120)
        print("-" * 50, f"Generate Logical Interface List - Name: {name}")

        self.interface_list = [name + str(fabric_interface) for fabric_interface in range(int_start, int_stop)]

        if name == 'dummy-':
            self.write_interfaces_to_file('dummy_interfaces.txt')
        if name == 'fabric-':
            self.write_interfaces_to_file('fabric_interfaces.txt')

    def create_logical_interfaces(self, bridge_echo=16384):

        """
        Create Logical Interfaces
        """
        print("-" * 120)
        print("-" * 50, "Create Logical Interfaces")

        for br_interface in self.interface_list:

            cmd_brctl = f'/sbin/ip link add name {br_interface} type bridge'
            cmd_ifconfig = f'/sbin/ip link set {br_interface} up'

            run_command(cmd_brctl, 'RTNETLINK answers: File exists')
            run_command(cmd_ifconfig, 'RTNETLINK answers: File exists')

            if not search('dummy', br_interface):
                # if all(x not in br_interface for x in ['fabric']):
                #     print(f"- configuring fwd_mask and MTU")

                lacp_ldp = f'echo {bridge_echo} > /sys/class/net/{br_interface}/bridge/group_fwd_mask'
                mtu_int = f'/sbin/ip link set dev {br_interface} mtu 9200'

                run_command(lacp_ldp, 'RTNETLINK answers: File exists')
                run_command(mtu_int, 'RTNETLINK answers: File exists')

            # if all(x not in br_interface for x in ['dummy', 'fabric']):
            #     print(f'- Creating Interface {br_interface}')

    def delete_interface(self):

        """
        Delete Logical Interfaces
        """

        print("-" * 120)
        print("-" * 50, "Delete Logical Interfaces")

        for br_interface in self.interface_list:

            cmd_ifconfig = f'/sbin/ip link set {br_interface} down'
            cmd_brctl = f'/sbin/ip link delete {br_interface} type bridge'

            if run_command_interface(cmd_ifconfig):
                run_command_interface(cmd_brctl)

            # if all(x not in br_interface for x in ['dummy', 'fabric']):
            #     print(f'- Deleting Interface {br_interface}')

    def get_virtual_machine_status(self, virsh_status="running", *args):

        """
        Get Virtual Machine Status
        """

        for vm in args:

            cmd_virsh_list = ''
            if virsh_status == "destroyed":
                cmd_virsh_list = f"virsh list --all | egrep {vm} | awk '{{print $2}}'"
            if virsh_status == "running":
                cmd_virsh_list = f"virsh list | egrep {vm} | awk '{{print $2}}'"

            # get the output of the cmd_virsh_list, strip and decode in utf-8 - necessary to clean the list output
            vrdc_info = subprocess.Popen(cmd_virsh_list, shell=True, stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')
            # creates list of the vrdc_info and clean the empty spaces
            self.vrdc_list.extend(vrdc_info.split("\n"))

    def start_stop_virtual_machine(self, virsh_action):

        """
        Start/Destroy - virsh
        """
        print("-" * 120)
        print("-" * 50, f"{virsh_action} - Virtual Machines")

        server_list = self.vrdc_list
        # print(server_list)

        for hostname in server_list:
            if hostname != '':
                print("-" * 10, f"{virsh_action} Virtual Image: {hostname}")
                command = f'/usr/bin/virsh {virsh_action} {hostname}'
                completed_process = subprocess.run(command, shell=True, capture_output=True, text=True)

                if "Domain is already active" in completed_process.stderr:
                    print(f"Skipping {hostname}, domain is already active.")
                elif completed_process.returncode != 0:
                    print(f"Error executing command for {hostname}. Error was {completed_process.stderr}")

        self.vrdc_list = []

    """
     command = f'/usr/bin/virsh {virsh_action} {server}'
                subprocess.call(command, shell=True)
                sleep(1)
    """

    def create_virtual_vm_dic(self, csv_file):

        """
        Create VMs Dict
        """
        file_handle = open(csv_file)
        hosts_info_dict = dict()
        for line in file_handle:
            words = line.split(',')
            hosts_info_dict.update({words[0]: dict()})
            n = len(words)
            for i in range(1, n - 1, 2):
                if words[0] in hosts_info_dict.keys():
                    hosts_info_dict[words[0]].update({words[i]: words[i + 1]})
        return hosts_info_dict

    def get_virtual_vm_hostname(self, data):

        """
        Get the hostname of the virtual VMs only
        """
        #virtual_hosts = self.createVirtualVmDic(data)

        db = data
        hostname_list = []
        for key, value in db.items():
            for i in value['data']:
                hostname = i['hostname']
                hostname_list.append(hostname)

        return hostname_list

    def createVirtualSonic(self, csv_file):

        """
        Create Virtual Enterprise Sonic - Dell
        """
        print("-" * 120)
        print("-" * 50, "Creating Datacenter Topology")

        copy_vrdc_img = f'cp {self.source_sonic_image} {self.ent_sonic_image}'
        subprocess.call(copy_vrdc_img, shell=True)

        virtual_hosts = self.create_virtual_vm_dic(csv_file)

        for i in virtual_hosts.keys():
            hostname = virtual_hosts[i].get('hostname')
            mgmt_int = virtual_hosts[i].get('mgmt_int')
            mgmt_ip = virtual_hosts[i].get('mgmt_ip')
            dummy_int = virtual_hosts[i].get('dummy_int')
            xe_1 = virtual_hosts[i].get('xe_1')
            xe_2 = virtual_hosts[i].get('xe_2')
            xe_3 = virtual_hosts[i].get('xe_3')
            xe_4 = virtual_hosts[i].get('xe_4')
            xe_5 = virtual_hosts[i].get('xe_5')
            xe_6 = virtual_hosts[i].get('xe_6')
            xe_7 = virtual_hosts[i].get('xe_7')
            xe_8 = virtual_hosts[i].get('xe_8')
            xe_9 = virtual_hosts[i].get('xe_9')
            xe_10 = virtual_hosts[i].get('xe_10')
            xe_11 = virtual_hosts[i].get('xe_11')
            xe_12 = virtual_hosts[i].get('xe_12')

            print("-" * 30, f'Creating Ent Virtual Sonic {i}')

            vrdc_vm = f'cp {self.ent_sonic_image} {self.image_path}{hostname}.img'

            subprocess.call(vrdc_vm, shell=True)

            install_vrdc = f'virt-install --name {hostname} \
            --memory 4096 \
            --vcpus=2 \
            --import \
            --os-variant generic \
            --nographics \
            --noautoconsole \
            --disk path={self.image_path}{hostname}.img,size=18,device=disk,bus=ide,format=qcow2 \
            --accelerate \
            --network bridge={mgmt_int},model=e1000 \
            --network bridge={dummy_int},model=e1000 \
            --network bridge={xe_1},model=e1000 \
            --network bridge={xe_2},model=e1000 \
            --network bridge={xe_3},model=e1000 \
            --network bridge={xe_4},model=e1000 \
            --network bridge={xe_5},model=e1000 \
            --network bridge={xe_6},model=e1000 \
            --network bridge={xe_7},model=e1000 \
            --network bridge={xe_8},model=e1000 \
            --network bridge={xe_9},model=e1000 \
            --network bridge={xe_10},model=e1000 \
            --network bridge={xe_11},model=e1000 \
            --network bridge={xe_12},model=e1000'

            subprocess.call(install_vrdc, bufsize=2000, shell=True)

            print("-", f'Starting Ent Virtual Sonic {i}')
            sleep(2)

    def createVirtualVms(self, data):

        """
        Create Virtual Linux - CENTOS
        """
        print("-" * 120)
        print("-" * 50, "Creating Hosts VMs")

        db = data

        a = BasicJuniper('lab1_device_info.xlsx')

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'centos' or i['type'] == 'ubuntu':
                    type = i['type']
                    version = i['version']
                    hostname = i['hostname']

                    int_values = {k: v for k, v in i.items() if k.startswith('eth')}
                    int_values, _ = a.update_interfaces(int_values, 'dummy_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}")

                    vm_img = f'{hostname}.qcow2'

                    if i['type'] == 'centos':
                        copy_vm = f'cp {self.source_images}{type}-{int(version)}/*.qcow2 ' \
                                  f'{self.libvirt_images_path}{vm_img}'

                        # Image used to expand the linux - will be deleted at the end of the routine
                        copy_vm_original = f'cp {self.source_images}{type}-{int(version)}/*.qcow2 ' \
                                           f'{self.libvirt_images_path}original.qcow2'

                        run_command(copy_vm)
                        run_command(copy_vm_original)
                        # create_img = f'qemu-img create -f qcow2 -o preallocation=metadata {self.libvirt_images_path}{vm_img} {linux_vmx_size}'
                        create_img = f'qemu-img create -f qcow2 {self.libvirt_images_path}{vm_img} {linux_vmx_size}'
                        exapand_img = f'virt-resize --expand /dev/sda1 {self.libvirt_images_path}original.qcow2 {self.libvirt_images_path}{vm_img}'
                        add_metadata = f'genisoimage -output {self.libvirt_images_path}{hostname}-config.iso -volid cidata ' \
                                       f'-joliet -r vm_config/{hostname}/user-data ' \
                                       f'vm_config/{hostname}/meta-data'

                        run_command(create_img)
                        run_command(exapand_img)
                        run_command(add_metadata)

                    if i['type'] == 'ubuntu':
                        # copy_vm = f'cp {self.source_images}{type}-{version}/*.img ' \
                        #           f'{self.libvirt_images_path}{vm_img}'

                        # Image used to expand the linux - will be deleted at the end of the routine
                        copy_vm_original = f'cp {self.source_images}{type}-{version}/*.img {self.libvirt_images_path}original.qcow2'

                        # subprocess.call(copy_vm, shell=True)
                        run_command(copy_vm_original)

                        create_img = f'qemu-img create -b {self.source_images}{type}-{version}/*.img -f qcow2 -F qcow2 {self.libvirt_images_path}{vm_img} {linux_vmx_size}'
                        run_command(create_img)
                        sleep(1)
                        add_metadata = f'genisoimage -output {self.libvirt_images_path}{hostname}-config.iso -volid cidata -joliet -r vm_config/{hostname}/user-data vm_config/{hostname}/meta-data'
                        run_command(add_metadata)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    run_command(change_permission)

                    network_bridges = []
                    for int_key, int_val in int_values.items():
                        network_bridges.append(f'--network bridge={int_val},model=e1000,mtu.size=9600')
                    network_bridge_str = ' \\\n'.join(network_bridges)

                    install_c_vm = f'''virt-install --import --name {hostname} \\
                                            --memory 1024 \\
                                            --vcpus=1 \\
                                            --disk path={self.libvirt_images_path}{vm_img},format=qcow2,bus=virtio \\
                                            --disk path={self.libvirt_images_path}{hostname}-config.iso,device=cdrom \\
                                            --os-variant=generic \\
                                            --graphics vnc,listen=0.0.0.0 \\
                                            --noautoconsole \\
                                            --accelerate \\
                                            {network_bridge_str}'''
                    run_command(install_c_vm)


        delete_vm_original = f'rm -f {self.libvirt_images_path}original.qcow2'
        subprocess.call(delete_vm_original, shell=True)

        # OLD LINUX CONFIG - 14/FEB/2024

        """
        # Copy generic centos to /var/lib/libvirt/images/ - we need it once we use this base image to create the vms

        generic_centos = '/var/lib/libvirt/images/CentOS-7-x86_64-GenericCloud.qcow2'
        copy_linux = f'cp {self.source_images}linux/CentOS-7-x86_64-GenericCloud.qcow2 {self.libvirt_images_path}'
        subprocess.call(copy_linux, shell=True)

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'linux':
                    version = i['version']
                    hostname = i['hostname']
                    bond = i['bond']
                    eth0 = i['eth0']
                    eth1 = i['eth1']
                    eth2 = i['eth2']

                    linux_image = f'{hostname}.qcow2'

                    subprocess.call(copy_linux, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    print("-" * 30, f'Creating VM {hostname}')

                    create_img = f'qemu-img create -f qcow2 -o preallocation=metadata {self.libvirt_images_path}{linux_image} 15G'
                    exapand_img = f'virt-resize --expand /dev/sda1 {generic_centos} {self.libvirt_images_path}{linux_image}'
                    add_metadata = f'genisoimage -output {self.libvirt_images_path}{hostname}-config.iso -volid cidata ' \
                                   f'-joliet -r vm_config/{hostname}/user-data ' \
                                   f'vm_config/{hostname}/meta-data vm_config/{hostname}/network-config'

                    # call command from exception_handler
                    run_command(create_img)
                    run_command(exapand_img)
                    run_command(add_metadata)

                    if bond == True:
                        install_c_vm = f'virt-install --import --name {hostname} \
                        --memory 1024 \
                        --vcpus=1 \
                        --disk path={self.libvirt_images_path}{linux_image},format=qcow2,bus=virtio \
                        --disk path={self.libvirt_images_path}{hostname}-config.iso,device=cdrom \
                        --network bridge={eth0},model=e1000 \
                        --network bridge={eth1},model=e1000 \
                        --network bridge={eth2},model=e1000 \
                        --os-variant=rhel7.0 \
                        --noautoconsole \
                        --accelerate'
                        # call command from exception_handler
                        run_command(install_c_vm)
                    else:
                        install_c_vm = f'virt-install --import --name {hostname} \
                        --memory 1024 \
                        --vcpus=1 \
                        --disk path={self.libvirt_images_path}{linux_image},format=qcow2,bus=virtio \
                        --disk path={self.libvirt_images_path}{hostname}-config.iso,device=cdrom \
                        --network bridge={eth0},model=e1000 \
                        --network bridge={eth1},model=e1000 \
                        --os-variant=rhel7.0 \
                        --noautoconsole \
                        --accelerate'
                        # call command from exception_handler
                        run_command(install_c_vm)
        """

    def delete_virtual_lab(self, data):

        """
        Delete Virtual LAB Topology
        """
        print("-" * 120)
        print("-" * 50, "Deleting Virtual Topology")

        db = data

        for key, value in db.items():
            for i in value['data']:
                hostname = i['hostname']

                print("-" * 30, f"Deleting Virtual Image: {hostname}")
                destroy_image = f'virsh destroy {hostname}'
                undefine_image = f'virsh undefine {hostname}'
                delete_image = f"rm -f {self.libvirt_images_path}{hostname}*"

                # call command from exception_handler
                run_command_delete_image(destroy_image, 'failed to get domain', hostname)
                run_command_delete_image(undefine_image, 'no domain with matching name', hostname)
                run_command_delete_image(delete_image, '', hostname)

    def delete_source_images(self):

        """
        Clean /var/lib/libvirt/images
        """
        print("-" * 120)
        print("-" * 50, "Removing Source Images: /var/lib/libvirt/images/")

        del_src_img = f'rm -rf images/*'
        print(del_src_img)

