#!/usr/bin/env python

import sys
import gtk
import appindicator
import imaplib
import re
import os
import ParrotZik

UPDATE_FREQUENCY = 30 # seconds

class ParrotZikIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator("new-parrotzik-indicator",
                                           "indicator-messages",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_icon("audio-headset")
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

        self.check2 = gtk.CheckMenuItem("Auto Connection")
        self.check2.connect("activate", self.toggleAuto)
        self.check2.set_sensitive(False)
        self.check2.show()
        self.menu.append(self.check2)

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
            if not self.findParrotZikMac():
                print "Lost connection"
                self.connected = False
            else:
                print "Connection already established"
        else:
            mac=self.findParrotZikMac()
            if mac:
                self.parrot = ParrotZik.ParrotZik(mac)
                self.connected = True
                self.name = self.parrot.getFriendlyName()
                self.version = self.parrot.getVersion()

                self.check.set_sensitive(True)
                if self.parrot.getNoiseCancel() == "true":
                    self.check.set_active(True)
                else:
                    self.check.set_active(False)

                self.check2.set_sensitive(True)
                if self.parrot.getAutoConnection() == "true":
                    self.check2.set_active(True)
                else:
                    self.check2.set_active(False)

                self.CheckBattery()
        return True

    def toggleANC(self,widget):
        if self.connected:
            if self.check.get_active():
                self.parrot.setNoiseCancel("true")
            else:
                self.parrot.setNoiseCancel("false")

    def toggleAuto(self,widget):
        if self.connected:
            if self.check2.get_active():
                self.parrot.setAutoConnection("true")
            else:
                self.parrot.setAutoConnection("false")

    def CheckBattery(self):
        if self.connected:
            print "Updating battery"
            self.batteryLevel = int(self.parrot.getBatteryLevel())
            self.info_item.set_label("Connected to: "+self.name+
                                    "\nFirmware version: "+self.version+
                                    "\nBattery Level: "+str(self.batteryLevel)+"%")
            if self.batteryLevel==100:
                self.ind.set_icon("battery-100")
            elif self.batteryLevel>80:
                self.ind.set_icon("battery-080")
            elif self.batteryLevel>60:
                self.ind.set_icon("battery-060")
            elif self.batteryLevel>40:
                self.ind.set_icon("battery-040")
            elif self.batteryLevel>20:
                self.ind.set_icon("battery-020")
            else:
                self.ind.set_icon("battery-caution")
        else:
            self.ind.set_icon("audio-headset")
            self.info_item.set_label("Parrot Zik Not connected..")
            self.check.set_sensitive(False)
        return True

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