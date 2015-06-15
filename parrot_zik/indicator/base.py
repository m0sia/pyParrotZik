class BaseIndicator(object):
    def __init__(self, icon, menu, statusicon):
        self.menu = menu
        self.statusicon = statusicon
        self.setIcon(icon)

    def setIcon(self, name):
        raise NotImplementedError

    def main(self):
        raise NotImplementedError

    def show_about_dialog(self, widget):
        raise NotImplementedError

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
