import re
from napalm.ios.ios import IOSDriver
from mayonet.regular_expressions import IOS_NAT_TRANSLATION_REGEX, IOS_NAT_STATISTICS_REGEX, IOS_DHCP_SNOOPING_BINDING


class ExtendedIOSDriver(IOSDriver):
    """Custom extension of NAPALM Cisco IOS Handler"""

    def get_nat_statistics(self):
        """
        Returns a dictionary of the 'show ip nat statistics' commands output.
        Example:
        {
            'translations': {
                'total': 1645,
                'static': 13,
                'dynamic': 1632,
                'extended': 1640,
                'peak': 4810,
                'hits': 434766136,
                'misses': 0
            },
            'interfaces': {
                'inside': ['GigabitEthernet0/0', 'GigabitEthernet0/1'],
                'outside': ['GigabitEthernet0/2', 'FastEthernet0/0/1']
            }
        }

        """
        command = "show ip nat statistics"
        output = self._send_command(command)
        result = re.search(IOS_NAT_STATISTICS_REGEX, output)
        result_dict = result.groupdict()
        statistics = {
            "translations": {
                "total": int(result_dict["total"]),
                "static": int(result_dict["static"]),
                "dynamic": int(result_dict["dynamic"]),
                "extended": int(result_dict["extended"]),
                "peak": int(result_dict["peak"]),
                "hits": int(result_dict["hits"]),
                "misses": int(result_dict["misses"]),
            },
            "interfaces": {
                "inside": result_dict["inside_interfaces"].replace(" ", "").split(","),
                "outside": result_dict["outside_interfaces"].replace(" ", "").split(","),
            }

        }
        return statistics

    def get_nat_translations(self) -> list[dict]:
        """
        Returns a list of dictionaries. Each dictionary represents an entry for the NAT translations table with the
        following keys:
            proto:  Protocol
            iga:    Inside Global Address
            igp:    Inside Global Port
            ila:    Inside Local Address
            ilp:    Inside Local Port
            ola:    Outside Local Address
            olp:    Outside Local Port
            oga:    Outside Global Address
            ogp:    Outside Global Port

        Note: doesn't support VRFs yet.
        """
        translations = []
        command = "show ip nat translations"
        output = self._send_command(command)
        for line in output.split("\n"):
            result = re.search(IOS_NAT_TRANSLATION_REGEX, line)
            if result is not None:
                translations.append(result.groupdict())
        return translations

    def get_ip_dhcp_snooping_bindings(self):
        """
        Returns a list of dictionaries. Each dictionary represents an entry for the DHCP Snooping Binding table with the
        following keys:
            mac:        MAC address
            ip:         IP address
            lease:      Lease time (sec)
            type:       Source of the binding
            vlan:       Vlan id
            interface:  Interface to which the lease is bond
        """
        bindings = []
        command = "show ip dhcp snooping binding"
        output = self._send_command(command)
        for line in output.split("\n"):
            result = re.search(IOS_DHCP_SNOOPING_BINDING, line)
            if result is not None:
                binding = result.groupdict()
                binding["lease"] = int(binding["lease"])
                binding["vlan"] = int(binding["vlan"])
                bindings.append(binding)
        return bindings
