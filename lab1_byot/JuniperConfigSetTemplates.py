"""
---------------------------------
 Author: gilbertorgit
 Date: 01/02/2023
---------------------------------
"""


def loopback_v4_v6_iso(**kwargs):

    interface = kwargs['interface']
    ipv4 = kwargs['ipv4']
    ipv6 = kwargs['ipv6']
    iso = kwargs['iso']

    data = f'''
set interfaces {interface} unit 0 family inet address {ipv4}/32
set interfaces {interface} unit 0 family iso address {iso}
set interfaces {interface} unit 0 family inet6 address {ipv6}/128
set interfaces {interface} unit 0 family mpls
    '''

    return data


def loopback_v4_v6(**kwargs):
    interface = kwargs['interface']
    ipv4 = kwargs['ipv4']
    ipv6 = kwargs['ipv6']

    data = f'''
set interfaces {interface} unit 0 family inet address {ipv4}/32
set interfaces {interface} unit 0 family inet6 address {ipv6}/128
set interfaces {interface} unit 0 family mpls
    '''

    return data


def ip_v4_v6_mpls_iso(**kwargs):
    interface = kwargs['interface']
    ipv4 = kwargs['ipv4']
    ipv6 = kwargs['ipv6']

    data = f'''
set interfaces {interface} unit 0 family inet address {ipv4}
set interfaces {interface} unit 0 family iso
set interfaces {interface} unit 0 family inet6 address {ipv6}
set interfaces {interface} unit 0 family mpls
            '''

    return data


def ip_v4_v6_mpls(**kwargs):

    interface = kwargs['interface']
    ipv4 = kwargs['ipv4']
    ipv6 = kwargs['ipv6']

    data = f'''
set interfaces {interface} unit 0 family inet address {ipv4}
set interfaces {interface} unit 0 family inet6 address {ipv6}
set interfaces {interface} unit 0 family mpls
    '''

    return data


def policy_ldb():

    data = f'''
set policy-options policy-statement ldb term 1 then load-balance per-packet
set policy-options policy-statement ldb term 1 then accept
set routing-options forwarding-table export ldb
    '''

    return data


def policy_nhs():

    data = f'''
set policy-options policy-statement nhs term 1 from protocol bgp
set policy-options policy-statement nhs term 1 from external
set policy-options policy-statement nhs term 1 then next-hop self
    '''

    return data


def routing_options_basic(**kwargs):

    ipv4 = kwargs['ipv4']

    data = f'''
set routing-options router-id {ipv4}
set routing-options autonomous-system 10459
set protocols lldp interface all
set protocols lldp-med interface all
    '''

    return data


def protocols_isis(**kwargs):

    interface = kwargs['interface']

    data = f'''
set protocols isis level 1 disable
set protocols isis level 2 authentication-key "$9$rgLKWxbs4Di.Ndi.P56/lKM8NdwYgJUj"
set protocols isis level 2 authentication-type md5
set protocols isis level 2 wide-metrics-only
set protocols isis interface lo0.0
set protocols isis interface {interface} point-to-point
set protocols isis interface {interface} ldp-synchronization
    '''

    return data


def protocols_ospf(**kwargs):
    interface = kwargs['interface']

    data = f'''
set protocols ospf3 traffic-engineering shortcuts lsp-metric-into-summary 
set protocols ospf3 realm ipv4-unicast area 0.0.0.0 interface {interface} interface-type p2p
set protocols ospf3 realm ipv4-unicast area 0.0.0.0 interface lo0.0 passive
set protocols ospf3 area 0.0.0.0 interface {interface} interface-type p2p
set protocols ospf3 area 0.0.0.0 interface lo0.0 passive
    '''

    return data


def protocols_mpls(**kwargs):

    interface = kwargs['interface']

    data = f'''
set protocols mpls ipv6-tunneling
set protocols mpls icmp-tunneling
set protocols mpls interface {interface}.0
set protocols mpls interface lo0.0
    '''

    return data


def protocols_ldp(**kwargs):

    interface = kwargs['interface']

    data = f'''
set protocols ldp track-igp-metric
set protocols ldp explicit-null
set protocols ldp interface {interface}.0
set protocols ldp interface lo0.0
    '''

    return data


def protocols_rsvp(**kwargs):

    interface = kwargs['interface']

    data = f'''
set protocols rsvp interface {interface}.0
set protocols rsvp interface {interface}.0 link-protection
set protocols rsvp interface {interface}.0 authentication-key "$9$M76L7VgoGqmTwYmTz3tpWLxNwY4aZjk."
    '''

    return data


def basic_bgp(**kwargs):

    ipv4 = kwargs['ipv4']
    ipv6 = kwargs['ipv6']

    data = f'''
set protocols bgp group ibgp log-updown
set protocols bgp group ibgp type internal
set protocols bgp group ibgp local-address {ipv4}
set protocols bgp group ibgp family inet unicast add-path receive
set protocols bgp group ibgp family inet-vpn unicast
set protocols bgp group ibgp family inet6 labeled-unicast explicit-null
set protocols bgp group ibgp family l2vpn signaling
set protocols bgp group ibgp family evpn signaling
set protocols bgp group ibgp bfd-liveness-detection minimum-interval 300
set protocols bgp group ibgp authentication-key "$9$AWCwuBElK8db2cyb24aiHtuO1cyevWx-V"
'''

    return data


def bgp_ibgp_neighbor_client(ipv4):

    ipv4 = ipv4

    data = f'''
set protocols bgp group ibgp neighbor {ipv4}
    '''

    return data


def bgp_export_nhs():

    data = f'''
set protocols bgp group ibgp export nhs
        '''

    return data


def bgp_ibgp_neighbor_rr(ipv4):
    ipv4 = ipv4

    data = f'''
set protocols bgp group ibgp neighbor {ipv4}
    '''

    return data


def bgp_ibgp_rr_cluster(cluster_id):

    cluster_id = cluster_id

    data = f'''
set protocols bgp group ibgp cluster {cluster_id}
    '''

    return data


def bgp_ebgp_neighbor_physical(ipv4):

    ipv4 = ipv4
    #ipv6 = ipv6

    a, b, c, d = ipv4.split('.')

    if (int(d) % 2) == 0:
        temp = int(d) + 1
    else:
        temp = int(d) - 1

    data = f'''
set protocols bgp group ibgp neighbor {a}.{b}.{c}.{temp}
    '''

    return data.strip()
