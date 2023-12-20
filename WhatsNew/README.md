# What is new - vJunos KVM

**December 2023**
- New roles support
  - 'CORE'
    - When configure 'CORE' + 'S-Xs' interfaces you can use options 7 and 8 for interface configuration
  - 'CORE,LER' -> **LER**=Label Edge Router
    - When configuring 'CORE,LER' + 'S-Xs' interfaces 
      - you can use options 5-8 for additional configuration 
      - it will create BGP Peering
        - full-mesh IBGP when no 'CORE,REFLECTOR' is configured
        - IBGP with Router Reflector when 'CORE,REFLECTOR' is configured
  - 'CORE,REFLECTOR'
    - you can use options 5-8 for additional configuration
    - This device will be a router reflector and have peering with 'CORE,LER' devices
  - DC - no additional config is provided
  - VR - no additional config is provided
*Check examples folder for further info* -> https://github.com/gilbertorgit/vjunos_kvm/tree/main/lab1_byot/examples

- Juniper vMX support

**November 2023**
- Juniper vjunos-router support

**October 2023**
- Juniper vjunos-evolved support

