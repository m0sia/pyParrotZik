__all__ = ('SysIndicator', 'Menu', 'MenuItem')

import sys

if sys.platform == 'linux2':
    import linux
    import gtk_wrapping
    SysIndicator = linux.LinuxIndicator
    Menu = gtk_wrapping.GTKMenu
    MenuItem = gtk_wrapping.GTKMenuItem
elif sys.platform == 'win32':
    import gtk_wrapping
    import windows
    SysIndicator = windows.WindowsIndicator
    Menu = gtk_wrapping.GTKMenu
    MenuItem = gtk_wrapping.GTKMenuItem
elif sys.platform == 'darwin':
    import mac
    SysIndicator = mac.DarwinIndicator
    Menu = mac.NSMenu
    MenuItem = mac.NSMenuItem
else:
    raise Exception('Platform not supported')
