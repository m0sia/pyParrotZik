from resource_manager import Version1ResourceManager
from resource_manager import Version2ResourceManager


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

class NoiseControl(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    @classmethod
    def from_noise_control(cls, noise_control):
        return cls(noise_control['type'], int(noise_control['value']))

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __str__(self):
        return '{}++{}'.format(self.type, self.value)

class NoiseControlTypes:
    NOISE_CONTROL_MAX = NoiseControl('anc', 2)
    NOISE_CONTROL_ON = NoiseControl('anc', 1)
    NOISE_CONTROL_OFF = NoiseControl('off', 1)
    STREET_MODE = NoiseControl('aoc', 1)
    STREET_MODE_MAX = NoiseControl('aoc', 2)


class ParrotZikBase(object):
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

    @property
    def version(self):
        return self.resource_manager.api_version

    def refresh_battery(self):
        self.resource_manager.fetch('/api/system/battery')

    @property
    def battery_state(self):
        answer = self.resource_manager.get("/api/system/battery")
        return answer.system.battery["state"]

    def get_battery_level(self, field_name):
        answer = self.resource_manager.get("/api/system/battery")
        return int(answer.system.battery[field_name])

    @property
    def friendly_name(self):
        answer = self.resource_manager.get("/api/bluetooth/friendlyname")
        return answer.bluetooth["friendlyname"]

    @property
    def auto_connect(self):
        answer = self.resource_manager.get("/api/system/auto_connection/enabled")
        return self._result_to_bool(
            answer.system.auto_connection["enabled"])

    @auto_connect.setter
    def auto_connect(self, arg):
        self.resource_manager.set("/api/system/auto_connection/enabled", arg)

    @property
    def anc_phone_mode(self):
        answer = self.resource_manager.get("/api/system/anc_phone_mode/enabled")
        return self._result_to_bool(
            answer.system.anc_phone_mode["enabled"])

    def _result_to_bool(self, result):
        if result == "true":
            return True
        elif result == "false":
            return False
        else:
            raise AssertionError(result)


class ParrotZikVersion1(ParrotZikBase):
    def __init__(self, resource_manager):
        super(ParrotZikVersion1, self).__init__(
            resource_manager.get_resource_manager(
                Version1ResourceManager))

    @property
    def version(self):
        answer = self.resource_manager.get('/api/software/version')
        return answer.software['version']

    @property
    def battery_level(self):
        return int(self.get_battery_level('level'))

    @property
    def lou_reed_mode(self):
        answer = self.resource_manager.get("/api/audio/specific_mode/enabled")
        return self._result_to_bool(
            answer.audio.specific_mode["enabled"])

    @lou_reed_mode.setter
    def lou_reed_mode(self, arg):
        self.resource_manager.get("/api/audio/specific_mode/enabled", arg)

    @property
    def concert_hall(self):
        answer = self.resource_manager.get("/api/audio/sound_effect/enabled")
        return self._result_to_bool(
            answer.audio.sound_effect["enabled"])

    @concert_hall.setter
    def concert_hall(self, arg):
        self.resource_manager.get("/api/audio/sound_effect/enabled", arg)

    @property
    def cancel_noise(self):
        answer = self.resource_manager.get("/api/audio/noise_cancellation/enabled")
        return self._result_to_bool(
            answer.audio.noise_cancellation["enabled"])

    @cancel_noise.setter
    def cancel_noise(self, arg):
        self.resource_manager.set("/api/audio/noise_cancellation/enabled", arg)


class ParrotZikVersion2(ParrotZikBase):
    def __init__(self, resource_manager):
        super(ParrotZikVersion2, self).__init__(
            resource_manager.get_resource_manager(
                Version2ResourceManager))

    @property
    def version(self):
        answer = self.resource_manager.get('/api/software/version')
        return answer.software['sip6']

    @property
    def battery_level(self):
        return self.get_battery_level('percent')

    @property
    def flight_mode(self):
        answer = self.resource_manager.get('/api/flight_mode')
        return self._result_to_bool(answer.flight_mode['enabled'])

    @flight_mode.setter
    def flight_mode(self, arg):
        if arg:
            self.resource_manager.toggle_on('/api/flight_mode')
        else:
            self.resource_manager.toggle_off('/api/flight_mode')

    @property
    def sound_effect(self):
        answer = self.resource_manager.get('/api/audio/sound_effect/enabled')
        return self._result_to_bool(answer.audio.sound_effect['enabled'])

    @sound_effect.setter
    def sound_effect(self, arg):
        self.resource_manager.set('/api/audio/sound_effect/enabled', arg)

    @property
    def room(self):
        answer = self.resource_manager.get('/api/audio/sound_effect/room_size')
        return answer.audio.sound_effect['room_size']

    @room.setter
    def room(self, arg):
        self.resource_manager.set('/api/audio/sound_effect/room_size', arg)

    @property
    def external_noise(self):
        answer = self.resource_manager.get('/api/audio/noise')
        return int(answer.audio.noise['external'])

    @property
    def internal_noise(self):
        answer = self.resource_manager.get('/api/audio/noise')
        return int(answer.audio.noise['internal'])

    @property
    def angle(self):
        answer = self.resource_manager.get('/api/audio/sound_effect/angle')
        return int(answer.audio.sound_effect['angle'])

    @angle.setter
    def angle(self, arg):
        self.resource_manager.set('/api/audio/sound_effect/angle', arg)

    @property
    def noise_control(self):
        answer = self.resource_manager.get('/api/audio/noise_control')
        return NoiseControl.from_noise_control(answer.audio.noise_control)

    @noise_control.setter
    def noise_control(self, arg):
        pass

    @property
    def noise_control_enabled(self):
        answer = self.resource_manager.get('/api/audio/noise_control/enabled')
        return self._result_to_bool(answer.audio.noise_control['enabled'])
