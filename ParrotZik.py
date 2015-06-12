import sys
if sys.platform == "darwin":
    import lightblue
else:
    import bluetooth

import ParrotProtocol
from BeautifulSoup import BeautifulSoup

def connect(addr=None):
    uuids = ["0ef0f502-f0ee-46c9-986c-54ed027807fb",
             "8B6814D3-6CE7-4498-9700-9312C1711F63"]

    if sys.platform == "darwin":
        service_matches = lightblue.findservices(
            name="Parrot RFcomm service", addr=addr)
    else:
        for uuid in uuids:
            service_matches = bluetooth.find_service(uuid=uuid,
                                                     address=addr)
            if service_matches:
                break

    if len(service_matches) == 0:
        print "Failed to find Parrot Zik RFCOMM service"
        return ParrotZikBase(ParrotZikApi(None))

    if sys.platform == "darwin":
        first_match = service_matches[0]
        port = first_match[1]
        name = first_match[2]
        host = first_match[0]
    else:
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

    print "Connecting to \"%s\" on %s" % (name, host)

    if sys.platform == "darwin":
        sock = lightblue.socket()
    else:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    sock.connect((host, port))

    sock.send('\x00\x03\x00')
    data = sock.recv(1024)
    api = ParrotZikApi(sock)
    if api.version.startswith('1'):
        return ParrotZikVersion1(api)
    else:
        return ParrotZikVersion2(api)


class ParrotZikApi(object):
    def __init__(self, socket):
        self.sock = socket

    @property
    def version(self):
        data = self.get("/api/software/version/get")
        try:
            return data.answer.software["version"]
        except KeyError:
            return data.answer.software['sip6']

    def get(self, message):
        message = ParrotProtocol.getRequest(message)
        return self.send_message(message)

    def set(self, message, arg):
        message = ParrotProtocol.setRequest(message, str(arg).lower())
        return self.send_message(message)

    def send_message(self, message):
        try:
            self.sock.send(str(message))
        except Exception:
            self.sock = ""
            return
        if sys.platform == "darwin":
            data = self.sock.recv(30)
        else:
            data = self.sock.recv(7)
        data = self.sock.recv(1024)
        data = BeautifulSoup(data)
        return data

    def close(self):
        self.sock.close()

class BatteryStates:
    CHARGED = 'charged'
    IN_USE = 'in_use'
    CHARGING = 'charging'
    representation = {
        CHARGED: 'Charged',
        IN_USE: 'In Use',
        CHARGING: 'Charging',
    }

class ParrotZikBase(object):

    def __init__(self, api):
        self.api = api

    @property
    def version(self):
        return self.api.version

    @property
    def battery_state(self):
        data = self.api.get("/api/system/battery/get")
        return data.answer.system.battery["state"]

    def get_battery_level(self, field_name):
        data = self.api.get("/api/system/battery/get")
        return data.answer.system.battery[field_name]

    @property
    def friendly_name(self):
        data = self.api.get("/api/bluetooth/friendlyname/get")
        return data.answer.bluetooth["friendlyname"]

    @property
    def auto_connect(self):
        data = self.api.get("/api/system/auto_connection/enabled/get")
        return self._result_to_bool(
            data.answer.system.auto_connection["enabled"])

    @auto_connect.setter
    def auto_connect(self, arg):
        self.api.get("/api/system/auto_connection/enabled/set", arg)

    @property
    def anc_phone_mode(self):
        data = self.api.get("/api/system/anc_phone_mode/enabled/get")
        return self._result_to_bool(
            data.answer.system.anc_phone_mode["enabled"])

    @property
    def noise_cancel(self):
        data = self.api.get("/api/audio/noise_cancellation/enabled/get")
        try:
            return self._result_to_bool(
                data.answer.audio.noise_cancellation["enabled"])
        except AttributeError:
            return False

    @noise_cancel.setter
    def noise_cancel(self, arg):
        self.api.get("/api/audio/noise_cancellation/enabled/set", arg)

    @property
    def concert_hall(self):
        data = self.api.get("/api/audio/sound_effect/enabled/get")
        try:
            return self._result_to_bool(
                data.answer.audio.sound_effect["enabled"])
        except AttributeError:
            return False

    @concert_hall.setter
    def concert_hall(self, arg):
        self.api.get("/api/audio/sound_effect/enabled/set", arg)

    def _result_to_bool(self, result):
        if result == "true":
            return True
        elif result == "false":
            return False
        else:
            raise AssertionError(result)


class ParrotZikVersion1(ParrotZikBase):
    @property
    def battery_level(self):
        return int(self.get_battery_level('level'))

    @property
    def lou_reed_mode(self):
        data = self.api.get("/api/audio/specific_mode/enabled/get")
        return self._result_to_bool(
            data.answer.audio.specific_mode["enabled"])

    @lou_reed_mode.setter
    def lou_reed_mode(self, arg):
        self.api.get("/api/audio/specific_mode/enabled/set", arg)


class ParrotZikVersion2(ParrotZikBase):
    @property
    def battery_level(self):
        return self.get_battery_level('percent')

    @property
    def flight_mode(self):
        data = self.api.get('/api/flight_mode/get')
        return self._result_to_bool(data.answer.flight_mode['enabled'])

    @flight_mode.setter
    def flight_mode(self, arg):
        self.api.set('/api/flight_mode/set', arg)

    @property
    def room_size(self):
        data = self.api.get('/api/audio/sound_effect/room_size/get')
        return data.answer.audio.sound_effect['room_size']

    @room_size.setter
    def room_size(self, arg):
        self.api.set('/api/audio/sound_effect/room_size/set', arg)

    @property
    def external_noise(self):
        data = self.api.get('/api/audio/noise/get')
        return int(data.answer.audio.noise['external'])

    @property
    def internal_noise(self):
        data = self.api.get('/api/audio/noise/get')
        return int(data.answer.audio.noise['internal'])

    @property
    def angle(self):
        data = self.api.get('/api/audio/sound_effect/angle/get')
        return int(data.answer.audio.sound_effect['angle'])

    @angle.setter
    def angle(self, arg):
        self.api.set('/api/audio/sound_effect/angle/set', arg)

    @property
    def noise_control(self):
        data = self.api.get('/api/audio/noise_control/get')
        return self._result_to_bool(data.answer.audio.noise_control['value'])

    @noise_control.setter
    def noise_control(self, arg):
        self.api.set('/api/audio/noise_control/set', arg)

    @property
    def noise_control_enabled(self):
        data = self.api.get('/api/audio/noise_control/enabled/get')
        return self._result_to_bool(data.answer.audio.noise_control['enabled'])
