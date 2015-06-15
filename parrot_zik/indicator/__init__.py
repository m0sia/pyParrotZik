__all__ = ('SysIndicator', 'Menu', 'MenuItem')

import sys

if sys.platform in ['linux', 'linux2']:
    from parrot_zik.indicator.linux import LinuxIndicator as SysIndicator
    from parrot_zik.indicator.gtk_wrapping import GTKMenuItem as MenuItem
    from parrot_zik.indicator.gtk_wrapping import GTKMenu as Menu
elif sys.platform == 'win32':
    from parrot_zik.indicator.windows import WindowsIndicator as SysIndicator
    from parrot_zik.indicator.gtk_wrapping import GTKMenuItem as MenuItem
    from parrot_zik.indicator.gtk_wrapping import GTKMenu as Menu
elif sys.platform == 'darwin':
    from parrot_zik.indicator.mac import DarwinIndicator as SysIndicator
    from parrot_zik.indicator.mac import NSMenuItem as MenuItem
    from parrot_zik.indicator.mac import NSMenu as Menu
else:
    raise Exception('Platform not supported')
