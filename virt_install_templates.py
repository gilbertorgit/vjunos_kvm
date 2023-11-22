"""
---------------------------------
 Author: gilbertorgit
 Date: 05/2023
---------------------------------
"""


def generate_virt_template_vsrx3(hostname, images_path, mgmt_int, int_values, vm_img, vm_config):
    network_bridges = []
    for int_key, int_val in int_values.items():
        network_bridges.append(f'--network bridge={int_val},model=virtio,mtu.size=9600')
    network_bridge_str = ' \\\n'.join(network_bridges)

    install_vm = f'''virt-install \\
--name {hostname} \\
--accelerate \\
--import \\
--memory 4096 \\
--vcpus=2 \\
--os-variant=rhel7.0 \\
--nographics \\
--noautoconsole \\
--disk path={images_path}{vm_img},size=16,device=disk,bus=ide,format=qcow2 \\
--disk path={images_path}{vm_config},bus=ide,format=raw,target=hdc,device=cdrom \\
--network bridge={mgmt_int},model=virtio \\
{network_bridge_str}'''

# --network bridge={int_values["int0"]},model=virtio \\
# --network bridge={int_values["int1"]},model=virtio \\
# --network bridge={int_values["int2"]},model=virtio \\
# --network bridge={int_values["int3"]},model=virtio \\
# --network bridge={int_values["int4"]},model=virtio \\
# --network bridge={int_values["int5"]},model=virtio \\
# --network bridge={int_values["int6"]},model=virtio \\
# --network bridge={int_values["int7"]},model=virtio \\
# --network bridge={int_values["int8"]},model=virtio \\
# --network bridge={int_values["int9"]},model=virtio \\
# --network bridge={int_values["int10"]},model=virtio \\
# --network bridge={int_values["int11"]},model=virtio'''

    return install_vm


def generate_virt_template_vex(hostname, images_path, mgmt_int, int_values, vm_img, vm_config):
    network_bridges = []
    for int_key, int_val in int_values.items():
        network_bridges.append(f'--network bridge={int_val},model=virtio,mtu.size=9600')
    network_bridge_str = ' \\\n'.join(network_bridges)

    install_vm = f'''virt-install \\
--name {hostname} \\
--accelerate \\
--vcpus 4 \\
--ram 6000 \\
--import \\
--autostart \\
--noautoconsole \\
--accelerate \\
--os-variant ubuntu18.04 \\
--nographics \\
--serial pty \\
--hvm --cpu IvyBridge,require=vmx \\
--sysinfo smbios,system_product=VM-VEX \\
--disk path={images_path}{vm_img},cache=directsync,bus=virtio,size=10 \\
--disk path={images_path}{vm_config},bus=usb,format=raw \\
--network bridge={mgmt_int},model=virtio \\
{network_bridge_str}'''

    #     install_vm = f'''virt-install \
# --name {hostname} \
# --accelerate \
# --vcpus 4 \
# --ram 6000 \
# --import \
# --autostart \
# --noautoconsole \
# --accelerate \
# --os-variant ubuntu18.04 \
# --nographics \
# --serial pty \
# --hvm --cpu IvyBridge,require=vmx \
# --sysinfo smbios,system_product=VM-VEX \
# --disk path={images_path}{vm_img},cache=directsync,bus=virtio,size=10 \
# --disk path={images_path}{vm_config},bus=usb,format=raw \
# --network bridge={mgmt_int},model=virtio \
# --network bridge={int_values["int0"]},model=virtio \
# --network bridge={int_values["int1"]},model=virtio \
# --network bridge={int_values["int2"]},model=virtio \
# --network bridge={int_values["int3"]},model=virtio \
# --network bridge={int_values["int4"]},model=virtio \
# --network bridge={int_values["int5"]},model=virtio \
# --network bridge={int_values["int6"]},model=virtio \
# --network bridge={int_values["int7"]},model=virtio \
# --network bridge={int_values["int8"]},model=virtio \
# --network bridge={int_values["int9"]},model=virtio'''

    return install_vm


def generate_virt_template_apstra(hostname, images_path, mgmt_int, vm_img):
    install_vm = f'''virt-install --name={hostname} \\
--accelerate \\
--vcpu=8 \\
--ram=32768 \\
--import \\
--disk={images_path}{vm_img} \\
--os-variant ubuntu16.04 \\
--network bridge={mgmt_int},model=virtio \\
--noautoconsole'''

    return install_vm


def generate_virt_template_vevo(hostname, images_path, mgmt_int, pfe_link, rpio_link, int_values, vm_img, vm_config,
                                channelized):
    network_bridges = []
    for int_key, int_val in int_values.items():
        network_bridges.append(f'--network bridge={int_val},model=virtio,mtu.size=9600')
    network_bridge_str = ' \\\n'.join(network_bridges)

    install_vm = f'''virt-install \\
--name {hostname} \\
--accelerate \\
--vcpus 4 \\
--ram 8192 \\
--import \\
--autostart \\
--noautoconsole \\
--os-variant generic \\
--nographics \\
--serial pty \\
--cpu IvyBridge,+vmx \\
--qemu-commandline="-smbios type=0,vendor=Bochs,version=Bochs -smbios type=3,manufacturer=Bochs -smbios type=1,manufacturer=Bochs,product=Bochs,serial=chassis_no=0:slot=0:type=1:assembly_id=0x0D20:platform=251:master=0:channelized={channelized}" \\
--disk path={images_path}{vm_img},cache=directsync,bus=virtio,size=10 \\
--disk path={images_path}{vm_config},bus=usb,format=raw \\
--network bridge={mgmt_int},model=virtio \\
--network bridge={pfe_link},model=virtio \\
--network bridge={rpio_link},model=virtio \\
--network bridge={rpio_link},model=virtio \\
--network bridge={pfe_link},model=virtio \\
{network_bridge_str}'''

#
# --network bridge={int_values["int0"]},model=virtio \\
# --network bridge={int_values["int1"]},model=virtio \\
# --network bridge={int_values["int2"]},model=virtio \\
# --network bridge={int_values["int3"]},model=virtio \\
# --network bridge={int_values["int4"]},model=virtio \\
# --network bridge={int_values["int5"]},model=virtio \\
# --network bridge={int_values["int6"]},model=virtio \\
# --network bridge={int_values["int7"]},model=virtio \\
# --network bridge={int_values["int8"]},model=virtio \\
# --network bridge={int_values["int9"]},model=virtio \\
# --network bridge={int_values["int10"]},model=virtio \\
# --network bridge={int_values["int11"]},model=virtio'''

    return install_vm


def generate_virt_template_vjunos_router(hostname, images_path, mgmt_int, int_values, vm_img, vm_config):
    network_bridges = []
    for int_key, int_val in int_values.items():
        network_bridges.append(f'--network bridge={int_val},model=virtio,mtu.size=9600')
    network_bridge_str = ' \\\n'.join(network_bridges)

    install_vm = f'''virt-install \\
--name {hostname} \\
--accelerate \\
--vcpus 4 \\
--ram 6000 \\
--import \\
--autostart \\
--noautoconsole \\
--accelerate \\
--os-variant ubuntu18.04 \\
--nographics \\
--serial pty \\
--hvm --cpu IvyBridge,require=vmx \\
--sysinfo smbios,system_product=VM-VMX,system.family=lab \\
--disk path={images_path}{vm_img},cache=directsync,bus=virtio,size=10 \\
--disk path={images_path}{vm_config},bus=usb,format=raw \\
--network bridge={mgmt_int},model=virtio \\
{network_bridge_str}'''

    return install_vm


def generate_virt_template_vcp(hostname, images_path, mgmt_int, fabric_int, vcp_img, hdd_img, metadata_img):

    install_vm = f'''virt-install \\
--name {hostname} \\
--accelerate \\
--import \\
--ram=2048 \\
--vcpus=1,threads=1,cores=1 \\
--arch x86_64 \\
--machine=pc \\
--cpu host \\
--features acpi=on,apic=on,pae=on \\
--sysinfo smbios,bios_vendor=Juniper,system_manufacturer=VMX,system_product=VM-vcp_vmx1-161-re-0,system_version=0.1.0 \\
--disk path={images_path}{vcp_img},cache=directsync,bus=virtio,format=qcow2 \\
--disk path={images_path}{hdd_img},cache=directsync,bus=virtio,format=qcow2 \\
--disk path={images_path}{metadata_img},cache=directsync,bus=virtio,format=raw \\
--graphics vnc,listen=0.0.0.0 \\
--noautoconsole \\
--os-variant generic \\
--network bridge={mgmt_int},model=virtio \\
--network bridge={fabric_int},model=virtio'''

    return install_vm


def generate_virt_template_vfp(hostname, images_path, replacement_int, fabric_int, int_values, vfp_img):
    network_bridges = []
    for int_key, int_val in int_values.items():
        network_bridges.append(f'--network bridge={int_val},model=virtio,mtu.size=9600')
    network_bridge_str = ' \\\n'.join(network_bridges)

    install_vm = f'''virt-install \\
--name {hostname} \\
--accelerate \\
--import \\
--ram=2048 \\
--vcpus=3,threads=1,cores=3 \\
--numatune mode=preferred,nodeset=0 \\
--arch x86_64 \\
--hvm --cpu host \\
--features acpi=on,apic=off \\
--disk path={images_path}{vfp_img},cache=directsync,bus=ide \\
--graphics vnc,listen=0.0.0.0 \\
--noautoconsole \\
--os-variant generic \\
--network bridge={replacement_int},model=virtio \\
--network bridge={fabric_int},model=virtio \\
{network_bridge_str}'''

    return install_vm