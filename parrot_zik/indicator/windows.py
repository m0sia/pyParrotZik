import sys
import tempfile
import gtk
import os

from .base import BaseIndicator


class WindowsIndicator(BaseIndicator):
    def __init__(self, icon, menu):
        self.icon_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])), 'share', 'icons', 'zik')
        self.menu_shown = False
        sys.stdout = open(os.path.join(tempfile.gettempdir(), "zik_tray_stdout.log", "w"))
        sys.stderr = open(os.path.join(tempfile.gettempdir(), "zik_tray_stderr.log", "w"))
        statusicon = gtk.StatusIcon()
        statusicon.connect("popup-menu", self.gtk_right_click_event)
        statusicon.set_tooltip("Parrot Zik")
        super(WindowsIndicator, self).__init__(icon, menu, statusicon)

    def gtk_right_click_event(self, icon, button, time):
        if not self.menu_shown:
            self.menu_shown = True
            self.menu.popup(None, None, gtk.status_icon_position_menu,
                            button, time, self.statusicon)
        else:
            self.menu_shown = False
            self.menu.poVpdown()

    def setIcon(self, name):
        self.statusicon.set_from_file(self.icon_directory + name + '.png')

    def main(self):
        gtk.main()

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Parrot Zik Tray")
        about_dialog.set_version("0.3")
        about_dialog.set_authors(["Dmitry Moiseev m0sia@m0sia.ru"])
        about_dialog.run()
        about_dialog.destroy()
