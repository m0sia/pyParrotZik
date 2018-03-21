import glob
import sys

if sys.platform == "win32":
    import py2exe
    from distutils.core import setup
else:
    from setuptools import setup


setup(
    name='parrotziktray',
    description='Parrot Zik Tray Indicator',
    author="Dmitry Moiseev",
    author_email="m0sia@m0sia.ru",
    maintainer_email="m0sia@m0sia.ru",
    url="https://github.com/m0sia/pyParrotZik",
    license="'GPLv2+'",
    version='0.3',

    windows=[
        {
            'script': 'parrot_zik/parrot_zik_tray.py',
            'icon_resources': [(1, "./share/icons/zik/Headphone.ico")],
        }
    ],

    options={
        'py2exe': {
            #'packages':'encodings',
            # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
            'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, _winreg',
        }
    },
   
    data_files=[
        ("share/icons/zik", glob.glob("share/icons/zik/*.png"))
            # If using GTK+'s built in SVG support, uncomment these
            #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
            #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
    ],

    install_requires=[
        'beautifulsoup4', 'pybluez'
    ],

    packages=['parrot_zik', 'parrot_zik.interface', 'parrot_zik.indicator', 'parrot_zik.model'],
    entry_points={
        'console_scripts': [
            'parrot_zik_tray=parrot_zik.parrot_zik_tray:ParrotZikIndicator.main',
        ]
    },
    include_package_data=True,
)
