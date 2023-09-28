"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""

from subprocess import call, Popen, DEVNULL


class DevicesConfig:

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

