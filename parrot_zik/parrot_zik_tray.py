from parrot_zik.interface.version1 import ParrotZikVersion1Interface
from parrot_zik.interface.version2 import ParrotZikVersion2Interface
from parrot_zik import resource_manager
from parrot_zik import bluetooth_paired_devices
from parrot_zik.indicator import MenuItem
from parrot_zik.indicator import Menu
from parrot_zik.indicator import SysIndicator
from parrot_zik.utils import repeat

REFRESH_FREQUENCY = 30000
RECONNECT_FREQUENCY = 5000



class ParrotZikIndicator(SysIndicator):
    def __init__(self):
 
        self.menu = Menu()

        self.info_item = MenuItem("Parrot Zik Not connected",
                                  None, sensitive=False)
        self.menu.append(self.info_item)

        self.version_1_interface = ParrotZikVersion1Interface(self)
        self.version_2_interface = ParrotZikVersion2Interface(self)
        self.quit_item = MenuItem("Quit", self.quit, checkitem=True)
        self.menu.append(self.quit_item)

        SysIndicator.__init__(self, icon="zik-audio-headset", menu=self.menu)

        self.active_interface = None

    @repeat
    def reconnect(self):
        if self.active_interface:
            self.reconnect.stop()
        else:
            self.info("Trying to connect")
            try:
                manager = bluetooth_paired_devices.connect()
            except bluetooth_paired_devices.BluetoothIsNotOn:
                self.info("Bluetooth is turned off")
            except bluetooth_paired_devices.DeviceNotConnected:
                self.info("Parrot Zik Not connected")
            except bluetooth_paired_devices.ConnectionFailure:
                self.info("Failed to connect")
            else:
                if manager.api_version.startswith('1'):
                    interface = self.version_1_interface
                else:
                    interface = self.version_2_interface
                try:
                    interface.activate(manager)
                except resource_manager.DeviceDisconnected:
                    interface.deactivate()
                else:
                    self.autorefresh(self)
                    self.autorefresh.start(self, REFRESH_FREQUENCY)
                    self.reconnect.stop()

    def info(self, message):
        self.info_item.set_label(message)
        print(message)

    @repeat
    def autorefresh(self):
        if self.active_interface:
            self.active_interface.refresh()
        else:
            self.reconnect.start(self, RECONNECT_FREQUENCY)
            self.autorefresh.stop()

    @classmethod
    def main(cls):
        try:
            indicator = cls()
            cls.reconnect.start(indicator, RECONNECT_FREQUENCY)
            super(ParrotZikIndicator, cls).main()
        except KeyboardInterrupt:
            pass
