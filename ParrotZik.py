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
        data = self.get("/api/software/version")
        try:
            return data.answer.software["version"]
        except KeyError:
            return data.answer.software['sip6']

    def get(self, resource):
        message = ParrotProtocol.getRequest(resource + '/get')
        return self.send_message(message)

    def toggle_on(self, resource):
        message = ParrotProtocol.getRequest(resource + '/enable')
        return self.send_message(message)

    def toggle_off(self, resource):
        message = ParrotProtocol.getRequest(resource + '/disable')
        return self.send_message(message)

    def set(self, resource, arg):
        message = ParrotProtocol.setRequest(resource + '/set', str(arg).lower())
        return self.send_message(message)

    def send_message(self, message):
        try:
            self.sock.send(str(message))
        except Exception:
            self.sock = ""
            return
        if sys.platform == "darwin":
            self.sock.recv(30)
        else:
            self.sock.recv(7)

        data = BeautifulSoup(self.sock.recv(1024))
        if not hasattr(data, 'anwser'):
            data = BeautifulSoup(self.sock.recv(1024))
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

class Rooms:
    CONCERT_HALL = 'concert'
    JAZZ_CLUB = 'jazz'
    LIVING_ROOM = 'living'
    SILENT_ROOM = 'silent'
    representation = {
        CONCERT_HALL: 'Concert Hall',
        JAZZ_CLUB: 'Jazz Club',
        LIVING_ROOM: 'Living Room',
        SILENT_ROOM: 'Silent Room',
    }


class ParrotZikBase(object):
    def __init__(self, api):
        self.api = api

    @property
    def version(self):
        return self.api.version

    @property
    def battery_state(self):
        data = self.api.get("/api/system/battery")
        return data.answer.system.battery["state"]

    def get_battery_level(self, field_name):
        data = self.api.get("/api/system/battery")
        return data.answer.system.battery[field_name]

    @property
    def friendly_name(self):
        data = self.api.get("/api/bluetooth/friendlyname")
        return data.answer.bluetooth["friendlyname"]

    @property
    def auto_connect(self):
        data = self.api.get("/api/system/auto_connection/enabled")
        return self._result_to_bool(
            data.answer.system.auto_connection["enabled"])

    @auto_connect.setter
    def auto_connect(self, arg):
        self.api.set("/api/system/auto_connection/enabled", arg)

    @property
    def anc_phone_mode(self):
        data = self.api.get("/api/system/anc_phone_mode/enabled")
        return self._result_to_bool(
            data.answer.system.anc_phone_mode["enabled"])

    @property
    def noise_cancel(self):
        data = self.api.get("/api/audio/noise_cancellation/enabled")
        return self._result_to_bool(
            data.answer.audio.noise_cancellation["enabled"])

    @noise_cancel.setter
    def noise_cancel(self, arg):
        self.api.set("/api/audio/noise_cancellation/enabled", arg)

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
        data = self.api.get("/api/audio/specific_mode/enabled")
        return self._result_to_bool(
            data.answer.audio.specific_mode["enabled"])

    @lou_reed_mode.setter
    def lou_reed_mode(self, arg):
        self.api.get("/api/audio/specific_mode/enabled", arg)

    @property
    def concert_hall(self):
        data = self.api.get("/api/audio/sound_effect/enabled")
        return self._result_to_bool(
            data.answer.audio.sound_effect["enabled"])

    @concert_hall.setter
    def concert_hall(self, arg):
        self.api.get("/api/audio/sound_effect/enabled", arg)


class ParrotZikVersion2(ParrotZikBase):
    @property
    def battery_level(self):
        return self.get_battery_level('percent')

    @property
    def flight_mode(self):
        data = self.api.get('/api/flight_mode')
        return self._result_to_bool(data.answer.flight_mode['enabled'])

    @flight_mode.setter
    def flight_mode(self, arg):
        if arg:
            self.api.toggle_on('/api/flight_mode')
        else:
            self.api.toggle_off('/api/flight_mode')

    @property
    def sound_effect(self):
        data = self.api.get('/api/audio/sound_effect/enabled')
        return self._result_to_bool(data.answer.audio.sound_effect['enabled'])

    @sound_effect.setter
    def sound_effect(self, arg):
        self.api.set('/api/audio/sound_effect/enabled', arg)

    @property
    def room(self):
        data = self.api.get('/api/audio/sound_effect/room_size')
        return data.answer.audio.sound_effect['room_size']

    @room.setter
    def room(self, arg):
        self.api.set('/api/audio/sound_effect/room_size', arg)

    @property
    def external_noise(self):
        data = self.api.get('/api/audio/noise')
        return int(data.answer.audio.noise['external'])

    @property
    def internal_noise(self):
        data = self.api.get('/api/audio/noise')
        return int(data.answer.audio.noise['internal'])

    @property
    def angle(self):
        data = self.api.get('/api/audio/sound_effect/angle')
        return int(data.answer.audio.sound_effect['angle'])

    @angle.setter
    def angle(self, arg):
        self.api.set('/api/audio/sound_effect/angle', arg)

    @property
    def noise_control(self):
        data = self.api.get('/api/audio/noise_control')
        return self._result_to_bool(data.answer.audio.noise_control['value'])

    @noise_control.setter
    def noise_control(self, arg):
        self.api.set('/api/audio/noise_control', arg)

    @property
    def noise_control_enabled(self):
        data = self.api.get('/api/audio/noise_control/enabled')
        return self._result_to_bool(data.answer.audio.noise_control['enabled'])
