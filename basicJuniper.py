"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""
import pprint
#import sys
#sys.path.append('./')
import subprocess
from time import sleep
from juniperTemplates import BasicConfigTemplateJuniper
from exception_handler import *
from virt_install_templates import *


class BasicJuniper:

    def __init__(self, lab_name: str):
        self.interface_list = []
        self.vrdc_list = []
        self.source_images = f'/opt/src_virtual_lab_images/'
        self.libvirt_images_path = '/var/lib/libvirt/images/'

    def run_command(self, command):

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{command}' failed with error: {e}")

    def peek_first_interface(self, file_path: str):
        """
        Function to peek the first interface from a file
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if not lines:
            return None

        first_interface = lines[0].strip()

        return first_interface

    def get_and_remove_first_interface(self, file_path: str):
        """
        Get the first interface from the file and remove it from the file
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if not lines:
            print(f"No interface to remove in {file_path}")
            return None

        first_interface = lines.pop(0).strip()

        with open(file_path, 'w') as file:
            for line in lines:
                file.write(line)

        # print(f"First interface '{first_interface}' has been removed from {file_path}")

        return first_interface

    def update_interfaces(self, int_values, file_path: str):
        """
        Update interface values replacing 'None' with an interface from file
        """
        replacement_interface = None
        for k, v in int_values.items():
            if v == 'None':
                if replacement_interface is None:
                    replacement_interface = self.get_and_remove_first_interface(file_path)
                int_values[k] = replacement_interface

        return int_values, replacement_interface

    @staticmethod
    def convert_to_list(string_name):

        li = list(string_name.split(","))
        return li

    def create_srx(self, data):

        """
        Create vSRX3 - Juniper
        """

        print("-" * 120)
        print("-" * 50, "Creating vSRX3")

        a = BasicConfigTemplateJuniper()


        db = data
        # pprint.pprint(db) # to debug

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'vsrx3':
                    version = i['version']
                    hostname = i['hostname']
                    mgmt_int = i['mgmt_int']
                    mgmt_ip = i['mgmt_ip']

                    # Old fix interfaces columns
                    # int_values = {f'int{j}': i[f'ge-0/0/{j}'] for j in range(12)}

                    # variable interfaces columns
                    int_values = {k: v for k, v in i.items() if k.startswith('ge-')}

                    int_values, _ = self.update_interfaces(int_values, 'dummy_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}/{mgmt_ip}")

                    # Get template with variables
                    config = a.vjunos_vsrx3(hostname, mgmt_ip)

                    config_name = '../config/juniper.conf'
                    to_file = open(config_name, 'w')
                    to_file.write(config)
                    to_file.close()

                    # create iso_dir
                    mkdir_config = f'mkdir ../config/iso_dir'
                    subprocess.call(mkdir_config, shell=True)

                    # copy config to iso_dir
                    cp_config = f'cp {config_name} ../config/iso_dir'
                    subprocess.call(cp_config, shell=True)

                    # generate disk into final directory
                    vm_config = f'{hostname}.iso'
                    create_iso = f'mkisofs -l -o {self.libvirt_images_path}{vm_config} ../config/iso_dir'
                    subprocess.call(create_iso, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    # clean iso_dir
                    rm_config = f'rm -rf {config_name} ../config/iso_dir'
                    subprocess.call(rm_config, shell=True)

                    vm_img = f'{hostname}.qcow2'

                    copy_vm = f'cp {self.source_images}vsrx3-{version}/junos-vsrx*.qcow2 ' \
                                f'{self.libvirt_images_path}{vm_img}'

                    subprocess.call(copy_vm, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)


                    virt_data = generate_virt_template_vsrx3(hostname, self.libvirt_images_path,
                                                             mgmt_int, int_values, vm_img, vm_config)
                    # pprint.pp(virt_data)  # to debug
                    subprocess.run(virt_data, shell=True)

                    sleep(15)

    def create_vex(self, data):

        """
        Create vjunos-switch(VEX) - Juniper
        """

        print("-" * 120)
        print("-" * 50, "Creating vJunos-Switch")

        a = BasicConfigTemplateJuniper()

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'vex':
                    version = i['version']
                    hostname = i['hostname']
                    mgmt_int = i['mgmt_int']
                    mgmt_ip = i['mgmt_ip']

                    # Old fix interfaces columns
                    # int_values = {f'int{j}': i[f'ge-0/0/{j}'] for j in range(10)}

                    # variable interfaces columns
                    int_values = {k: v for k, v in i.items() if k.startswith('ge-')}

                    int_values, _ = self.update_interfaces(int_values, 'dummy_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}/{mgmt_ip}")

                    # Get template with variables
                    config = a.vjunos_switch(hostname, mgmt_ip)

                    # Create a local file with config
                    config_name = '../config/juniper.conf'
                    to_file = open(config_name, 'w')
                    to_file.write(config)
                    to_file.close()

                    # make-config.sh executable
                    per_make_config = f'chmod 755 ../config/make-config.sh'
                    subprocess.call(per_make_config, shell=True)

                    # Define config disk name and generate disk
                    vm_config = f'{hostname}.img'
                    script_path = f'../config/make-config.sh'
                    create_disk_config = f'{script_path} {config_name} {self.libvirt_images_path}{vm_config}'
                    subprocess.call(create_disk_config, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    vm_img = f'{hostname}.qcow2'

                    copy_vm = f'cp {self.source_images}vjunos-switch-{version}/*.qcow2 ' \
                                f'{self.libvirt_images_path}{vm_img}'

                    subprocess.call(copy_vm, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    virt_data = generate_virt_template_vex(hostname, self.libvirt_images_path, mgmt_int,
                                                           int_values, vm_img, vm_config)
                    # pprint.pp(virt_data)  # to debug
                    subprocess.run(virt_data, shell=True)

                    sleep(10)

    def create_vjunos_router(self, data):

        """
        Create vjunos-router(VMX) - Juniper
        """

        print("-" * 120)
        print("-" * 50, "Creating vJunos-router")

        a = BasicConfigTemplateJuniper()

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'vrouter':
                    version = i['version']
                    hostname = i['hostname']
                    mgmt_int = i['mgmt_int']
                    mgmt_ip = i['mgmt_ip']

                    # Old fix interfaces columns
                    # int_values = {f'int{j}': i[f'ge-0/0/{j}'] for j in range(10)}

                    # variable interfaces columns
                    int_values = {k: v for k, v in i.items() if k.startswith('ge-')}

                    int_values, _ = self.update_interfaces(int_values, 'dummy_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}/{mgmt_ip}")

                    # Get template with variables
                    config = a.vjunos_router(hostname, mgmt_ip)

                    # Create a local file with config
                    config_name = '../config/juniper.conf'
                    to_file = open(config_name, 'w')
                    to_file.write(config)
                    to_file.close()

                    # make-config.sh executable
                    per_make_config = f'chmod 755 ../config/make-config.sh'
                    subprocess.call(per_make_config, shell=True)

                    # Define config disk name and generate disk
                    vm_config = f'{hostname}.img'
                    script_path = f'../config/make-config.sh'
                    create_disk_config = f'{script_path} {config_name} {self.libvirt_images_path}{vm_config}'
                    subprocess.call(create_disk_config, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    vm_img = f'{hostname}.qcow2'

                    copy_vm = f'cp {self.source_images}vjunos-router-{version}/*.qcow2 ' \
                                f'{self.libvirt_images_path}{vm_img}'

                    subprocess.call(copy_vm, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    virt_data = generate_virt_template_vjunos_router(hostname, self.libvirt_images_path, mgmt_int,
                                                                     int_values, vm_img, vm_config)
                    #pprint.pp(virt_data)  # to debug
                    subprocess.run(virt_data, shell=True)

                    sleep(10)

    def create_aos(self, data):

        """
        Create Apstra Server - Juniper
        """
        print("-" * 120)
        print("-" * 50, "Creating Apstra Server")

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'apstra_server':
                    version = i['version']
                    hostname = i['hostname']
                    mgmt_int = i['mgmt_int']
                    mgmt_ip = i['mgmt_ip']

                    print("-" * 30, f"Creating: {hostname}/{mgmt_ip}")

                    vm_img = f'{hostname}.qcow2'

                    copy_vm = f'cp {self.source_images}apstra-{version}/*.qcow2 ' \
                                  f'{self.libvirt_images_path}{vm_img}'

                    subprocess.call(copy_vm, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    virt_data = generate_virt_template_apstra(hostname, self.libvirt_images_path, mgmt_int, vm_img)
                    # pprint.pp(virt_data)  # to debug
                    subprocess.run(virt_data, shell=True)

                    sleep(10)

    def create_vevo(self, data):

        """
        Create vjunos-evolved - Juniper
        """

        print("-" * 120)
        print("-" * 50, "Creating vJunos-Evolved")

        a = BasicConfigTemplateJuniper()

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'vevo':
                    channelized = i['channelized']
                    version = i['version']
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']
                    mgmt_int = i['mgmt_int']
                    pfe_link = self.get_and_remove_first_interface('fabric_interfaces.txt')
                    rpio_link = self.get_and_remove_first_interface('fabric_interfaces.txt')

                    # Old fix interfaces columns
                    # int_values = {f'int{j}': i[f'et-0/0/{j}'] for j in range(12)}

                    # variable interfaces columns
                    int_values = {k: v for k, v in i.items() if k.startswith('et-')}

                    int_values, _ = self.update_interfaces(int_values, 'dummy_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}/{mgmt_ip}")

                    # Get template with variables
                    config = a.vjunos_evolved(hostname, mgmt_ip)

                    # Create a local file with config
                    config_name = '../config/juniper.conf'
                    to_file = open(config_name, 'w')
                    to_file.write(config)
                    to_file.close()

                    # make-config.sh executable
                    per_make_config = f'chmod 755 ../config/make-config.sh'
                    subprocess.call(per_make_config, shell=True)

                    # Define config disk name and generate disk
                    vm_config = f'{hostname}.img'
                    script_path = f'../config/make-config.sh'
                    create_disk_config = f'{script_path} {config_name} {self.libvirt_images_path}{vm_config}'
                    subprocess.call(create_disk_config, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    vm_img = f'{hostname}.qcow2'
                    copy_vm = f'cp {self.source_images}vjunos-evolved-{version}/*.qcow2 ' \
                                f'{self.libvirt_images_path}{vm_img}'

                    subprocess.call(copy_vm, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    virt_data = generate_virt_template_vevo(hostname, self.libvirt_images_path, mgmt_int, pfe_link,
                                                            rpio_link, int_values, vm_img, vm_config,channelized)
                    # pprint.pp(virt_data)  # to debug
                    subprocess.run(virt_data, shell=True)

                    sleep(10)

    def create_vmx(self, data):

        """
        Create vMX (Official) - Juniper
        """

        print("-" * 120)
        print("-" * 50, "Creating vMX")

        a = BasicConfigTemplateJuniper()

        db = data

        for key, value in db.items():
            for i in value['data']:

                if i['type'] == 'vmx-vcp':
                    version = i['version']
                    hostname = i['hostname']
                    mgmt_int = i['mgmt_int']
                    mgmt_ip = i['mgmt_ip']
                    fabric_int = self.peek_first_interface('fabric_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}/{mgmt_ip}")

                    # Get template with variables
                    config = a.vjunos_vmx(hostname, mgmt_ip)

                    # Create a local file with config
                    config_name = '../config/juniper.conf'
                    to_file = open(config_name, 'w')
                    to_file.write(config)
                    to_file.close()

                    # make-config.sh executable
                    per_make_config = f'chmod 755 ../config/make-vmx-config.sh'
                    subprocess.call(per_make_config, shell=True)

                    # Define config disk name and generate disk
                    script_path = f'../config/make-vmx-config.sh'
                    create_disk_config = f'{script_path} {config_name}'
                    subprocess.call(create_disk_config, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    # subprocess.call(create_disk_config, shell=True)

                    vcp_img = f'{hostname}.qcow2'
                    hdd_img = f'{hostname}_hdd.img'
                    metadata_img = f'{hostname}_metadata.img'
                    copy_vcp = f'cp {self.source_images}vmx-{version}/*.qcow2 ' \
                               f'{self.libvirt_images_path}{vcp_img}'
                    copy_hdd = f'cp {self.source_images}vmx-{version}/vmxhdd.img ' \
                               f'{self.libvirt_images_path}{hdd_img}'
                    copy_metadata = f'mv ./metadata-usb-re.img ' \
                                    f'{self.libvirt_images_path}{metadata_img}'

                    subprocess.call(copy_vcp, shell=True)
                    subprocess.call(copy_hdd, shell=True)
                    subprocess.call(copy_metadata, shell=True)

                    """
                    # Old metadata
                    copy_metadata = f'cp {self.source_images}vmx-{version}/metadata-usb-re.img ' \
                                    f'{self.libvirt_images_path}{metadata_img}'
                    subprocess.call(copy_metadata, shell=True)
                    """

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    virt_data = generate_virt_template_vcp(hostname, self.libvirt_images_path, mgmt_int,
                                                           fabric_int, vcp_img, hdd_img,metadata_img)
                    # pprint.pp(virt_data)  # to debug

                    # print(virt_data)
                    subprocess.run(virt_data, shell=True)

                    sleep(15)

                if i['type'] == 'vmx-vfp':
                    version = i['version']
                    hostname = i['hostname']
                    fabric_int = self.get_and_remove_first_interface('fabric_interfaces.txt')

                    int_values = {k: v for k, v in i.items() if k.startswith('ge-')}
                    int_values, replacement_int = self.update_interfaces(int_values, 'dummy_interfaces.txt')

                    print("-" * 30, f"Creating: {hostname}")

                    vfp_img = f'{hostname}.img'
                    copy_vfp = f'cp {self.source_images}vmx-{version}/vFPC-*.img ' \
                               f'{self.libvirt_images_path}{vfp_img}'
                    subprocess.call(copy_vfp, shell=True)

                    change_permission = f'chmod 755 {self.libvirt_images_path}*'
                    subprocess.call(change_permission, shell=True)

                    virt_data = generate_virt_template_vfp(hostname, self.libvirt_images_path, replacement_int,
                                                           fabric_int, int_values,vfp_img)
                    # pprint.pp(virt_data)  # to debug
                    subprocess.run(virt_data, shell=True)

                    sleep(15)

    def clean_ssh_hosts(self):

        """
        clean /root/.ssh/known_hosts
        """

        clean_ssh = f'echo "" > /root/.ssh/known_hosts'
        subprocess.call(clean_ssh, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def save_config_local(self, data, port=22, user='lab', password='lab123'):

        """
        Save Juniper Virtual Devices config to local server
        """
        self.clean_ssh_hosts()

        print("#" * 50, "Save Config locally")

        db = data
        for key, value in db.items():
            for i in value['data']:
                if i['type'].upper() == 'VEX' or i['type'].upper() == 'VROUTER' \
                        or i['type'].upper() == 'VSRX3' or i['type'].upper() == 'VEVO':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']
                    print(f"- {mgmt_ip} -saving {hostname} config - see bkp_config directory")

                    handle_save_config_local(mgmt_ip, port, user, password, hostname)

    def create_baseline_config(self, data, port=22, user='lab', password='lab123'):

        """
        Create baseline file configuration after configure MGMT and HOSTNAME
        """

        self.clean_ssh_hosts()

        print("#" * 50, "Create Baseline")

        db = data
        for key, value in db.items():
            for i in value['data']:
                if i['type'].upper() == 'VEX' or i['type'].upper() == 'VROUTER' \
                        or i['type'].upper() == 'VSRX3' or i['type'].upper() == 'VEVO':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']
                    print(f"- {mgmt_ip} - Save {hostname}.conf\n")

                    handle_create_baseline_config(mgmt_ip, port, user, password)

    def load_baseline(self, data, port=22, user='lab', password='lab123'):

        """
        Load baseline file configuration with MGMT and HOSTNAME only
        """

        self.clean_ssh_hosts()

        print("#" * 50, "Baseline Config")

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'].upper() == 'VEX' or i['type'].upper() == 'VROUTER' \
                        or i['type'].upper() == 'VSRX3' or i['type'].upper() == 'VEVO':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']

                    print(f'-------Configuring {hostname}/({mgmt_ip}) with baseline config overwrite')
                    # print(data)
                    baseline_config = f'baseline.conf'

                    handle_load_baseline(mgmt_ip, port, user, password, baseline_config)

    def shutdown_vjunos(self, data, port=22, user='lab', password='lab123'):

        """
        Shutdown vjunos-switch only
        """
        self.clean_ssh_hosts()

        print("#" * 50, "Shutdown vJunos")

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'].upper() == 'VEX' or i['type'].upper() == 'VROUTER' or i['type'].upper() == 'VEVO':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']
                    print(f"- Shutdown: {hostname} \n")

                    poweroff_device(mgmt_ip, port=port, user=user, password=password)
                    

if __name__ == "__main__":
    pass