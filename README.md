# mayonet
Extension of the NAPALM framework to support more Cisco IOS features.

## ExtendedIOSDriver
Extends the original NAPALM IOSDriver class and add new methods:
- get_nat_translations()            : returns a list of all active NAT translations.
- get_nat_statistics()              : returns a dictionary of counters and interfaces shown in 'show ip nat statistics'.
- get_ip_dhcp_snooping_binding()    : returns a list of DHCP leases in the DHCP snooping bindings table.

