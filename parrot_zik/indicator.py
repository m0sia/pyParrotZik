#!/usr/bin/env python

import sys
import os
import tempfile

if sys.platform == "linux2" or sys.platform == "win32":
    import gtk
elif sys.platform == "darwin":
    from Foundation import *
    from AppKit import *
    from PyObjCTools import AppHelper
    from status_app_mac import StatusApp


class BaseIndicator(object):
    def __init__(self, icon, menu, statusicon):
        self.menu = menu
        self.statusicon = statusicon
        self.setIcon(icon)

    def gtk_right_click_event(self, icon, button, time):
        if not self.menu_shown:
            self.menu_shown = True
            self.menu.popup(None, None, gtk.status_icon_position_menu,
                            button, time, self.statusicon)
        else:
            self.menu_shown = False
            self.menu.popdown()

    def setIcon(self, name):
        raise NotImplementedError

    def main(self):
        raise NotImplementedError

    def show_about_dialog(self, widget):
        raise NotImplementedError


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


class LinuxIndicator(BaseIndicator):
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


class DarwinIndicator(BaseIndicator):
    def __init__(self, icon, menu):
        self.icon_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])), 'share', 'icons', 'zik')
        statusicon = StatusApp.sharedApplication()
        statusicon.initMenu(menu)
        super(DarwinIndicator, self).__init__(icon, menu, statusicon)

    def setIcon(self, name):
        self.statusicon.setIcon(name, self.icon_directory)

    def main(self):
        AppHelper.runEventLoop()

    def show_about_dialog(self, widget):
        pass


class NSMenu(object):
    def __init__(self):
        self.actions = {}
        self.menubarMenu = NSMenu.alloc().init()
        self.menubarMenu.setAutoenablesItems_(False)

    def append(self, menu_item):
        self.actions[menu_item.title] = menu_item.action
        self.menubarMenu.addItem_(menu_item.nsmenu_item)

    def reposition(self):
        #  TODO
        pass

class GTKMenu(object):
    def __init__(self):
        self.gtk_menu = gtk.Menu()

    def append(self, menu_item):
        self.gtk_menu.append(menu_item.base_item)

    def reposition(self):
        self.gtk_menu.reposition()


class MenuItemBase(object):
    def __init__(self, base_item, sensitive, visible):
        self.base_item = base_item
        self.set_sensitive(sensitive)
        if visible:
            self.show()
        else:
            self.hide()

    def set_sensitive(self, option):
        raise NotImplementedError

    def set_active(self, option):
        raise NotImplementedError

    def get_active(self):
        raise NotImplementedError

    def set_label(self, option):
        raise NotImplementedError

    def show(self):
        self.base_item.show()

    def hide(self):
        self.base_item.hide()

    def set_submenu(self, menu):
        raise NotImplementedError

class GTKMenuItem(MenuItemBase):
    def __init__(self, name, action, sensitive=True, checkitem=False, visible=True):
        if checkitem:
            gtk_item = gtk.CheckMenuItem(name)
        else:
            gtk_item = gtk.MenuItem(name)
        if action:
            gtk_item.connect("activate", action)
        super(GTKMenuItem, self).__init__(gtk_item, sensitive, visible)

    def set_sensitive(self, option):
        return self.base_item.set_sensitive(option)

    def set_active(self, option):
        return self.base_item.set_active(option)

    def get_active(self):
        return self.base_item.get_active()

    def set_label(self, option):
        return self.base_item.set_label(option)

    def set_submenu(self, menu):
        self.base_item.set_submenu(menu.gtk_menu)


class NSMenuItem(MenuItemBase):
    def __init__(self, name, action, sensitive=True, checkitem=False, visible=True):
        self.title = name
        self.action = action
        nsmenu_item = (
            NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                name, 'clicked:', ''))
        super(NSMenuItem, self).__init__(nsmenu_item, sensitive, visible)

    def set_sensitive(self, option):
        self.base_item.setEnabled_(option)

    def set_active(self, option):
        self.base_item.setState_(option)

    def get_active(self):
        return self.base_item.state

    def set_label(self, option):
        self.title = option
        self.base_item.setTitle_(option)

if sys.platform == 'linux2':
    SysIndicator = LinuxIndicator
    Menu = GTKMenu
    MenuItem = GTKMenuItem
elif sys.platform == 'win32':
    SysIndicator = WindowsIndicator
    Menu = GTKMenu
    MenuItem = GTKMenuItem
elif sys.platform == 'darwin':
    SysIndicator = DarwinIndicator
    Menu = NSMenu
    MenuItem = NSMenuItem
else:
    raise Exception('Platform not supported')

if __name__ == "__main__":

    quit_item = MenuItem("Quit", sys.exit, True)

    menu = Menu()
    menu.append(quit_item)

    indicator = SysIndicator(icon="zik-audio-headset", menu=menu)
    indicator.main()
