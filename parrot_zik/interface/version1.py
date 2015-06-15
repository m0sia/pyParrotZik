from parrot_zik import resource_manager
from parrot_zik.indicator import MenuItem
from parrot_zik.interface.base import ParrotZikBaseInterface
from parrot_zik.model.version1 import ParrotZikVersion1


class ParrotZikVersion1Interface(ParrotZikBaseInterface):
    parrot_class = ParrotZikVersion1

    def __init__(self, indicator):
        super(ParrotZikVersion1Interface, self).__init__(indicator)
        self.noise_cancelation = MenuItem(
            "Noise Cancellation", self.toggle_noise_cancelation,
            checkitem=True, visible=False)
        self.lou_reed_mode = MenuItem("Lou Reed Mode", self.toggle_lou_reed_mode,
                                      checkitem=True, visible=False)
        self.concert_hall_mode = MenuItem(
            "Concert Hall Mode", self.toggle_parrot_concert_hall,
            checkitem=True, visible=False)
        self.indicator.menu.append(self.noise_cancelation)
        self.indicator.menu.append(self.lou_reed_mode)
        self.indicator.menu.append(self.concert_hall_mode)

    def activate(self, manager):
        self.noise_cancelation.show()
        self.lou_reed_mode.show()
        self.concert_hall_mode.show()
        super(ParrotZikVersion1Interface, self).activate(manager)
        self.noise_cancelation.set_active(self.parrot.cancel_noise)
        self.lou_reed_mode.set_active(self.parrot.lou_reed_mode)
        self.concert_hall_mode.set_active(self.parrot.concert_hall)

    def deactivate(self):
        self.noise_cancelation.hide()
        self.lou_reed_mode.hide()
        self.concert_hall_mode.hide()
        super(ParrotZikVersion1Interface, self).deactivate()

    def toggle_noise_cancelation(self, widget):
        try:
            self.parrot.cancel_noise = self.noise_cancelation.get_active()
            self.noise_cancelation.set_active(self.parrot.cancel_noise)
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def toggle_lou_reed_mode(self, widget):
        try:
            self.parrot.lou_reed_mode = self.lou_reed_mode.get_active()
            self.lou_reed_mode.set_active(self.parrot.lou_reed_mode)
            self.concert_hall_mode.set_active(self.parrot.concert_hall)
            self.concert_hall_mode.set_sensitive(
                not self.lou_reed_mode.get_active())
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def toggle_parrot_concert_hall(self, widget):
        try:
            self.parrot.concert_hall = self.concert_hall_mode.get_active()
            self.concert_hall_mode.set_active(self.parrot.concert_hall)
        except resource_manager.DeviceDisconnected:
            self.deactivate()
