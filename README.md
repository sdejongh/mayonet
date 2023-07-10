# mayonet
Extension of the NAPALM framework to support more Cisco IOS features.

## ExtendedIOSDriver
Extends the original NAPALM IOSDriver class and add new methods:
- get_cdp_neighbors()               : returns a a dictionary of all cdp neighbors (show cdp neighbors).
- get_interfaces_trunk()            : returns a dictionary of all working trunks (show interfaces trunk).
- get_ip_dhcp_snooping_binding()    : returns a list of DHCP leases in the DHCP snooping bindings table (show ip dhcp snooping bindings).
- get_nat_statistics()              : returns a dictionary NAT statistics (show ip nat statistics).
- get_nat_translations()            : returns a list of all active NAT translations (show ip nat translations).

