import gtk

from parrot_zik.indicator.base import MenuItemBase


class GTKMenu(object):
    def __init__(self):
        self.gtk_menu = gtk.Menu()

    def append(self, menu_item):
        self.gtk_menu.append(menu_item.base_item)

    def reposition(self):
        self.gtk_menu.reposition()


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
