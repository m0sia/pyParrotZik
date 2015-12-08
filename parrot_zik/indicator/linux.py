import os

import gtk

from parrot_zik.indicator.base import BaseIndicator


class LinuxIndicator(BaseIndicator):
    def __init__(self, icon, menu, statusicon):
        super(LinuxIndicator, self).__init__(icon, menu, statusicon)

    def gtk_right_click_event(self, icon, button, time):
        if not self.menu_shown:
            self.menu_shown = True
            self.menu.popup(None, None, gtk.status_icon_position_menu,
                            button, time, self.statusicon)
        else:
            self.menu_shown = False
            self.menu.poVpdown()

    @classmethod
    def main(cls):
        gtk.main()

    def quit(self, _):
        gtk.main_quit()

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Parrot Zik Tray")
        about_dialog.set_version("0.3")
        about_dialog.set_authors(["Dmitry Moiseev m0sia@m0sia.ru"])
        about_dialog.run()
        about_dialog.destroy()


class LinuxAppIndicator(LinuxIndicator):
    def __init__(self, icon, menu):
        import appindicator
        self.icon_directory = os.path.join('/', 'usr', 'share', 'icons', 'zik')
        if not os.path.isdir(self.icon_directory):
            self.icon_directory = os.path.join('share', 'icons', 'zik')
        statusicon = appindicator.Indicator(
            "new-parrotzik-indicator", "indicator-messages",
            appindicator.CATEGORY_APPLICATION_STATUS)
        statusicon.set_status(appindicator.STATUS_ACTIVE)
        statusicon.set_icon_theme_path(self.icon_directory)
        statusicon.set_menu(menu.gtk_menu)
        super(LinuxIndicator, self).__init__(icon, menu, statusicon)

    def setIcon(self, name):
        self.statusicon.set_icon(name)



class LinuxGtkIndicator(LinuxIndicator):
    def __init__(self, icon, menu):
        self.icon_directory = os.path.join(
            '/usr', 'share', 'icons/')
        self.menu_shown = False
        statusicon = gtk.StatusIcon()
        statusicon.connect("popup-menu", self.gtk_right_click_event)
        statusicon.set_tooltip("Parrot Zik")
        super(LinuxIndicator, self).__init__(icon, menu, statusicon)

    def setIcon(self, name):
        self.statusicon.set_from_file(self.icon_directory + name + '.png')

