import functools

from parrot_zik import resource_manager
from parrot_zik.indicator import MenuItem, Menu
from parrot_zik.interface.base import ParrotZikBaseInterface
from parrot_zik.model.version2 import ParrotZikVersion2
from parrot_zik.model.version2 import NoiseControlTypes
from parrot_zik.model.version2 import Rooms


class ParrotZikVersion2Interface(ParrotZikBaseInterface):
    parrot_class = ParrotZikVersion2

    def __init__(self, indicator):
        self.room_dirty = False
        self.angle_dirty = False
        self.noise_cancelation_dirty = False
        super(ParrotZikVersion2Interface, self).__init__(indicator)
        self.noise_cancelation = MenuItem("Noise Control", None, visible=False)
        self.noise_cancelation_submenu = Menu()
        self.noise_cancelation.set_submenu(self.noise_cancelation_submenu)

        self.noise_control_cancelation_max = MenuItem(
            "Max Calcelation", functools.partial(
                self.toggle_noise_cancelation,
                NoiseControlTypes.NOISE_CONTROL_MAX), checkitem=True)
        self.noise_control_cancelation_on = MenuItem(
            "Normal Cancelation", functools.partial(
                self.toggle_noise_cancelation,
                NoiseControlTypes.NOISE_CONTROL_ON), checkitem=True)
        self.noise_control_off = MenuItem(
            "Off", functools.partial(
                self.toggle_noise_cancelation,
                NoiseControlTypes.NOISE_CONTROL_OFF), checkitem=True)
        self.noise_control_street_mode = MenuItem(
            "Street Mode", functools.partial(
                self.toggle_noise_cancelation,
                NoiseControlTypes.STREET_MODE), checkitem=True)
        self.noise_control_street_mode_max = MenuItem(
            "Street Mode Max", functools.partial(
                self.toggle_noise_cancelation,
                NoiseControlTypes.STREET_MODE_MAX), checkitem=True)
        self.noise_cancelation_submenu.append(self.noise_control_cancelation_max)
        self.noise_cancelation_submenu.append(self.noise_control_cancelation_on)
        self.noise_cancelation_submenu.append(self.noise_control_off)
        self.noise_cancelation_submenu.append(self.noise_control_street_mode)
        self.noise_cancelation_submenu.append(self.noise_control_street_mode_max)

        self.room_sound_effect = MenuItem(
            "Room Sound Effect", None, visible=False)
        self.room_sound_effect_submenu = Menu()
        self.room_sound_effect.set_submenu(self.room_sound_effect_submenu)

        self.room_sound_effect_enabled = MenuItem(
            "Enabled", self.toggle_room_sound_effect, checkitem=True)
        self.rooms = MenuItem("Rooms", None, checkitem=False)
        self.angle = MenuItem("Angle", None, checkitem=False)
        self.room_sound_effect_submenu.append(self.room_sound_effect_enabled)
        self.room_sound_effect_submenu.append(self.rooms)
        self.room_sound_effect_submenu.append(self.angle)

        self.rooms_submenu = Menu()
        self.rooms.set_submenu(self.rooms_submenu)

        self.concert_hall_mode = MenuItem(
            "Concert Hall", functools.partial(self.toggle_room, Rooms.CONCERT_HALL), checkitem=True)
        self.jazz_mode = MenuItem(
            "Jazz Club", functools.partial(self.toggle_room, Rooms.JAZZ_CLUB), checkitem=True)
        self.living_mode = MenuItem(
            "Living Room", functools.partial(self.toggle_room, Rooms.LIVING_ROOM), checkitem=True)
        self.silent_mode = MenuItem(
            "Silent Room", functools.partial(self.toggle_room, Rooms.SILENT_ROOM), checkitem=True)
        self.rooms_submenu.append(self.concert_hall_mode)
        self.rooms_submenu.append(self.jazz_mode)
        self.rooms_submenu.append(self.living_mode)
        self.rooms_submenu.append(self.silent_mode)

        self.angle_submenu = Menu()
        self.angle.set_submenu(self.angle_submenu)
        self.angle_30 = MenuItem(
            "30", functools.partial(self.toggle_angle, 30), checkitem=True)
        self.angle_60 = MenuItem(
            "60", functools.partial(self.toggle_angle, 60), checkitem=True)
        self.angle_90 = MenuItem(
            "90", functools.partial(self.toggle_angle, 90), checkitem=True)
        self.angle_120 = MenuItem(
            "120", functools.partial(self.toggle_angle, 120), checkitem=True)
        self.angle_150 = MenuItem(
            "150", functools.partial(self.toggle_angle, 150), checkitem=True)
        self.angle_180 = MenuItem(
            "180", functools.partial(self.toggle_angle, 180), checkitem=True)
        self.angle_submenu.append(self.angle_30)
        self.angle_submenu.append(self.angle_60)
        self.angle_submenu.append(self.angle_90)
        self.angle_submenu.append(self.angle_120)
        self.angle_submenu.append(self.angle_150)
        self.angle_submenu.append(self.angle_180)

        self.flight_mode = MenuItem("Flight Mode", self.toggle_flight_mode,
                                    checkitem=True, visible=False)

        self.head_detection = MenuItem("Head Detection", self.toggle_head_detection, checkitem=True)
        self.settings_submenu.append(self.head_detection)

        self.indicator.menu.append(self.room_sound_effect)
        self.indicator.menu.append(self.noise_cancelation)
        self.indicator.menu.append(self.flight_mode)

    def activate(self, manager):
        super(ParrotZikVersion2Interface, self).activate(manager)
        self._read_noise_cancelation()
        self.flight_mode.set_active(self.parrot.flight_mode)
        self._read_sound_effect_room()
        self._read_sound_effect_angle()
        self.head_detection.set_active(self.parrot.head_detection)

        sound_effect = self.parrot.sound_effect

        self.room_sound_effect_enabled.set_active(sound_effect)
        self.concert_hall_mode.set_sensitive(sound_effect)
        self.jazz_mode.set_sensitive(sound_effect)
        self.living_mode.set_sensitive(sound_effect)
        self.silent_mode.set_sensitive(sound_effect)

        self.angle_30.set_sensitive(sound_effect)
        self.angle_60.set_sensitive(sound_effect)
        self.angle_90.set_sensitive(sound_effect)
        self.angle_120.set_sensitive(sound_effect)
        self.angle_150.set_sensitive(sound_effect)
        self.angle_180.set_sensitive(sound_effect)

        self.noise_cancelation.show()
        self.flight_mode.show()
        self.room_sound_effect.show()
        self.indicator.menu.reposition()

    def deactivate(self):
        self.noise_cancelation.hide()
        self.flight_mode.hide()
        self.room_sound_effect.hide()
        super(ParrotZikVersion2Interface, self).deactivate()

    def toggle_flight_mode(self, widget):
        try:
            self.parrot.flight_mode = self.flight_mode.get_active()
            self.flight_mode.set_active(self.parrot.flight_mode)
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def toggle_room(self, room, widget):
        try:
            if not self.room_dirty:
                self.parrot.room = room
                self.room_dirty = True
                self._read_sound_effect_room()
                self.room_dirty = False
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def _read_sound_effect_room(self):
        active_room = self.parrot.room
        room_to_menuitem_map = (
            (Rooms.CONCERT_HALL, self.concert_hall_mode),
            (Rooms.JAZZ_CLUB, self.jazz_mode),
            (Rooms.LIVING_ROOM, self.living_mode),
            (Rooms.SILENT_ROOM, self.silent_mode),
        )
        for room, menu_item in room_to_menuitem_map:
            menu_item.set_active(room == active_room)

    def toggle_room_sound_effect(self, widget):
        try:
            self.parrot.sound_effect = self.room_sound_effect_enabled.get_active()
            sound_effect = self.parrot.sound_effect
            self.room_sound_effect_enabled.set_active(sound_effect)
            self.concert_hall_mode.set_sensitive(sound_effect)
            self.jazz_mode.set_sensitive(sound_effect)
            self.living_mode.set_sensitive(sound_effect)
            self.silent_mode.set_sensitive(sound_effect)
            self.angle_30.set_sensitive(sound_effect)
            self.angle_60.set_sensitive(sound_effect)
            self.angle_90.set_sensitive(sound_effect)
            self.angle_120.set_sensitive(sound_effect)
            self.angle_150.set_sensitive(sound_effect)
            self.angle_180.set_sensitive(sound_effect)
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def toggle_angle(self, angle, widget):
        try:
            if not self.angle_dirty:
                self.parrot.angle = angle
                self.angle_dirty = True
                self._read_sound_effect_angle()
                self.angle_dirty = False
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def _read_sound_effect_angle(self):
        active_angle = self.parrot.angle
        angle_to_menuitem_map = (
            (30, self.angle_30),
            (60, self.angle_60),
            (90, self.angle_90),
            (120, self.angle_120),
            (150, self.angle_150),
            (180, self.angle_180),
        )
        for angle, menu_item in angle_to_menuitem_map:
            menu_item.set_active(angle == active_angle)

    def toggle_noise_cancelation(self, noise_calcelation, widget):
        try:
            if not self.noise_cancelation_dirty:
                self.parrot.noise_control = noise_calcelation
                self.noise_cancelation_dirty = True
                self._read_noise_cancelation()
                self.noise_cancelation_dirty = False
        except resource_manager.DeviceDisconnected:
            self.deactivate()

    def _read_noise_cancelation(self):
        active_noise_control = self.parrot.noise_control
        noise_control_to_menuitem_map = (
            (NoiseControlTypes.NOISE_CONTROL_MAX, self.noise_control_cancelation_max),
            (NoiseControlTypes.NOISE_CONTROL_ON, self.noise_control_cancelation_on),
            (NoiseControlTypes.NOISE_CONTROL_OFF, self.noise_control_off),
            (NoiseControlTypes.STREET_MODE, self.noise_control_street_mode),
            (NoiseControlTypes.STREET_MODE_MAX, self.noise_control_street_mode_max),
        )
        for noise_control, menu_item in noise_control_to_menuitem_map:
            menu_item.set_active(active_noise_control == noise_control)

    def toggle_head_detection(self, widget):
        try:
            self.parrot.head_detection = self.head_detection.get_active()
            self.head_detection.set_active(self.parrot.head_detection)
        except resource_manager.DeviceDisconnected:
            self.deactivate()
