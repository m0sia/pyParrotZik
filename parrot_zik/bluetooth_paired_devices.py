import dbus
import sys
import re
from subprocess import Popen, PIPE, STDOUT

from .resource_manager import GenericResourceManager

if sys.platform == "darwin":
    from binplist import binplist
    import lightblue
else:
    import bluetooth
    if sys.platform == "win32":
        import _winreg


p = re.compile('90:03:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}|'
               'A0:14:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}')


def get_parrot_zik_mac_linux_using_bluez_test():
    try:
        pipe = Popen(
            ['bluez-test-adapter', 'powered'],
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT
        )
        bluetooth_on = int(pipe.communicate())
    except dbus.exceptions.DBusException:
        pass
    else:
        if bluetooth_on == 1:
            try:
                pipe = Popen(
                    ['bluez-test-device', 'list'],
                    stdout=PIPE,
                    stdin=PIPE,
                    stderr=STDOUT
                )
                out = pipe.communicate()
            except dbus.exceptions.DBusException:
                pass
            else:
                res = p.findall(out)
                if len(res) > 0:
                    return res[0]
                else:
                    raise DeviceNotConnected
        else:
            raise BluetoothIsNotOn


def get_parrot_zik_mac_linux_using_bluetoothcmd():
    pipe = Popen(['bluetoothctl'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    res = pipe.communicate("exit")
    if len(res) > 0 and res[0]:
        match = p.search(res[0])
        if match:
            return match.group(0)

    raise DeviceNotConnected


def get_parrot_zik_mac_linux():
    try:
        get_parrot_zik_mac_linux_using_bluez_test()
    except OSError as e:
        if e.errno == 2:
            # File not found, probably it means that bluez utils are not
            # installed
            return get_parrot_zik_mac_linux_using_bluetoothcmd()


def get_parrot_zik_mac_darwin():
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


def get_parrot_zik_mac_windows():
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


if sys.platform in ['linux', 'linux2']:
    get_parrot_zik_mac = get_parrot_zik_mac_linux
elif sys.platform == 'darwin':
    get_parrot_zik_mac = get_parrot_zik_mac_darwin
elif sys.platform == 'win32':
    get_parrot_zik_mac = get_parrot_zik_mac_windows
else:
    raise AssertionError('Platform not supported')


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

    try:
        sock.connect((host, port))
    except bluetooth.btcommon.BluetoothError:
        raise ConnectionFailure

    sock.send('\x00\x03\x00')
    sock.recv(1024)
    return GenericResourceManager(sock)


class DeviceNotConnected(Exception):
    pass


class ConnectionFailure(Exception):
    pass


class BluetoothIsNotOn(Exception):
    pass
