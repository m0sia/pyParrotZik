import os
import sys

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

from parrot_zik.indicator.base import BaseIndicator
from parrot_zik.indicator.base import MenuItemBase
from parrot_zik.status_app_mac import StatusApp


class DarwinIndicator(BaseIndicator):
    def __init__(self, icon, menu):
        self.icon_directory = os.path.join(
            os.path.dirname(os.path.realpath(sys.argv[0])), 'share', 'icons', 'zik')
        statusicon = StatusApp.sharedApplication()
        statusicon.initMenu(menu)
        super(DarwinIndicator, self).__init__(icon, menu, statusicon)

    def setIcon(self, name):
        self.statusicon.setIcon(name, self.icon_directory)

    @classmethod
    def main(cls):
        AppHelper.runEventLoop()

    def show_about_dialog(self, widget):
        pass

    def quit(self, _):
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
