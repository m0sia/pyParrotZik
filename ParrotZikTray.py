#!/usr/bin/env python

import sys
import gtk
import re
import os
import ParrotZik

UPDATE_FREQUENCY = 30 # seconds

class ParrotZikIndicator:
    def __init__(self):

        self.menu_setup()      
                
        if sys.platform=="linux2":
            import appindicator
            self.icon_directory = os.path.sep + 'usr' + os.path.sep+ 'share' + os.path.sep+'icons' + os.path.sep+'zik'+ os.path.sep
            self.statusicon = appindicator.Indicator("new-parrotzik-indicator",
                                           "indicator-messages",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
            self.statusicon.set_status(appindicator.STATUS_ACTIVE)
            self.statusicon.set_icon_theme_path(self.icon_directory)            
            self.statusicon.set_menu(self.menu)
        else:
            print "Win32"
            self.icon_directory = os.path.dirname(os.path.realpath(sys.argv[0])) + os.path.sep+ 'share' + os.path.sep+'icons' + os.path.sep+'zik'+ os.path.sep
            self.statusicon = gtk.StatusIcon()            
            self.statusicon.connect("popup-menu", self.gtk_right_click_event)
            self.statusicon.set_tooltip("Parrot Zik")
            self.menu_shown=False            
            sys.stdout = open("debug.log", "w")
            sys.stderr = open("debug.log", "w")
        
        self.setIcon("audio-headset")
        self.connected=False

        self.p = re.compile('90:03:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}')

        return

    def pos(menu, ignore, icon):
        return (Gtk.StatusIcon.position_menu(menu, icon))

    def setIcon(self,   name):
        if sys.platform=="linux2":
            self.statusicon.set_icon(name)
        else:
            self.statusicon.set_from_file(self.icon_directory+name+'.png') 

    def gtk_right_click_event(self, icon, button, time):
        if not self.menu_shown:
            self.menu_shown=True
            self.menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)
        else:
            self.menu_shown=False
            self.menu.popdown()

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

        self.about = gtk.MenuItem()
        self.about.set_label("About")
        self.about.connect("activate", self.show_about_dialog)
        self.about.show()
        self.menu.append(self.about)

        self.quit_item = gtk.MenuItem("Quit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()
        self.menu.append(self.quit_item)

    def ParrotZikMac(self):
        if sys.platform == "linux2":
            out = os.popen("bluez-test-device list").read()
            res = self.p.findall(out)
            if len(res)>0:
                return res[0]
            else:
                return ''          
        else:
            import _winreg
            aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
            aKey = _winreg.OpenKey(aReg, 'SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Devices')
            for i in range(10):
                try:
                    asubkey_name=_winreg.EnumKey(aKey,i)
                    mac =':'.join(asubkey_name[i:i+2] for i in range(0,12,2))
                    res = self.p.findall(mac)
                    if len(res)>0:
                        return res[0]
                    else:
                        return ''
                except EnvironmentError:
                    break


    def EstablishConnection(self):
        if self.connected:
            if not self.parrot.sock:
                print "Lost connection"
                self.connected = False
            else:
                print "Connection already established"
        else:
            mac=self.ParrotZikMac()
            if mac:
                self.parrot = ParrotZik.ParrotZik(mac)
                if not self.parrot.sock:
                    print "Failed to connect to Parrot Zik %s" % mac
                    return False

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
            
            if self.parrot.BatteryCharging:
                self.batteryLevel = "Charging"
                self.setIcon("zik-battery-charging")
                self.batteryLevel="Unknown"
                self.batteryState="Charging"
            elif self.batteryLevel>80:
                self.setIcon("zik-battery-100")
                self.batteryState="In Use"
            elif self.batteryLevel>60:
                self.setIcon("zik-battery-080")
                self.batteryState="In Use"
            elif self.batteryLevel>40:                
                self.setIcon("zik-battery-060")
                self.batteryState="In Use"
            elif self.batteryLevel>20:
                self.setIcon("zik-battery-040")
                self.batteryState="In Use"
            else:
                self.setIcon("zik-battery-low")
                self.batteryState="In Use"

            self.info_item.set_label("Connected to: "+self.name+
                                    "\nFirmware version: "+self.version+
                                    "\nState: "+self.batteryState+
                                    "\nBattery Level: "+str(self.batteryLevel))
        else:
            self.setIcon("zik-audio-headset")
            self.info_item.set_label("Parrot Zik Not connected..")
            self.check.set_sensitive(False)
            self.check2.set_sensitive(False)
        return True

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("Parrot Zik Tray")
        about_dialog.set_version("0.1")
        about_dialog.set_authors(["Dmitry Moiseev m0sia@m0sia.ru"])
        about_dialog.run()
        about_dialog.destroy()

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