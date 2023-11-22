"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""

from consoleTemplate import ConsoleConfig
from subprocess import call, Popen, DEVNULL
import pexpect


class DevicesConfig:

    def vmx_console_cfg(self, data):

        print("########## Basic vMX MGMT Configuration - hostname and ip")

        db = data
        console = ConsoleConfig()

        for key, value in db.items():
            for i in value['data']:
                if i['type'] == 'vmx-vcp':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']

                    try:
                        console.vmx_config(hostname, mgmt_ip)
                    except pexpect.exceptions.TIMEOUT:
                        print(f'Unable to configure: {hostname} with {mgmt_ip}! Please, configure it manually!!\n')
                    except pexpect.exceptions.EOF:
                        print(f'Unable to configure: {hostname} with {mgmt_ip}! Please, configure it manually!!\n')

    @staticmethod
    def ping_device(hostname, mgmt_ip):
        pass

        response = call(['ping', '-c', '1', mgmt_ip], stdout=DEVNULL)

        if response == 0:
             print(f'{hostname} - MGMT Network: {mgmt_ip} is reachable\n')
        else:
            print(f'{hostname} - MGMT Network: {mgmt_ip} is unreachable\n')

    def check_ping(self, data):

        db = data

        for key, value in db.items():
            for i in value['data']:
                if i['type'] != 'vmx-vfp':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']

                    DevicesConfig.ping_device(hostname, mgmt_ip)

