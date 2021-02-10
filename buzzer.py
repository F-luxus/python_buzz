#!/usr/bin/python
# -*- coding: utf-8 -*-

# PS2 Buzz! Controller library

import usb.core
import usb.util
import traceback
import sys
import os
import time
import pyglet
import usb.backend.libusb1
import json
with open('includes/strings.json', 'r', encoding='utf-8') as f:
    datastore = json.load(f)
    

class buzz:
    
    def __init__(self):

    # ID 054c:1000 Sony Corp. Wireless Buzz! Receiver
        backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
        self.device = usb.core.find(backend=backend, idVendor=0x054c, idProduct=0x1000)
        if self.device is None:
            print(datastore["CONNECT_STATUS"])
            while self.device is None:
                self.device = usb.core.find(backend=backend, idVendor=0x054c, idProduct=0x1000)
                time.sleep(4)
                
        self.interface = 0
        self.lights = [0, 0, 0, 0]
        self.buttons = [{
            'red': 0,
            'yellow': 0,
            'green': 0,
            'orange': 0,
            'blue': 0,
            }, {
            'red': 0,
            'yellow': 0,
            'green': 0,
            'orange': 0,
            'blue': 0,
            }, {
            'red': 0,
            'yellow': 0,
            'green': 0,
            'orange': 0,
            'blue': 0,
            }, {
            'red': 0,
            'yellow': 0,
            'green': 0,
            'orange': 0,
            'blue': 0,
            }]
        self.bits = 0




        self.device.set_configuration()
        usb.util.claim_interface(self.device, self.interface)
        cfg = self.device.get_active_configuration()
        self.endpoint = cfg[(0, 0)][0]

        
    def devicestatus(self):
    # ID 054c:1000 Sony Corp. Wireless Buzz! Receiver
        backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
        self.device = usb.core.find(backend=backend, idVendor=0x054c, idProduct=0x1000)
        
        return self.device

        
    def setlights(self, control):

    # Sets lights based on binaray
    # 1 = Controller 1
    # 2 = Controller 2
    # 4 = Controller 3
    # 8 = Controller 4

        self.lights[0] = (0xFF if control & 1 else 0)
        self.lights[1] = (0xFF if control & 2 else 0)
        self.lights[2] = (0xFF if control & 4 else 0)
        self.lights[3] = (0xFF if control & 8 else 0)
        self.device.ctrl_transfer(0x21, 0x09, 0x0200, 0, [
            0,
            self.lights[0],
            self.lights[1],
            self.lights[2],
            self.lights[3],
            0,
            0,
            ])

    def setlight(self, controller, state=False):

    # Sets a light on or off for a single controller

        self.lights[controller] = (0xFF if state else 0)
        self.device.ctrl_transfer(0x21, 0x09, 0x0200, 0, [
            0,
            self.lights[0],
            self.lights[1],
            self.lights[2],
            self.lights[3],
            0,
            0,
            ])

    def fliplight(self, controller):

    # Flips the state of a controllers light
    # TODO

        pass

    def readcontroller(self, raw=False, timeout=1000):

    # Reads the controller
    # Returns the result of Parsecontroller (the changed bit) or raw

        try:
            cfg = self.device.get_active_configuration()
            self.endpoint = cfg[(0, 0)][0]
            data = self.device.read(self.endpoint.bEndpointAddress,
                                    self.endpoint.wMaxPacketSize,
                                    timeout=timeout)
            parsed = self.parsecontroller(data)
        except usb.core.USBError as e:
        
                #if (e): print ("Laukiama mygtuko")
                data = None
        if data != None and raw == False:
            data = parsed
        return data

    def parsecontroller(self, data):

    # Function to parse the results of readcontroller
    # We break this out incase someone else wants todo something different
    # Returns the changed bits

    # Controller 1

        self.buttons[0]['red'] = (True if data[2] & 1 else False)
        self.buttons[0]['yellow'] = (True if data[2] & 2 else False)
        self.buttons[0]['green'] = (True if data[2] & 4 else False)
        self.buttons[0]['orange'] = (True if data[2] & 8 else False)
        self.buttons[0]['blue'] = (True if data[2] & 16 else False)

    # Controller 2

        self.buttons[1]['red'] = (True if data[2] & 32 else False)
        self.buttons[1]['yellow'] = (True if data[2] & 64 else False)
        self.buttons[1]['green'] = (True if data[2] & 128 else False)
        self.buttons[1]['orange'] = (True if data[3] & 1 else False)
        self.buttons[1]['blue'] = (True if data[3] & 2 else False)

    # Controller 3

        self.buttons[2]['red'] = (True if data[3] & 4 else False)
        self.buttons[2]['yellow'] = (True if data[3] & 8 else False)
        self.buttons[2]['green'] = (True if data[3] & 16 else False)
        self.buttons[2]['orange'] = (True if data[3] & 32 else False)
        self.buttons[2]['blue'] = (True if data[3] & 64 else False)

    # Controller 4

        self.buttons[3]['red'] = (True if data[3] & 128 else False)
        self.buttons[3]['yellow'] = (True if data[4] & 1 else False)
        self.buttons[3]['green'] = (True if data[4] & 2 else False)
        self.buttons[3]['orange'] = (True if data[4] & 4 else False)
        self.buttons[3]['blue'] = (True if data[4] & 8 else False)

        oldbits = self.bits
        self.bits = (data[4] << 16) + (data[3] << 8) + data[2]

        changed = oldbits | self.bits

        return changed

    def getbuttons(self):

    # Returns current state of buttons

        return self.buttons

    def getlights(self):

    # Returns the current state of the lights

        return self.lights


if __name__ == '__main__':
    buzz = buzz()

#    for x in range(16):
# ....buzz.setlights(x)
# ....time.sleep(1)
        
    def efektai():

        for x in range(0, 12):
            buzz.setlights(8)
            time.sleep(0.05)
            buzz.setlights(4)
            time.sleep(0.05)
            buzz.setlights(2)
            time.sleep(0.05)
            buzz.setlights(1)
            time.sleep(0.05)
        buzz.setlights(0)

    intro = pyglet.media.StaticSource(pyglet.media.load('includes/audio.mp3'))
    intro.play()

    checked = pyglet.media.StaticSource(pyglet.media.load('includes/check.mp3'))
    button  = pyglet.media.StaticSource(pyglet.media.load('includes/check.mp3'))
    noanswer  = pyglet.media.StaticSource(pyglet.media.load('includes/noanswer.mp3'))
    error  = pyglet.media.StaticSource(pyglet.media.load('includes/error.mp3'))
    efektai()
    pirma =0;
    antra =0;
    trecia =0;
    atsakymas =1;
    paspaude =0;
    atsakymas1 =0;
    atsakymas2 =0;
    atsakymas3 =0;
    teisingas = 0;
    
        
    while True:
        r = buzz.readcontroller(timeout=20)
        if buzz.devicestatus() is None:
            sys.exit(datastore["DISCONNECTED"])

        if r != None:
            if buzz.buttons[3]['blue']: atsakymas="melynas"; print(datastore["BLUE_ANSWER_TEXT"]);
            if buzz.buttons[3]['orange']: atsakymas="oranzinis"; print(datastore["ORANGE_ANSWER_TEXT"]);
            if buzz.buttons[3]['green']: atsakymas="zalias"; print(datastore["GREEN_ANSWER_TEXT"]);
            if buzz.buttons[3]['yellow']: atsakymas="geltonas"; print(datastore["YELLOW_ANSWER_TEXT"]);
            
            if buzz.buttons[0]['red'] == True and paspaude !=1:
                button.play();
                buzz.setlights(1);
                print(datastore["FIRST_TEAM"]);
                time.sleep(5);
                paspaude =1
            if buzz.buttons[1]['red'] == True and paspaude !=1:
                button.play();buzz.setlights(2);
                print(datastore["SECOND_TEAM"]);
                time.sleep(5);
                paspaude =1

            if buzz.buttons[2]['red'] == True and paspaude !=1:
                button.play();
                buzz.setlights(4);
                print(datastore["THIRTH_TEAM"]);
                time.sleep(5);
                paspaude =1

   
  

            
            if pirma == 0:
                if buzz.buttons[0]['blue']: pirma=1; checked.play(); print(datastore["I_TEAM_BLUE"]); atsakymas1 ="melynas"; teisingas=2;
                if buzz.buttons[0]['orange']: pirma=1; checked.play(); print(datastore["I_TEAM_ORANGE"]);atsakymas1 ="oranzinis"; teisingas=2;
                if buzz.buttons[0]['green']: pirma=1; checked.play(); print(datastore["I_TEAM_GREEN"]);atsakymas1 ="zalias"; teisingas=2;
                if buzz.buttons[0]['yellow']: pirma=1; checked.play(); print(datastore["I_TEAM_YELLOW"]);atsakymas1 ="geltonas"; teisingas=2;

            if antra == 0:
                if buzz.buttons[1]['blue']: antra =1; checked.play(); print(datastore["II_TEAM_BLUE"]);atsakymas2 ="melynas"; teisingas=2;
                if buzz.buttons[1]['orange']: antra =1; checked.play(); print(datastore["II_TEAM_ORANGE"]);atsakymas2 ="oranzinis"; teisingas=2;
                if buzz.buttons[1]['green']: antra =1; checked.play(); print(datastore["II_TEAM_GREEN"]);atsakymas2 ="zalias"; teisingas=2;
                if buzz.buttons[1]['yellow']: antra =1; checked.play(); print(datastore["II_TEAM_YELLOW"]);atsakymas2 ="geltonas";teisingas=2;
            
            if trecia == 0:
                if buzz.buttons[2]['blue']: trecia =1;checked.play(); print(datastore["III_TEAM_BLUE"]);atsakymas3 ="melynas";teisingas=2;
                if buzz.buttons[2]['orange']: trecia =1; checked.play(); print(datastore["III_TEAM_ORANGE"]);atsakymas3 ="oranzinis"; teisingas=2;
                if buzz.buttons[2]['green']: trecia =1; checked.play(); print(datastore["III_TEAM_GREEN"]);atsakymas3 ="zalias";teisingas=2;
                if buzz.buttons[2]['yellow']: trecia =1; checked.play(); print(datastore["III_TEAM_YELLOW"]);atsakymas3 ="geltonas";teisingas=2;
# ....     IV pultelis skirtas valdyti kitus pultelius
            if buzz.buttons[3]['red'] == True:
                if pirma==1 and atsakymas==1: error.play();
                else:
                    if atsakymas == atsakymas1:
                        time.sleep(0.200);
                        button.play();
                        print(datastore["I_TEAM_YELLOW_CORRECT"] ,atsakymas)
                        buzz.setlight(0,True);
                        teisingas = 1;
      
                    if atsakymas == atsakymas2:
                        time.sleep(0.200);
                        button.play();
                        print(datastore["II_TEAM_YELLOW_CORRECT"],atsakymas)
                        buzz.setlight(1,True);
                        teisingas = 1;
                        
                    if atsakymas == atsakymas3:
                        time.sleep(0.200);
                        button.play();
                        print(datastore["III_TEAM_YELLOW_CORRECT"],atsakymas)
                        buzz.setlight(2,True);
                        teisingas = 1;
                    if teisingas ==2: noanswer.play();time.sleep(2); teisingas=0;
                    if teisingas ==1: time.sleep(10); teisingas=0;
                    
                    intro.play()
                    efektai();
                    paspaude=0;
                    pirma =0;
                    antra =0;
                    trecia =0;
                    atsakymas = 1;
                    atsakymas1 =0;
                    atsakymas2 =0;
                    atsakymas3 =0;
 
# ....     IV pultelis skirtas valdyti kitus pultelius            
# ....    print buzz.getbuttons()

			
