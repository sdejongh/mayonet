import re
from napalm.ios.ios import IOSDriver
from mayonet.regular_expressions import IOS_NAT_TRANSLATION_REGEX, \
    IOS_NAT_STATISTICS_REGEX, \
    IOS_DHCP_SNOOPING_BINDING_REGEX, \
    IOS_CDP_NEIGHBORS_REGEX, \
    IOS_INTERFACES_TRUNK_REGEX, \
    IOS_INTERFACES_TRUNK_STATUS_REGEX, \
    IOS_INTERFACES_TRUNK_VLANS_REGEX


def parse_trunk_vlans(vlan_string: str) -> list[int] or None:
    """
    F!unction that takes a string of vlans and return a list of all included vlans.
    Example:
        parse_trunk_vlans('1-10,300,301') returns [1,2,3,4,5,6,7,8,9,10,300,301]
    """
    if vlan_string == "none":
        return None
    vlans = []
    for part in vlan_string.split(","):
        if "-" in part:
            first, last = part.split("-")
            vlans.extend(range(int(first), int(last) + 1))
        else:
            vlans.append(int(part))
    return vlans


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
            result = re.search(IOS_DHCP_SNOOPING_BINDING_REGEX, line)
            if result is not None:
                binding = result.groupdict()
                binding["lease"] = int(binding["lease"])
                binding["vlan"] = int(binding["vlan"])
                bindings.append(binding)
        return bindings

    def get_cdp_neighbors(self):
        """
        Returns a dictionary with the neighbor device name as key and a dictionary as value.
        Each dictionary represents a CDP neighbor entry and has the following keys:
            local_interface:    The local interface linked to the neighbor
            holdtime:           Time remaining before the CDP information expires
            capabilities:       A list of letters representing the device capabilities
            platform:           The IOS platform of the cdp neighbor
            remote_interface:   The interface on the neighbor side.
        """
        command = "show cdp neighbors"
        output = self._send_command(command)
        result = re.findall(IOS_CDP_NEIGHBORS_REGEX, output)
        neighbors = {}
        for neighbor in result:
            device_name = neighbor[0]
            device_dict = {
                "local_interface": neighbor[1],
                "holdtime": int(neighbor[2]),
                "capabilities": [capability for capability in neighbor[3].split(" ")],
                "platform": neighbor[4],
                "remote_interface": neighbor[5],
            }
            neighbors[device_name] = device_dict
        return neighbors

    def get_interfaces_trunk(self):
        """
        Returns a dictionary of trunks with the interface name as key and a dictionary of information as value
        with the following keys:
            mode:               the trunk port mode (on, auto, ...)
            protocol:           the trunking protocol used
            status:             the actual status of the trunk
            native_vlan:        the native vlan on the trunk (integer)
            allowed_vlans:      a list of all allowed vlans on the trunk (integers)
            active_vlans:       a list of all allowed and active vlans on the trunk (integers)
            forwarding_vlans:   a list of all allowed, active, in STP forwarding state and not pruned vlans on the trunk (integers)
        """
        trunks = {}
        command = "show interfaces trunk"

        # Adding missing \n at the end of the output
        output = self._send_command(command) + "\n"

        result = re.search(IOS_INTERFACES_TRUNK_REGEX, output)

        if result is None:
            return trunks

        trunks_status = result.groups()[0]
        trunks_allowed_vlans = result.groups()[1]
        trunks_active_vlans = result.groups()[2]
        trunks_forwarding_vlans = result.groups()[3]

        for line in trunks_status.split("\n"):
            if len(line) == 0:
                continue
            trunk_dict = re.search(IOS_INTERFACES_TRUNK_STATUS_REGEX, line).groupdict()
            trunks[trunk_dict["interface"]] = {
                "mode": trunk_dict["status"],
                "protocol": trunk_dict["protocol"],
                "status": trunk_dict["status"],
                "native_vlan": int(trunk_dict["native_vlan"])
            }

        for line in trunks_allowed_vlans.split("\n"):
            if len(line) == 0:
                continue
            trunk_dict = re.search(IOS_INTERFACES_TRUNK_VLANS_REGEX, line).groupdict()
            trunks[trunk_dict["interface"]]["allowed_vlans"] = parse_trunk_vlans(trunk_dict["vlans"])

        for line in trunks_active_vlans.split("\n"):
            if len(line) == 0:
                continue
            trunk_dict = re.search(IOS_INTERFACES_TRUNK_VLANS_REGEX, line).groupdict()
            trunks[trunk_dict["interface"]]["active_vlans"] = parse_trunk_vlans(trunk_dict["vlans"])

        for line in trunks_forwarding_vlans.split("\n"):
            if len(line) == 0:
                continue
            trunk_dict = re.search(IOS_INTERFACES_TRUNK_VLANS_REGEX, line).groupdict()
            trunks[trunk_dict["interface"]]["forwarding_vlans"] = parse_trunk_vlans(trunk_dict["vlans"])

        return trunks
