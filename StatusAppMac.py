import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

class StatusApp(NSApplication):

    def initMenu(self,menu):
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)

        self.mymenu = menu
        #add menu to statusitem
        self.statusitem.setMenu_(menu.menubarMenu)
        self.statusitem.setToolTip_('Parrot Zik Indicator')

    def setIcon(self,icon,icon_directory):
        self.icon = NSImage.alloc().initByReferencingFile_(icon_directory+icon+'.png')
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((20, 20))
        self.statusitem.setImage_(self.icon)

    def clicked_(self, notification):
        self.mymenu.actions[notification._.title]()
        NSLog('clicked!')