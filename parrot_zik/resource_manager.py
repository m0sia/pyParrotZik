import bluetooth
from operator import itemgetter
import sys

from bs4 import BeautifulSoup

from .message import Message


class ResourceManagerBase(object):
    resources = [
    ]

    def __init__(self, socket, resource_values=None):
        self.sock = socket
        self.resource_values = resource_values or {}

    def get(self, resource):
        try:
            return self.resource_values[resource]
        except KeyError:
            return self.fetch(resource)

    def fetch(self, resource):
        result = self.send_message(self._create_message(resource, 'get'))
        self.resource_values[resource] = result
        return result

    def toggle_on(self, resource):
        self.send_message(self._create_message(resource, 'enable'))
        self.fetch(resource)

    def toggle_off(self, resource):
        self.send_message(self._create_message(resource, 'disable'))
        self.fetch(resource)

    def set(self, resource, arg):
        self.send_message(self._create_message(resource, 'set', arg))
        self.fetch(resource)

    def _create_message(self, resource, method, arg=None):
        assert resource in self.resources, 'Unknown resource {}'.format(resource)
        assert method in self.resources[resource], 'Unhandled method {} for {}'.format(method, resource)
        return Message(resource, method, arg)

    def send_message(self, message):
        try:
            self.sock.send(str(message))
            return self.get_answer(message)
        except bluetooth.btcommon.BluetoothError:
            raise DeviceDisconnected

    def get_answer(self, message):
        data = self.receive_message()
        notifications = []
        while not data.answer:
            if data.notify:
                notifications.append(data.notify)
            else:
                raise AssertionError('Unknown response "{}" for {}'.format(
                    data, message.request_string))
            data = self.receive_message()
        self.handle_notifications(notifications, message.resource)
        return data.answer

    def handle_notifications(self, notifications, resource):
        paths = map(itemgetter('path'), notifications)
        clean_paths = set(map(self._clean_path, paths))
        for path in clean_paths:
            if resource != path:
                self.fetch(path)

    def _clean_path(self, path):
        return path.rsplit('/', 1)[0].encode('utf-8')

    def receive_message(self):
        if sys.platform == "darwin":
            self.sock.recv(30)
        else:
            self.sock.recv(7)
        return BeautifulSoup(self.sock.recv(1024))

    def close(self):
        self.sock.close()


class GenericResourceManager(ResourceManagerBase):
    resources = {
        '/api/software/version': ['get'],
    }

    def __init__(self, sock):
        super(GenericResourceManager, self).__init__(sock)
        self.notifications = []

    def handle_notification(self, notification):
        self.notifications.append(notification)

    def get_resource_manager(self, resource_manager_class):
        resource_manager = resource_manager_class(self.sock, self.resource_values)
        resource_manager.handle_notifications(self.notifications, '/api/software/version')
        return resource_manager

    @property
    def api_version(self):
        answer = self.get("/api/software/version")
        try:
            return answer.software["version"]
        except KeyError:
            return answer.software['sip6']


class Version1ResourceManager(ResourceManagerBase):
    resources = {
        '/api/software/version': ['get'],
        '/api/system/battery': ['get'],
        '/api/bluetooth/friendlyname': ['get'],
        '/api/system/auto_connection/enabled': ['get', 'set'],
        '/api/system/anc_phone_mode/enabled': ['get', 'set'],
        '/api/audio/specific_mode/enabled': ['get', 'set'],
        '/api/audio/sound_effect/enabled': ['get', 'set'],
        '/api/audio/noise_cancellation/enabled': ['get', 'set'],
    }

class Version2ResourceManager(ResourceManagerBase):
    resources = {
        '/api/account/username': ['get', 'set'],
        '/api/appli_version': ['set'],
        '/api/audio/counter': ['get'],
        '/api/audio/equalizer/enabled': ['get', 'set'],
        '/api/audio/equalizer/preset_id': ['set'],
        '/api/audio/equalizer/preset_value': ['set'],
        '/api/audio/noise_cancellation/enabled': ['get', 'set'],
        '/api/audio/noise_control/enabled': ['get', 'set'],
        '/api/audio/noise_control': ['get', 'set'],
        '/api/audio/noise_control/phone_mode': ['get', 'set'],
        '/api/audio/noise': ['get'],
        '/api/audio/param_equalizer/value': ['set'],
        '/api/audio/preset/bypass': ['get', 'set'],
        '/api/audio/preset/': ['clear_all'],
        '/api/audio/preset/counter': ['get'],
        '/api/audio/preset/current': ['get'],
        '/api/audio/preset': ['download', 'activate', 'save', 'remove', 'cancel_producer'],
        '/api/audio/preset/synchro': ['start', 'stop'],
        '/api/audio/smart_audio_tune': ['get', 'set'],
        '/api/audio/sound_effect/angle': ['get', 'set'],
        '/api/audio/sound_effect/enabled': ['get', 'set'],
        '/api/audio/sound_effect': ['get'],
        '/api/audio/sound_effect/room_size': ['get', 'set'],
        '/api/audio/source': ['get'],
        '/api/audio/specific_mode/enabled': ['get', 'set'],
        '/api/audio/thumb_equalizer/value': ['get', 'set'],
        '/api/audio/track/metadata': ['get', 'force'],
        '/api/bluetooth/friendlyname': ['get', 'set'],
        '/api/flight_mode': ['get', 'enable', 'disable'],
        '/api/software/download_check_state': ['get'],
        '/api/software/download_size': ['set'],
        '/api/software/tts': ['get', 'enable', 'disable'],
        '/api/software/version_checking': ['get'],
        '/api/software/version': ['get'],
        '/api/system/anc_phone_mode/enabled': ['get', 'set'],
        '/api/system/auto_connection/enabled': ['get', 'set'],
        '/api/system/auto_power_off': ['get', 'set'],
        '/api/system/auto_power_off/presets_list': ['get'],
        '/api/system/battery/forecast': ['get'],
        '/api/system/battery': ['get'],
        '/api/system/bt_address': ['get'],
        '/api/system': ['calibrate'],
        '/api/system/color': ['get'],
        '/api/system/device_type': ['get'],
        '/api/system/': ['factory_reset'],
        '/api/system/head_detection/enabled': ['get', 'set'],
        '/api/system/pi': ['get'],
    }

class DeviceDisconnected(Exception):
    pass
