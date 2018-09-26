#!/usr/bin/env python

""" A simple continuous receiver class. """

# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.

from time import sleep
import json
import time
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD

class LoRaBeacon(LoRa):
    def __init__(self, verbose=False):
        super(LoRaBeacon, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self._id = "NODE_01"
        self.rx_done = False

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])
        print "Receive:", data 

        self.set_mode(MODE.SLEEP)
        #self.reset_ptr_rx()
        #self.set_mode(MODE.RXCONT)
        self.rx_done = True


    def start(self):
        while True:
            print '----------------------------------'    

            self.set_mode(MODE.STDBY)
            self.clear_irq_flags(TxDone=1)

            _payload ="123456"            
            data = [int(hex(ord(c)), 0) for c in _payload]
            print "data", _payload
            print "Rawinput:", data

            sleep(1)
            self.write_payload(data)                                       
            self.set_mode(MODE.TX)
            sleep(1)



#    
# initialize sx1278
#    
BOARD.setup()

sf = 8
bw = 3
cr = 1
t = sf * bw * cr

lora = LoRaBeacon()
lora.set_mode(MODE.SLEEP)
lora.set_pa_config(pa_select=1)
lora.set_freq(433)
lora.set_spreading_factor(sf)  # 7-12
lora.set_bw(bw)  # 0-9
lora.set_coding_rate(cr)  # 1-4
lora.clear_irq_flags(TxDone=1)
lora.set_agc_auto_on(True)
lora.set_lna_gain(GAIN.NOT_USED)
lora.set_implicit_header_mode(False)
lora.set_pa_config(max_power=0x04, output_power=0x0F)
print(lora)

try:
    lora.start()
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
    print "exit()"
