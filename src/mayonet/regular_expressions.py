IOS_NAT_TRANSLATION_REGEX = "^(?P<proto>icmp|tcp|udp)\s+(?:(?P<iga>.*):(?P<igp>\d{1,5}))" \
                            "\s+(?:(?P<ila>.*):(?P<ilp>\d{1,5}))" \
                            "\s+(?:(?P<ola>.*):(?P<olp>\d{1,5}))\s+(?:(?P<oga>.*):(?P<ogp>\d{1,5}))$"

IOS_NAT_STATISTICS_REGEX = "^Total active translations: (?P<total>\d+) \((?P<static>\d+) static, " \
                           "(?P<dynamic>\d+) dynamic; (?P<extended>\d+) extended\)\n" \
                           "Peak translations: (?P<peak>\d+), occurred (?P<peak_time>.*) ago\n" \
                           "Outside interfaces:\s*\n" \
                           "(?:\s\s(?P<outside_interfaces>.*)\n)?" \
                           "Inside interfaces:\s*\n" \
                           "(?:\s\s(?P<inside_interfaces>.*)\n)?" \
                           "Hits: (?P<hits>\d+)\s+Misses: (?P<misses>\d+)"

IOS_DHCP_SNOOPING_BINDING_REGEX = "^(?P<mac>([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s+(?P<ip>([0-9]{1,3}\.){3}[0-9]{1,3})" \
                                  "\s+(?P<lease>\d+)\s+(?P<type>[^\s]+)\s+(?P<vlan>\d+)\s+(?P<interface>.*)$"

IOS_CDP_NEIGHBORS_REGEX = "(?P<device>[a-zA-Z0-9\-\_\.]+)\s*\n?(?P<local_interface>\w+ \d(?:/\d+)*)\s+(?P<holdtime>\d+)\s+(?P<capabilities>\w(?:\s\w)*)\s+(?P<platform>[a-zA-Z0-9\-]+)" \
                          "\s+(?P<remote_interface>\w+ \d(?:/\d+)*)\n?"

IOS_INTERFACES_TRUNK_REGEX = "Port\s+Mode\s+Encapsulation\s+Status\s+Native vlan\n((?:.*\n)*)" \
                             "\nPort\s+Vlans allowed on trunk\n((?:.*\n)*)" \
                             "\nPort\s+Vlans allowed and active in management domain\n((?:.*\n)*)" \
                             "\nPort\s+Vlans in spanning tree forwarding state and not pruned\n((?:.*\n)*)"

IOS_INTERFACES_TRUNK_STATUS_REGEX = "(?P<interface>\w+\d(?:\s?/\d+)*)\s+(?P<mode>\w+)\s+(?P<protocol>\w+(\.\w+)?)\s+" \
                                    "(?P<status>\w+)\s+(?P<native_vlan>\d+)"

IOS_INTERFACES_TRUNK_VLANS_REGEX = "(?P<interface>\w+\d(?:\s?/\d+)*)\s+(?P<vlans>none|(?:\d+(?:[,-]\d+)*))"

IOS_NTP_ASSOCIATIONS_REGEX = "disp\n((?:.*)(?:(?:\n).*))"

IOS_NTP_ASSOCIATION_INFOS_REGEX = "(?P<flags>[x#\*\+\-~\s]+)(?P<peer>[^\s]+)\s+(?P<peer_ref>[^\s]+)\s+" \
                                 "(?P<stratum>\d+)\s+(?P<when>\d+)\s+(?P<poll>\d+)\s+(?P<reach>\d+)\s+" \
                                 "(?P<delay>[0-9\.\-]+)\s+(?P<offset>[0-9\.\-]+)\s+(?P<disp>[0-9\.\-]+)"