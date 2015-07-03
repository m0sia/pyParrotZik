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
        return int(answer.system.battery[field_name] or 0)

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

class BatteryStates:
    CHARGED = 'charged'
    IN_USE = 'in_use'
    CHARGING = 'charging'
    representation = {
        CHARGED: 'Charged',
        IN_USE: 'In Use',
        CHARGING: 'Charging',
    }
