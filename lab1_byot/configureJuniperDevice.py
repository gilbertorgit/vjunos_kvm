"""
---------------------------------
 Author: gilbertorgit
 Date: 01/02/2023
---------------------------------
"""
import sys

from jnpr.junos.exception import ConnectTimeoutError

sys.path.append('../')
# from main import MainScript
from generateData import GenerateData
from generateIP import GenerateIpAddr
from JuniperConfigSetTemplates import *
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import pprint

#import logging
#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')

lab_user = 'lab'
lab_password = 'lab123'


class ConfigureJuniperDevice:

    def __init__(self, number_int, count):
        self.p2p_data = {}
        self.loopback_data = {}
        self.p2p_loopback_data = {}
        self.number_int = number_int
        self.count = count

    def get_data(self):

        device_tab_list = ('SRX', 'VROUTER', 'VEX', 'VEVO')
        vlab1_data = GenerateData()
        tab_list = device_tab_list
        vlab1_data.generate_data_info('../lab1_byot/lab1_device_info.xlsx', *tab_list)
        devices_dict = vlab1_data.get_merged_data

        b = GenerateIpAddr(self.number_int, self.count)
        b.create_ipv4_p2p()
        b.create_ipv6_p2p()

        b.create_ipv4_loopback()
        b.create_ipv6_loopback()

        self.p2p_data = b.create_p2p_dict(devices_dict)
        #pprint.pprint(self.p2p_data)
        self.loopback_data = b.create_loopback_dict(devices_dict)

        self.p2p_loopback_data = b.merged_p2p_loopback_data()

        # pprint.pprint(self.p2p_loopback_data)

    def device_request(self, data: str, host, port=22, user='lab', password='lab123'):

        try:
            with Device(host=host, port=int(port), user=user, password=password) as dev:
                with Config(dev, mode='exclusive') as cu:
                    cu.load(data, format='set', merge=True)
                    cu.commit()
        except (ConnectionError, ConnectTimeoutError) as err:
            print(f'-- Cannot connect to device: {err}')

    def configure_physical_interface(self):

        print("#" * 50, "P2P Config")

        db = self.p2p_loopback_data

        data = ''
        interface = ''
        list_int = ''
        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                for k1, v1 in v['physical_int'].items():
                    interface = k1
                    p2p_addr_v4 = v1['ipv4']
                    p2p_addr_v6 = v1['ipv6']

                    data_dict = {
                        'interface': interface,
                        'ipv4': p2p_addr_v4,
                        'ipv6': p2p_addr_v6
                    }
                    data += ip_v4_v6_mpls(**data_dict)
                    list_int += f'\n- {interface}: \t{p2p_addr_v4}, \t{p2p_addr_v6}'
                print(f'-------Configuring {hostname}/({mgmt_ip}) P2P IP -> Interface:{list_int}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')
                data = ''
                list_int = ''

    def configure_physical_interface_iso(self):

        print("#" * 50, "P2P Config")

        db = self.p2p_loopback_data

        data = ''
        interface = ''
        list_int = ''
        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                for k1, v1 in v['physical_int'].items():
                    interface = k1
                    p2p_addr_v4 = v1['ipv4']
                    p2p_addr_v6 = v1['ipv6']

                    data_dict = {
                        'interface': interface,
                        'ipv4': p2p_addr_v4,
                        'ipv6': p2p_addr_v6
                    }
                    data += ip_v4_v6_mpls_iso(**data_dict)
                    list_int += f'\n- {interface}: \t{p2p_addr_v4}, \t{p2p_addr_v6}'
                print(f'-------Configuring {hostname}/({mgmt_ip}) P2P IP -> Interface:{list_int}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')
                data = ''
                list_int = ''

    def configure_loopback_interface_iso(self):

        print("#" * 50, "Loopback Config")

        db = self.loopback_data

        data = ''
        interface = ''
        ipv4 = ''
        ipv6 = ''
        iso = ''
        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                for k1, v1 in v['loopback_int'].items():
                    interface = k1
                    ipv4 = v1['loopback_ipv4']
                    ipv6 = v1['loopback_ipv6']
                    iso = v1['loopback_iso']

                    data_dict = {
                    'interface': interface,
                    'ipv4': ipv4,
                    'ipv6': ipv6,
                    'iso': iso
                    }

                    data += loopback_v4_v6_iso(**data_dict)
                print(f'-------Configuring {hostname}/({mgmt_ip}) Loopback IP -> Interface:\n- {interface}: '
                      f'{ipv4}, \t{ipv6}, \t{iso}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')

                data = ''

    def configure_loopback_interface(self):

        print("#" * 50, "Loopback Config")

        db = self.loopback_data

        data = ''
        interface = ''
        ipv4 = ''
        ipv6 = ''
        iso = ''
        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                for k1, v1 in v['loopback_int'].items():
                    interface = k1
                    ipv4 = v1['loopback_ipv4']
                    ipv6 = v1['loopback_ipv6']

                    data_dict = {
                    'interface': interface,
                    'ipv4': ipv4,
                    'ipv6': ipv6
                    }

                    data += loopback_v4_v6(**data_dict)
                print(f'-------Configuring {hostname}/({mgmt_ip}) Loopback IP -> Interface:\n- {interface}: '
                      f'{ipv4}, \t{ipv6}, \t{iso}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')

                data = ''

    def configure_policies(self):

        print("#" * 50, "LDB, NHS Policies Config")

        db = self.loopback_data

        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                ipv4 = ''
                for k1, v1 in v['loopback_int'].items():
                    if str(k1) == 'lo0':
                        ipv4 = v1['loopback_ipv4']

                data_dict = {
                    'ipv4': ipv4,
                }

                data1 = policy_ldb()
                data2 = policy_nhs()
                data3 = routing_options_basic(**data_dict)

                data = data1 + data2 + data3

                print(f'-------Configuring {hostname}/({mgmt_ip}) Basic Policies -> LDB/NHS')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')

    def configure_protocols_iso(self):

        print("#" * 50, "ISIS, MPLS, LDP, RSVP Config")

        db = self.loopback_data
        data = ''
        list_int = ''
        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                interface = ''
                for k1, v1 in v['physical_int'].items():
                    interface = k1

                    data_dict = {
                        'interface': interface,
                    }

                    data1 = protocols_isis(**data_dict)
                    data2 = protocols_mpls(**data_dict)
                    data3 = protocols_ldp(**data_dict)
                    data4 = protocols_rsvp(**data_dict)

                    data += data1 + data2 + data3 + data4
                    list_int += f'{interface} '
                print(f'-------Configuring {hostname}/({mgmt_ip}) Basic Protocols -> Interface: {list_int}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')
                data = ''
                list_int = ''

    def configure_protocols(self):

        print("#" * 50, "OSPF, MPLS, LDP, RSVP Config")

        db = self.loopback_data
        data = ''
        list_int = ''
        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                interface = ''
                for k1, v1 in v['physical_int'].items():
                    interface = k1

                    data_dict = {
                        'interface': interface,
                    }

                    data1 = protocols_ospf(**data_dict)
                    data2 = protocols_mpls(**data_dict)
                    data3 = protocols_ldp(**data_dict)
                    data4 = protocols_rsvp(**data_dict)

                    data += data1 + data2 + data3 + data4
                    list_int += f'{interface} '
                print(f'-------Configuring {hostname}/({mgmt_ip}) Basic Protocols -> Interface: {list_int}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')
                data = ''
                list_int = ''

    def configure_basic_bgp(self):

        print("#" * 50, "BGP basic Config")

        db = self.loopback_data

        for k, v in db.items():
            if 'CORE' in v['role'].upper():
                hostname = v['hostname']
                mgmt_ip = v['mgmt_ip']
                ipv4 = v['loopback_int']['lo0']['loopback_ipv4']
                ipv6 = v['loopback_int']['lo0']['loopback_ipv6']

                data_dict = {
                    'ipv4': ipv4,
                    'ipv6': ipv6,
                }

                data = basic_bgp(**data_dict)
                print(f'-------Configuring {hostname}/({mgmt_ip}) Basic BGP -> group ibgp')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')

    def configure_bgp_ibgp_neighbor_client_to_rr(self):

        print("#" * 50, "BGP Client Neighbor Config")

        db = self.loopback_data

        def check_reflector():
            for k1, v1 in db.items():
                if 'REFLECTOR' in v1['role'].upper():
                    return True

        if check_reflector():
            data = ''
            router_reflector_ip = ''
            for k1, v1 in db.items():
                if 'REFLECTOR' in v1['role'].upper():
                    router_reflector_ip = v1['loopback_int']['lo0']['loopback_ipv4']

                    for k, v in db.items():
                        if 'CORE' in v['role'].upper():
                            if 'REFLECTOR' not in v['role'].upper():

                                hostname = v['hostname']
                                mgmt_ip = v['mgmt_ip']

                                data1 = bgp_export_nhs()
                                data2 = bgp_ibgp_neighbor_client(router_reflector_ip)

                                data += data1 + data2

                                print(f'-------Configuring {hostname}/({mgmt_ip}) with Router Reflector -> Neighbor: {router_reflector_ip} ')
                                # print(data)
                                self.device_request(data, mgmt_ip, user='lab', password='lab123')
                                data = ''
        else:
            for k1, v1 in db.items():
                data = ''
                data2 = ''
                ip_list = ''
                if 'CORE' in v1['role'].upper():
                    hostname = v1['hostname']
                    mgmt_ip = v1['mgmt_ip']
                    ipv4 = v1['loopback_int']['lo0']['loopback_ipv4']
                    for k, v in db.items():
                        if 'CORE' in v['role'].upper():
                            ipv4_neighbor = v['loopback_int']['lo0']['loopback_ipv4']
                            if ipv4 != ipv4_neighbor:
                                data2 += bgp_ibgp_neighbor_client(ipv4_neighbor)
                                ip_list += f'{ipv4_neighbor} '

                    data1 = bgp_export_nhs()
                    data += data1 + data2

                    print(f'-------Configuring {hostname}/({mgmt_ip}) -> {ipv4} with neighbor: {ip_list}')
                    # print(data)
                    self.device_request(data, mgmt_ip, user='lab', password='lab123')

    def configure_bgp_ibgp_neighbor_rr_to_client(self):

        print("#" * 50, "BGP Router Reflector Neighbor Config")

        db = self.loopback_data

        mgmt_ip = ''
        hostname = ''

        data = ''
        ip_list = ''
        router_reflector_ip = ''
        for k1, v1 in db.items():
            if 'REFLECTOR' in v1['role'].upper():
                hostname = v1['hostname']
                mgmt_ip = v1['mgmt_ip']
                router_reflector_ip = v1['loopback_int']['lo0']['loopback_ipv4']

                data += bgp_ibgp_rr_cluster(router_reflector_ip)

                for k, v in db.items():
                    if 'CORE' in v['role'].upper():
                        if 'REFLECTOR' not in v['role'].upper():
                            ipv4 = v['loopback_int']['lo0']['loopback_ipv4']

                            data += bgp_ibgp_neighbor_rr(ipv4)
                            ip_list += f'{ipv4} '
                print(f'-------Configuring {hostname}/({mgmt_ip}) -> Neighbor: {ip_list}')
                # print(data)
                self.device_request(data, mgmt_ip, user='lab', password='lab123')
                data = ''
                ip_list = ''


if __name__ == "__main__":
    pass

    # dev = ConfigureJuniperDevice(50, 1)
    # dev.get_data()
    # dev.configure_loopback_interface()
    # dev.configure_physical_interface()
    # dev.configure_policies()
    # dev.configure_protocols()
    # dev.configure_basic_bgp()
    # dev.configure_bgp_ibgp_neighbor_client_to_rr()
    # dev.configure_bgp_ibgp_neighbor_rr_to_client()

