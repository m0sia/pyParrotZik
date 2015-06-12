import sys
import re
import os

if sys.platform == "darwin":
    from binplist import binplist
elif sys.platform == "win32":
    import _winreg


def ParrotZikMac():
        p = re.compile('90:03:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}|'
                       'A0:14:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}')
        if sys.platform == "linux2":
            out = os.popen("bluez-test-device list").read()
            res = p.findall(out)
            if len(res) > 0:
                return res[0]

        elif sys.platform == "darwin":
            fd = open("/Library/Preferences/com.apple.Bluetooth.plist", "rb")
            plist = binplist.BinaryPlist(file_obj=fd)
            parsed_plist = plist.Parse()
            try:
                for mac in parsed_plist['PairedDevices']:
                    if p.match(mac.replace("-", ":")):
                        return mac.replace("-", ":")
            except Exception:
                pass

        elif sys.platform == "win32":
            aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            aKey = _winreg.OpenKey(
                aReg, 'SYSTEM\CurrentControlSet\Services\
                BTHPORT\Parameters\Devices')
            for i in range(10):
                try:
                    asubkey_name = _winreg.EnumKey(aKey, i)
                    mac = ':'.join(asubkey_name[i:i+2] for i in range(0, 12, 2))
                    res = p.findall(mac)
                    if len(res) > 0:
                        return res[0]

                except EnvironmentError:
                    pass
