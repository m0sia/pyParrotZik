from distutils.core import setup
import glob
import py2exe

setup(
    name = 'parrotziktray',
    description = 'Parrot Zik Tray',
    version = '0.1',

    windows = [
                  {
                      'script': 'ParrotZikTray.py',
                      'icon_resources': [(1, "./icons/Headphone.ico")],
                  }
              ],

    options = {
                  'py2exe': {
                      #'packages':'encodings',
                      # Optionally omit gio, gtk.keysyms, and/or rsvg if you're not using them
                      'includes': 'cairo, pango, pangocairo, atk, gobject, gio, gtk.keysyms, _winreg',
                  }
              },

    data_files=[
    				("icons", glob.glob("icons/*.png"))
                   # If using GTK+'s built in SVG support, uncomment these
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'gdk-pixbuf-query-loaders.exe'),
                   #os.path.join(gtk_base_path, '..', 'runtime', 'bin', 'libxml2-2.dll'),
               ]
)