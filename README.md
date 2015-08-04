Parrot Zik Api
========

## Overview

Parrot Zik is one of the most advanced headphones in the market.
http://www.parrot.com/zik/usa/technology


Python Parrot Zik and simple unity app indicator applet.

## Windows Usage

1. Connect Parrot Zik with standard windows GUI
2. Install Parrot Tray Zik
http://goo.gl/dXij2t
3. Run ParrotZikTray.exe

## Tray Indicator Applet Usage

1. Connect Parrot Zik with standard bluetooth connection
2. Copy `share/icons/zik` directory to `/usr/share/icons`
3. Run applet `./ParrotZikTray.py`

### Requirement

Python-bluez is needed. On ubuntu based distro run

```
sudo apt-get install python-bluez python-appindicator python-beautifulsoup
```

### Optional

If you want start the manager through the menu or desktop shortcut,
follow the next steps:

1. Copy the `pyParrotZik` directory or its content to `/opt` directory;
2. Create a desktop file in `/usr/share/applications` with the following content:

```
[Desktop Entry]
Version=1.0
Name=Parrot Zik Manager
GenericName=Parrot Zik Manager
X-GNOME-FullName=Parrot Zik Manager
Comment=Manager for Parrot Zik headphones
Exec=/opt/parrot-zik-manager/ParrotZikTray
Icon=/opt/parrot-zik-manager/share/icons/zik/Headphone.ico
Terminal=false
Type=Application
Categories=AudioVideo;
```

## Screenshots

![ScreenShot](https://dl.dropboxusercontent.com/u/4907241/ParrotZikTray.png "Unity App Indicator Applet")

![ScreenShot](https://dl.dropboxusercontent.com/u/4907241/traywin32.png "Windows tray utility")

