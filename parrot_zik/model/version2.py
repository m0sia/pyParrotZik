from parrot_zik.model.base import ParrotZikBase
from parrot_zik.resource_manager import Version2ResourceManager


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
        self.resource_manager.set('/api/audio/noise_control', arg)

    @property
    def noise_control_enabled(self):
        answer = self.resource_manager.get('/api/audio/noise_control/enabled')
        return self._result_to_bool(answer.audio.noise_control['enabled'])

    @property
    def head_detection(self):
        answer = self.resource_manager.get('/api/system/head_detection/enabled')
        return self._result_to_bool(answer.system.head_detection['enabled'])

    @head_detection.setter
    def head_detection(self, arg):
        self.resource_manager.set('/api/system/head_detection/enabled', arg)


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
        return '{}&value={}'.format(self.type, self.value)


class NoiseControlTypes:
    NOISE_CONTROL_MAX = NoiseControl('anc', 2)
    NOISE_CONTROL_ON = NoiseControl('anc', 1)
    NOISE_CONTROL_OFF = NoiseControl('off', 1)
    STREET_MODE = NoiseControl('aoc', 1)
    STREET_MODE_MAX = NoiseControl('aoc', 2)


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

class SoundSource:
    LINE_IN = 'line-in'
    A2DP = 'a2dp'
