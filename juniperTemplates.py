"""
---------------------------------
 Author: gilbertorgit
 Date: 01/02/2023
---------------------------------
"""


class BasicConfigTemplateJuniper:

    def vjunos_evolved(self, hostname: str, mgmt_ip: str):

        data = f'''system {{
    host-name {hostname};
    root-authentication {{
        encrypted-password "$1$aic0re1C$iga3zkJvFaG7rP7tDP/P91";
    }}
    login {{
        user lab {{
            uid 2000;
            class super-user;
            authentication {{
                encrypted-password "$1$aic0re1C$i719d/4ZQchOhadfrUQxR.";
            }}
        }}
    }}
    syslog {{
        file interactive-commands {{
            interactive-commands any;
        }}
        file messages {{
            any notice;
            authorization info;
        }}
    }}
    services {{
        ssh {{
            root-login allow;
        }}
        netconf {{
            ssh;
        }}
    }}
    processes {{
        nlsd enable;
    }}
}}
interfaces {{
    re0:mgmt-0 {{
        unit 0 {{
            family inet {{
                address {mgmt_ip}/24;
            }}
        }}
    }}
}}
protocols {{
    lldp {{
        port-id-subtype interface-name;
        interface all;
    }}
}}

'''
        return data

    def vjunos_switch(self, hostname: str, mgmt_ip: str):

        data = f'''system {{
    host-name {hostname};
    root-authentication {{
        encrypted-password "$1$aic0re1C$iga3zkJvFaG7rP7tDP/P91";
    }}
    commit synchronize;
    login {{
        user lab {{
            uid 2000;
            class super-user;
            authentication {{
                encrypted-password "$1$aic0re1C$i719d/4ZQchOhadfrUQxR.";
            }}
        }}
    }}
    syslog {{
        file interactive-commands {{
            interactive-commands any;
        }}
        file messages {{
            any notice;
            authorization info;
        }}
    }}
    services {{
        ssh {{
            root-login allow;
        }}
        netconf {{
            ssh;
        }}
    }}
    processes {{
        nlsd enable;
    }}
}}
interfaces {{
    fxp0 {{
        unit 0 {{
            family inet {{
                address {mgmt_ip}/24;
            }}
        }}
    }}
}}
multi-chassis {{
    mc-lag {{
        consistency-check;
    }}
}}
protocols {{
    lldp {{
        port-id-subtype interface-name;
        interface all;
    }}
}}

'''
        return data

    def vjunos_vsrx3(self, hostname: str, mgmt_ip: str):
        data = f'''system {{
    host-name {hostname};
    root-authentication {{
        encrypted-password "$6$4Gsx3XMx$yDylMLxrZlMPJvstpp.K/wZGOEB550PrCDX4dlihNNv52KzZ0QFKkXn8BtiJGaBvdoQUmL1oWiZQ843v3tFsV1";
    }}
    login {{
        user lab {{
            class super-user;
            authentication {{
                encrypted-password "$6$47kU3MQ8$8OTll3oZNDyQhhHB1rhkCmBGZCY3oLcRq9GHnvZoimvmZ/trHBvEoq9rAvhj3qzBoDGXE/BCNDI4FdzbwxcPu/";
            }}
        }}
    }}
    services {{
        ssh {{
            root-login allow;
        }}
        netconf {{
            ssh;
        }}
        web-management {{
            http {{
                interface fxp0.0;
            }}
            https {{
                system-generated-certificate;
                interface fxp0.0;
            }}
        }}
    }}
    syslog {{
        file interactive-commands {{
            interactive-commands any;
        }}
        file messages {{
            any any;
            authorization info;
        }}
    }}
    license {{
        autoupdate {{
            url https://ae1.juniper.net/junos/key_retrieval;
        }}
    }}
}}
security {{
    forwarding-options {{
        family {{
            inet6 {{
                mode packet-based;
            }}
            mpls {{
                mode packet-based;
            }}
            iso {{
                mode packet-based;
            }}
        }}
    }}
}}
interfaces {{
    fxp0 {{
        unit 0 {{
            family inet {{
                address {mgmt_ip}/24;
            }}
        }}
    }}
}}

'''
        return data

    def vjunos_router(self, hostname: str, mgmt_ip: str):

        data = f'''system {{
    host-name {hostname};
    root-authentication {{
        encrypted-password "$1$aic0re1C$iga3zkJvFaG7rP7tDP/P91";
    }}
    commit synchronize;
    login {{
        user lab {{
            uid 2000;
            class super-user;
            authentication {{
                encrypted-password "$1$aic0re1C$i719d/4ZQchOhadfrUQxR.";
            }}
        }}
    }}
    syslog {{
        file interactive-commands {{
            interactive-commands any;
        }}
        file messages {{
            any notice;
            authorization info;
        }}
    }}
    services {{
        ssh {{
            root-login allow;
        }}
        netconf {{
            ssh;
        }}
    }}
    processes {{
        nlsd enable;
    }}
}}
chassis {{
    fpc 0 {{
        pic 0 {{
            number-of-ports 20;
        }}
    }}
}}
interfaces {{
    fxp0 {{
        unit 0 {{
            family inet {{
                address {mgmt_ip}/24;
            }}
        }}
    }}
}}

'''
        return data
