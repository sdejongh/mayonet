import re
from napalm.ios.ios import IOSDriver
from mayonet.regular_expressions import IOS_NAT_TRANSLATION_REGEX


class ExtendedIOSDriver(IOSDriver):
    """Custom extension of NAPALM Cisco IOS Handler"""

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
