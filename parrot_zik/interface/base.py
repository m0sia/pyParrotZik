from .. import resource_manager
from ..indicator import MenuItem
from ..model.base import BatteryStates

RECONNECT_FREQUENCY = 5000


class ParrotZikBaseInterface(object):
    def __init__(self, indicator):
        self.indicator = indicator
        self.parrot = None
        self.battery_level = MenuItem("Battery Level:", None, sensitive=False,
                                      visible=False)
        self.battery_state = MenuItem("Battery State:", None, sensitive=False,
                                      visible=False)
        self.firmware_version = MenuItem("Firmware Version:", None,
                                         sensitive=False, visible=False)
        self.auto_connection = MenuItem("Auto Connection", self.toggle_auto_connection,
                                        checkitem=True, visible=False)
        self.indicator.menu.append(self.battery_level)
        self.indicator.menu.append(self.battery_state)
        self.indicator.menu.append(self.firmware_version)
        self.indicator.menu.append(self.auto_connection)

    def activate(self, manager):
        self.parrot = self.parrot_class(manager)
        self.read_battery()
        self.indicator.info("Connected to: " + self.parrot.friendly_name)
        self.firmware_version.set_label(
            "Firmware version: " + self.parrot.version)
        self.auto_connection.set_active(self.parrot.auto_connect)
        self.battery_level.show()
        self.battery_state.show()
        self.firmware_version.show()
        self.auto_connection.show()
        self.indicator.active_interface = self
        self.indicator.menu.reposition()

    @property
    def parrot_class(self):
        raise NotImplementedError

    def deactivate(self):
        self.parrot = None
        self.battery_level.hide()
        self.battery_state.hide()
        self.firmware_version.hide()
        self.auto_connection.hide()
        self.indicator.menu.reposition()
        self.indicator.active_interface = None
        self.indicator.setIcon("zik-audio-headset")
        self.indicator.info('Lost Connection')
        self.indicator.reconnect.start(self.indicator, RECONNECT_FREQUENCY)

    def toggle_auto_connection(self, widget):
        try:
            self.parrot.auto_connect = self.auto_connection.get_active()
            self.auto_connection.set_active(self.parrot.auto_connect)
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def refresh(self):
        self.read_battery()

    def read_battery(self):
        try:
            self.parrot.refresh_battery()
            battery_level = self.parrot.battery_level
            battery_state = self.parrot.battery_state
        except resource_manager.DeviceDisconnected:
            self.deactivate()
        else:
            if battery_state == BatteryStates.CHARGING:
                self.indicator.setIcon("zik-battery-charging")
            elif battery_level > 80:
                self.indicator.setIcon("zik-battery-100")
            elif battery_level > 60:
                self.indicator.setIcon("zik-battery-080")
            elif battery_level > 40:
                self.indicator.setIcon("zik-battery-060")
            elif battery_level > 20:
                self.indicator.setIcon("zik-battery-040")
            else:
                self.indicator.setIcon("zik-battery-low")

            self.battery_state.set_label(
                "State: " + BatteryStates.representation[battery_state])
            self.battery_level.set_label(
                "Battery Level: " + str(battery_level))
