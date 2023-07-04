# Extract protocol, inside/outsside local/global addresses and ports from translation line.
IOS_NAT_TRANSLATION_REGEX = "^(?P<proto>icmp|tcp|udp)\s+(?:(?P<iga>.*):(?P<igp>\d{1,5}))\s+(?:(?P<ila>.*):(?P<ilp>\d{1,5}))\s+(?:(?P<ola>.*):(?P<olp>\d{1,5}))\s+(?:(?P<oga>.*):(?P<ogp>\d{1,5}))$"
IOS_NAT_STATISTICS_REGEX = "^Total active translations: (?P<total>\d+) \((?P<static>\d+) static, (?P<dynamic>\d+) dynamic; (?P<extended>\d+) extended\)\n" \
                             "Peak translations: (?P<peak>\d+), occurred (?P<peak_time>.*) ago\n" \
                             "Outside interfaces:\s*\n" \
                             "(?:\s\s(?P<outside_interfaces>.*)\n)?" \
                             "Inside interfaces:\s*\n" \
                             "(?:\s\s(?P<inside_interfaces>.*)\n)?" \
                             "Hits: (?P<hits>\d+)\s+Misses: (?P<misses>\d+)"