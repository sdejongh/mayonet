# mayonet
Extension of the NAPALM framework to support more Cisco IOS features.

## ExtendedIOSDriver
Extends the original NAPALM IOSDriver class and add new methods:

### get_cdp_neighbors()               
Returns a a dictionary of all cdp neighbors (show cdp neighbors).

### get_interfaces_trunk()
Returns a dictionary of all working trunks (show interfaces trunk).

### get_ip_dhcp_snooping_binding()
Returns a list of DHCP leases in the DHCP snooping bindings table (show ip dhcp snooping bindings).

### get_nat_statistics()
Returns a dictionary NAT statistics (show ip nat statistics).

### get_nat_translations()
Returns a list of all active NAT translations (show ip nat translations).

### get_ntp_associations()
Returns a list of all NTP associations (show ntp associations).

