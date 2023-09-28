"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""

import sys
#sys.path.append('/')
from ipaddress import ip_network
import re
#from lab4_super_core.main import MainScript
from generateData import GenerateData
from pprint import pprint


class GenerateIpAddr:

    def __init__(self, number_int, count, p2p_ipv4 ='10.0.0.0/23', loopback_ipv4 ='10.10.10.0/24',
                 p2p_ipv6 ='2000:2000:0::0/120', loopback_ipv6 ='2000:2000:10::0/120'):

        self.p2p_ipv4 = ip_network(p2p_ipv4)
        self.loopback_ipv4 = ip_network(loopback_ipv4)
        self.p2p_ipv6 = ip_network(p2p_ipv6)
        self.loopback_ipv6 = ip_network(loopback_ipv6)
        self.p2p_ipv4_dict = {}
        self.p2p_ipv6_dict = {}
        self.loopback_ipv4_dict = {}
        self.loopback_ipv6_dict = {}
        self.stop = number_int
        self.core_p2p_ip_dict = {}
        self.core_loopback_ip_dict = {}
        self.iso_address = ''
        self.all_data_dict = {}
        self.count = count

    @staticmethod
    def pairwise(iterable):

        a_iterable = iter(iterable)
        return zip(a_iterable, a_iterable)

    def create_ipv4_p2p(self):

        """
        Create IPv4 P2P
        """
        ip_list = []
        count = 1
        for i in self.p2p_ipv4:
            if count <= self.stop * 2:
                ip_list.append(str(i))
            count += 1

        count2 = self.count
        for x, y in self.pairwise(ip_list):
            index = (f'S-{count2}')
            self.p2p_ipv4_dict[index] = (x, y)
            count2 += 1
        return self.p2p_ipv4_dict

    def create_ipv6_p2p(self):

        """
        Create IPv6 P2P
        """
        ipv6_list = []
        count = 1
        for i in self.p2p_ipv6:
            if count <= self.stop * 2:
                ipv6_list.append(str(i))
            count += 1

        count2 = self.count
        for x, y in self.pairwise(ipv6_list):
            index = (f'S-{count2}')
            self.p2p_ipv6_dict[index] = (x, y)
            count2 += 1
        return self.p2p_ipv6_dict

    def create_ipv4_loopback(self):

        """
        Create IPv4 Loopbcak P2P
        """

        ip_list = []
        count = 1
        for i in self.loopback_ipv4:
            if count == 1:
                count += 1
                continue
            elif count <= self.stop:
                ip_list.append(str(i))
            count += 1

        count2 = 1
        for x in ip_list:
            index = (f'{count2}')
            self.loopback_ipv4_dict[index] = (x)
            count2 += 1

        return self.loopback_ipv4_dict

    def create_ipv6_loopback(self):

        """
        Create IPv6 Loopbcak P2P
        """

        ipv6_list = []
        count = 1
        for i in self.loopback_ipv6:
            if count == 1:
                count += 1
                continue
            elif count <= self.stop:
                ipv6_list.append(str(i))
            count += 1

        count2 = 1
        for x in ipv6_list:
            index = (f'{count2}')
            self.loopback_ipv6_dict[index] = (x)
            count2 += 1

        return self.loopback_ipv6_dict

    def create_iso_address(self, ip):

        """
        Create ISO Address
        """
        ip = ip
        padded_octets = [f'{x:>03}' for x in ip.split('.')]
        joined_octets = ''.join(padded_octets)
        re_split = '.'.join(re.findall('....', joined_octets))
        result = '.'.join(['49.0000', re_split, '00'])
        return result

    @staticmethod
    def merge_dictionary(ipv4_dict, ipv6_dict):

        """
        Merge Dicts
        """
        merge_dict = {**ipv4_dict, **ipv6_dict}
        for key, value in merge_dict.items():
            if key in ipv4_dict and key in ipv6_dict:
                merge_dict[key] = [value, ipv4_dict[key]]
        return merge_dict

    def create_p2p_dict(self, data1: dict):

        """
        Create P2P Dict
        """

        merge_dict = self.merge_dictionary(self.p2p_ipv4_dict, self.p2p_ipv6_dict)

        db = data1

        count = 0
        hostname = ''
        mgmt_ip = ''
        for key, value in merge_dict.items():
            for key1, value1 in db.items():
                for i in value1['data']:
                    if i['type'].upper() == 'VROUTER':
                        hostname = i['hostname']
                        mgmt_ip = i['mgmt_ip']

                    if i['type'].upper() == 'VSRX3':
                        hostname = i['hostname']
                        mgmt_ip = i['mgmt_ip']

                    if i['type'].upper() == 'VEX':
                        hostname = i['hostname']
                        mgmt_ip = i['mgmt_ip']

                    if i['type'].upper() == 'VEVO':
                        hostname = i['hostname']
                        mgmt_ip = i['mgmt_ip']

                    for k, v in i.items():
                        if str(key) == str(v):
                            """
                            - if equal and count == 0, it will get the fist IP from p2p_ipv4_dict per index:
                            S-1 (10.0.0.0, 10.0.0.1 ) -> 10.0.0.0
                            - then, update the dictionary and count +1 - So, in the next one it will go to the 
                            else statement 
                            - in the else it will get the second IP: 10.0.0.1
                            - update the dictionary
                            - reset the count to 0
                            """
                            if count == 0:
                                self.core_p2p_ip_dict[value[1][count]] = {
                                    'hostname': hostname,
                                    'mgmt_ip': mgmt_ip,
                                    'interface': k,
                                    'ipv4': f'{value[1][count]}/31',
                                    'ipv6': f'{value[0][count]}/127'
                                }
                                count += 1
                            else:
                                self.core_p2p_ip_dict[value[1][count]] = {
                                    'hostname': hostname,
                                    'mgmt_ip': mgmt_ip,
                                    'interface': k,
                                    'ipv4': f'{value[1][count]}/31',
                                    'ipv6': f'{value[0][count]}/127'
                                }
                                count = 0
        return self.core_p2p_ip_dict

    def create_loopback_dict(self, data1: dict):

        """
        Create loopback Dict
        """

        merge_dict = self.merge_dictionary(self.loopback_ipv4_dict, self.loopback_ipv6_dict)

        db = data1

        count = 1
        for key, value in db.items():
            for i in value['data']:
                if i['type'].upper() != 'VROUTER':
                    hostname = i['hostname']
                    mgmt_ip = i['mgmt_ip']
                    role = i['role']

                    iso_address = self.create_iso_address(merge_dict[f'{count}'][1])
                    self.core_loopback_ip_dict[hostname] = {
                        'hostname': hostname,
                        'role': role,
                        'mgmt_ip': mgmt_ip,
                        'loopback_int': {'lo0':
                            {
                            'loopback_ipv4': merge_dict[f'{count}'][1],
                            'loopback_ipv6': merge_dict[f'{count}'][0],
                            'loopback_iso': iso_address
                            }
                        },
                        'physical_int': {}
                    }
                    #self.core_loopback_ip_dict[hostname]['interfaces'] = {}
                    count += 1

        return self.core_loopback_ip_dict

    def merged_p2p_loopback_data(self):

        """
        Create P2P and Loopback Dict - Consolidate both with right info
        """

        self.all_data_dict = self.core_loopback_ip_dict

        for k, v in self.all_data_dict.items():

            for k1, v1 in self.core_p2p_ip_dict.items():
                if str(k) == str(v1['hostname']):
                    self.all_data_dict[v1['hostname']]['physical_int'][v1['interface']] = {
                        'ipv4': v1['ipv4'],
                        'ipv6': v1['ipv6']
                    }
        return self.all_data_dict
