__all__ = ('SysIndicator', 'Menu', 'MenuItem')

import sys

if sys.platform in ['linux', 'linux2']:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--gtk", action="store_true")
    args = parser.parse_args()
    if args.gtk:
        from parrot_zik.indicator.linux import LinuxGtkIndicator as SysIndicator
    else:
        from parrot_zik.indicator.linux import LinuxAppIndicator as SysIndicator
    from parrot_zik.indicator.gtk_wrapping import GTKMenuItem as MenuItem
    from parrot_zik.indicator.gtk_wrapping import GTKMenu as Menu
elif sys.platform in ['win32']:
    from parrot_zik.indicator.windows import WindowsIndicator as SysIndicator
    from parrot_zik.indicator.gtk_wrapping import GTKMenuItem as MenuItem
    from parrot_zik.indicator.gtk_wrapping import GTKMenu as Menu
elif sys.platform == 'darwin':
    from parrot_zik.indicator.mac import DarwinIndicator as SysIndicator
    from parrot_zik.indicator.mac import NSMenuItem as MenuItem
    from parrot_zik.indicator.mac import NSMenu as Menu
else:
    raise Exception('Platform not supported')
