#!/usr/bin/env python

import sys
import gtk
import appindicator
import imaplib
import re
import os
import ParrotZik

UPDATE_FREQUENCY = 10 # seconds

class ParrotZikIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator("new-parrotzik-indicator",
                                           "indicator-messages",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon("gtk-info")
        self.menu_setup()
        self.ind.set_menu(self.menu)
        self.connected=False

    def menu_setup(self):
        self.menu = gtk.Menu()

        self.info_item = gtk.MenuItem("Parrot Zik Not connected..")  
        self.info_item.set_sensitive(False)      
        self.info_item.show()
        self.menu.append(self.info_item)

        self.check = gtk.CheckMenuItem("Noise Cancellation")
        self.check.connect("activate", self.toggleANC)
        self.check.set_sensitive(False)
        self.check.show()
        self.menu.append(self.check)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def findParrotZikMac(self):
        out = os.popen("hcitool con").read()
        p = re.compile('90:03:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}')
        res = p.findall(out)
        if len(res)>0:
            return res[0]
        else:
            return ''

    def EstablishConnection(self):
        if self.connected:
            return
        else:
            mac=self.findParrotZikMac()
            if mac:
                self.parrot = ParrotZik.ParrotZik(mac)
                self.connected = True
                self.check.set_sensitive(True)
                if self.parrot.getNoiseCancel() == "true":
                    self.check.set_active(True)
                else:
                    self.check.set_active(False)
                self.CheckBattery()
            else:
                return

    def toggleANC(self,widget):
        if self.connected:
            if self.check.get_active():
                self.parrot.setNoiseCancel("true")
            else:
                self.parrot.setNoiseCancel("false")

    def CheckBattery(self):
        if self.connected:
            self.batteryLevel = self.parrot.getBatteryLevel()
            self.info_item.set_label("Battery "+self.batteryLevel+"%")
            if self.batteryLevel==100:
                self.ind.set_icon("battery-100")
            elif self.batteryLevel>80:
                self.ind.set_icon("battery-80")
            elif self.batteryLevel>60:
                self.ind.set_icon("battery-80")
            elif self.batteryLevel>40:
                self.ind.set_icon("battery-40")
            else:
                self.ind.set_icon("battery-low")
        else:
            self.ind.set_icon("gtk-info")
            self.info_item.set_label("Parrot Zik Not connected..")
            self.check.set_sensitive(False)

    def main(self):
        self.EstablishConnection()
        gtk.timeout_add(UPDATE_FREQUENCY * 1000, self.EstablishConnection)
        gtk.timeout_add(UPDATE_FREQUENCY * 1000, self.CheckBattery)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    indicator = ParrotZikIndicator()
    indicator.main()