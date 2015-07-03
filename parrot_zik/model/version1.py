from parrot_zik.model.base import ParrotZikBase
from parrot_zik.resource_manager import Version1ResourceManager


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
        self.resource_manager.set("/api/audio/specific_mode/enabled", arg)

    @property
    def concert_hall(self):
        answer = self.resource_manager.get("/api/audio/sound_effect/enabled")
        return self._result_to_bool(
            answer.audio.sound_effect["enabled"])

    @concert_hall.setter
    def concert_hall(self, arg):
        self.resource_manager.set("/api/audio/sound_effect/enabled", arg)

    @property
    def cancel_noise(self):
        answer = self.resource_manager.get("/api/audio/noise_cancellation/enabled")
        return self._result_to_bool(
            answer.audio.noise_cancellation["enabled"])

    @cancel_noise.setter
    def cancel_noise(self, arg):
        self.resource_manager.set("/api/audio/noise_cancellation/enabled", arg)
