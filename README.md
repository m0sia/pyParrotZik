Parrot Zik Applet
========

## Overview

Parrot Zik is one of the most advanced headphones in the market.
https://www.parrot.com/en/audio/parrot-zik-3

PyParrot Zik is unofficial tool that show Parrot Zik indicator on Windows and Linux.
Thanks to [@serathius](https://github.com/serathius) for Parrot Zik 2.0 support.
Thanks to [@moimadmax](https://github.com/moimadmax) for Parrot Zik 3.0 support.

## Windows Usage

![https://ci.appveyor.com/api/projects/status/7o0v6hy6fqaeulrr?svg=true](https://ci.appveyor.com/api/projects/status/7o0v6hy6fqaeulrr?svg=true)
Latest build(currently doesn't work):
https://ci.appveyor.com/project/m0sia/pyParrotZik/build/artifacts

Outdated version that supports only Zik 1.0:
http://goo.gl/dXij2t  

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

Based on investigation made for pyParrotZik the excellent Parrot-Status tool was developed specially for Mac OS (https://github.com/vincent-le-normand/Parrot-Status)
