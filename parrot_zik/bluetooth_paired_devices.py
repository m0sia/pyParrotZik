import sys
import re
import os

from parrot_zik.resource_manager import GenericResourceManager

if sys.platform == "darwin":
    from binplist import binplist
    import lightblue
else:
    import bluetooth
    if sys.platform == "win32":
        import _winreg


def get_parrot_zik_mac():
        p = re.compile('90:03:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}|'
                       'A0:14:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}')
        if sys.platform == "linux2":
            bluetooth_on = int(os.popen('bluez-test-adapter powered').read())
            if bluetooth_on == 1:
                out = os.popen("bluez-test-device list").read()
                res = p.findall(out)
                if len(res) > 0:
                    return res[0]
                else:
                    raise DeviceNotConnected
            else:
                raise BluetoothIsNotOn
        elif sys.platform == "darwin":
            fd = open("/Library/Preferences/com.apple.Bluetooth.plist", "rb")
            plist = binplist.BinaryPlist(file_obj=fd)
            parsed_plist = plist.Parse()
            try:
                for mac in parsed_plist['PairedDevices']:
                    if p.match(mac.replace("-", ":")):
                        return mac.replace("-", ":")
                else:
                    raise DeviceNotConnected
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
                    else:
                        raise DeviceNotConnected
                except EnvironmentError:
                    pass


def connect():
    mac = get_parrot_zik_mac()
    if sys.platform == "darwin":
        service_matches = lightblue.findservices(
            name="Parrot RFcomm service", addr=mac)
    else:
        uuids = ["0ef0f502-f0ee-46c9-986c-54ed027807fb",
                 "8B6814D3-6CE7-4498-9700-9312C1711F63"]
        service_matches = []
        for uuid in uuids:
            try:
                service_matches = bluetooth.find_service(uuid=uuid, address=mac)
            except bluetooth.btcommon.BluetoothError:
                pass
            if service_matches:
                break

    if len(service_matches) == 0:
        raise ConnectionFailure
    first_match = service_matches[0]

    if sys.platform == "darwin":
        host = first_match[0]
        port = first_match[1]
        sock = lightblue.socket()
    else:
        port = first_match["port"]
        host = first_match["host"]
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    sock.connect((host, port))

    sock.send('\x00\x03\x00')
    sock.recv(1024)
    return GenericResourceManager(sock)


class DeviceNotConnected(Exception):
    pass


class ConnectionFailure(Exception):
    pass


class BluetoothIsNotOn(Exception):
    pass
