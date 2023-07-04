# Extract protocol, inside/outsside local/global addresses and ports from translation line.
IOS_NAT_TRANSLATION_REGEX = "^(?P<proto>icmp|tcp|udp)\s+(?:(?P<iga>.*):(?P<igp>\d{1,5}))\s+(?:(?P<ila>.*):(?P<ilp>\d{1,5}))\s+(?:(?P<ola>.*):(?P<olp>\d{1,5}))\s+(?:(?P<oga>.*):(?P<ogp>\d{1,5}))$"
IOS_NAT_STATISTICS_REGEX = "^Total active translations: (?P<total>\d+) \((?P<static>\d+) static, (?P<dynamic>\d+) dynamic; (?P<extended>\d+) extended\)\n" \
                             "Peak translations: (?P<peak>\d+), occurred (?P<peak_time>.*) ago\n" \
                             "Outside interfaces:\s*\n" \
                             "(?:\s\s(?P<outside_interfaces>.*)\n)?" \
                             "Inside interfaces:\s*\n" \
                             "(?:\s\s(?P<inside_interfaces>.*)\n)?" \
                             "Hits: (?P<hits>\d+)\s+Misses: (?P<misses>\d+)"

IOS_DHCP_SNOOPING_BINDING = "^(?P<mac>([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})\s+(?P<ip>([0-9]{1,3}\.){3}[0-9]{1,3})\s+(?P<lease>\d+)\s+(?P<type>[^\s]+)\s+(?P<vlan>\d+)\s+(?P<interface>.*)$"