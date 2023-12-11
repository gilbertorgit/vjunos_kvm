#!/bin/bash

usage() {
        echo "Usage :  make-vmx-config.sh <juniper-config>"
        exit 0;
}


#echo "-----------------------------------------------------"
#echo "Prepere..."
mkdir /mnt/virtioc

#echo "-----------------------------------------------------"
#echo "Creating config drive..."
mkdir config_drive
mkdir config_drive/boot
mkdir config_drive/config

#echo "-----------------------------------------------------"
#echo "Creating loader file..."
cat > config_drive/boot/loader.conf <<EOF
vm_retype="RE-VMX"
vm_instance="0"
console="vidconsole,comconsole"
vm_i2cid="0xBAA"
vm_chassis_i2cid="161"
EOF

cp -v $1 config_drive/config/

#echo "-----------------------------------------------------"
#echo "Creating vmm-config.tgz..."
cd config_drive
tar zcf vmm-config.tgz *
rm -rf boot config var
cd ..

#echo "-----------------------------------------------------"
#echo "Creating virtioc (metadata-usb-re.img)..."
# metadata-usb-re.img
# Create our own metadrive image, so we can use a junos config file
dd if=/dev/zero of=metadata-usb-re.img bs=1M count=50 >/dev/null 2>&1
mkfs.vfat metadata-usb-re.img >/dev/null
mount -o loop metadata-usb-re.img /mnt/virtioc
cp config_drive/vmm-config.tgz /mnt/virtioc
umount /mnt/virtioc
rm -R /mnt/virtioc
rm -rf config_drive