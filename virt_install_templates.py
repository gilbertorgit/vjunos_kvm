"""
---------------------------------
 Author: gilbertorgit
 Date: 05/2023
---------------------------------
"""


def generate_virt_template_vsrx3(hostname, images_path, mgmt_int, int_values, vm_img, vm_config):

    install_vm = f'''virt-install \
--name {hostname} \
--accelerate \
--import \
--memory 4096 \
--vcpus=2 \
--os-variant=rhel7.0 \
--nographics \
--noautoconsole \
--disk path={images_path}{vm_img},size=16,device=disk,bus=ide,format=qcow2 \
--disk path={images_path}{vm_config},bus=ide,format=raw,target=hdc,device=cdrom \
--network bridge={mgmt_int},model=virtio \
--network bridge={int_values["int0"]},model=virtio \
--network bridge={int_values["int1"]},model=virtio \
--network bridge={int_values["int2"]},model=virtio \
--network bridge={int_values["int3"]},model=virtio \
--network bridge={int_values["int4"]},model=virtio \
--network bridge={int_values["int5"]},model=virtio \
--network bridge={int_values["int6"]},model=virtio \
--network bridge={int_values["int7"]},model=virtio \
--network bridge={int_values["int8"]},model=virtio \
--network bridge={int_values["int9"]},model=virtio \
--network bridge={int_values["int10"]},model=virtio \
--network bridge={int_values["int11"]},model=virtio'''

    return install_vm


def generate_virt_template_vex(hostname, images_path, mgmt_int, int_values, vm_img, vm_config):
    install_vm = f'''virt-install \
--name {hostname} \
--accelerate \
--vcpus 4 \
--ram 6000 \
--import \
--autostart \
--noautoconsole \
--accelerate \
--os-variant ubuntu18.04 \
--nographics \
--serial pty \
--hvm --cpu IvyBridge,require=vmx \
--sysinfo smbios,system_product=VM-VEX \
--disk path={images_path}{vm_img},cache=directsync,bus=virtio,size=10 \
--disk path={images_path}{vm_config},bus=usb,format=raw \
--network bridge={mgmt_int},model=virtio \
--network bridge={int_values["int0"]},model=virtio \
--network bridge={int_values["int1"]},model=virtio \
--network bridge={int_values["int2"]},model=virtio \
--network bridge={int_values["int3"]},model=virtio \
--network bridge={int_values["int4"]},model=virtio \
--network bridge={int_values["int5"]},model=virtio \
--network bridge={int_values["int6"]},model=virtio \
--network bridge={int_values["int7"]},model=virtio \
--network bridge={int_values["int8"]},model=virtio \
--network bridge={int_values["int9"]},model=virtio'''

    return install_vm


def generate_virt_template_apstra(hostname, images_path, mgmt_int, vm_img):
    install_vm = f'''virt-install --name={hostname} \
--accelerate \
--vcpu=8 \
--ram=32768 \
--import \
--disk={images_path}{vm_img} \
--os-variant ubuntu16.04 \
--network bridge={mgmt_int},model=virtio \
--noautoconsole'''

    return install_vm


def generate_virt_template_vevo(hostname, images_path, mgmt_int, pfe_link, rpio_link, int_values, vm_img, vm_config,
                                channelized):
    install_vm = f'''virt-install \
--name {hostname} \
--accelerate \
--vcpus 4 \
--ram 8192 \
--import \
--autostart \
--noautoconsole \
--os-variant generic \
--nographics \
--serial pty \
--cpu IvyBridge,+vmx \
--qemu-commandline="-smbios type=0,vendor=Bochs,version=Bochs -smbios type=3,manufacturer=Bochs -smbios type=1,manufacturer=Bochs,product=Bochs,serial=chassis_no=0:slot=0:type=1:assembly_id=0x0D20:platform=251:master=0:channelized={channelized}" \
--disk path={images_path}{vm_img},cache=directsync,bus=virtio,size=10 \
--disk path={images_path}{vm_config},bus=usb,format=raw \
--network bridge={mgmt_int},model=virtio \
--network bridge={pfe_link},model=virtio \
--network bridge={rpio_link},model=virtio \
--network bridge={rpio_link},model=virtio \
--network bridge={pfe_link},model=virtio \
--network bridge={int_values["int0"]},model=virtio \
--network bridge={int_values["int1"]},model=virtio \
--network bridge={int_values["int2"]},model=virtio \
--network bridge={int_values["int3"]},model=virtio \
--network bridge={int_values["int4"]},model=virtio \
--network bridge={int_values["int5"]},model=virtio \
--network bridge={int_values["int6"]},model=virtio \
--network bridge={int_values["int7"]},model=virtio \
--network bridge={int_values["int8"]},model=virtio \
--network bridge={int_values["int9"]},model=virtio \
--network bridge={int_values["int10"]},model=virtio \
--network bridge={int_values["int11"]},model=virtio'''

    return install_vm