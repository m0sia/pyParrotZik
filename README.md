Parrot Zik Applet
========

## Overview

Parrot Zik is one of the most advanced headphones in the market.
http://www.parrot.com/zik/usa/technology

Python Parrot Zik and simple unity app indicator applet.
Thanks to [@serathius](https://github.com/serathius) Parrot Zik 2.0 is now supported.

## Screenshots

![ScreenShot](https://dl.dropboxusercontent.com/u/4907241/ParrotZikTray.png "Unity App Indicator Applet")

![ScreenShot](https://dl.dropboxusercontent.com/u/4907241/traywin32.png "Windows tray utility")

## Windows Usage

*Looking for volunteer to make a fresh windows build. Please contact me if you are interested.*

1. Connect Parrot Zik with standard windows GUI
2. Install Parrot Tray Zik
http://goo.gl/dXij2t (outdated version supporting only Zik 1.0)
3. Run ParrotZikTray.exe

## Linux Usage

1. Connect Parrot Zik with standard bluetooth connection
2. Install the applet
   ```
   python setup install
   ```
3. Run the applet
   ```
   parrot_zik_tray
   ```

### Linux Requirement

Python-bluez is needed. On ubuntu based distro run

```
sudo apt-get install python-bluez python-appindicator python-beautifulsoup
```

## Mac OS Usage

Current version of pyParrotZik doesn't support Mac OS(even the core should work on Mac OS). Looking for volunteer to do all the dirty work(mostly GUI).

You can also use excellent Parrot-Status tool developed specially for Mac OS (https://github.com/vincent-le-normand/Parrot-Status)
