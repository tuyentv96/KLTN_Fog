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
import time
import json
import sys
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from packer import *

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self._id = "GW_01"

    def on_rx_done(self):
        print '----------------------------------'
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])
        print "Time:", str(time.ctime())
        print "Rawinput:", payload
        # try:
        #     _length, _data = packer.Unpack_Str(data)
        #     print "Time:", str(time.ctime())
        #     print "Length:", _length
        #     print "Receive:", _data
        # except:
        #     print "Non-hexadecimal digit found..."
        print "Receive:", data
        self.set_mode(MODE.RXCONT)


    def start(self):
        print 'start to receive...'
        self.reset_ptr_rx()
        # self.set_mode(0x8d)
        self.set_mode(MODE.RXCONT)

        while True:
            # print(lora.get_rx_nb_bytes())
            # print(lora.get_hop_channel())
            # payload = self.read_payload(nocheck=True)
            # rssi_value = self.get_rssi_value()
            # status = self.get_modem_status()
            # sys.stdout.flush()
            # print('mode:','%02x' % lora.get_mode())
            # data = ''.join([chr(c) for c in payload])
            # print "Time:", str(time.ctime())
            # print "Rawinput:", payload
    
            # try:
            #     _length, _data = packer.Unpack_Str(data)
            #     print "Time:", str(time.ctime())
            #     print "Length:", _length
            #     print "Receive:", _data
            # except:
            #     print "Non-hexadecimal digit found..."
            #     print "Receive:", data
            # # self.set_mode(MODE.SLEEP)
            # self.clear_irq_flags(RxDone=1)
            # print('irg flag:',self.get_irq_flags())
            # print(lora.get_hop_period())
            # print('lna:',lora.get_lna())
            # print(lora.get_modem_config_1())
            # print(lora.get_modem_config_2())
            # print(lora.get_modem_config_3())
            # print(lora.get_symb_timeout())
            # print('ocp:',lora.get_ocp())
            # print('paramp:',lora.get_pa_ramp())
            # # self.set_mode(0x8d)
            # #self.set_mode(MODE.RXCONT)
            # lora.get_all_registers()
            # self.clear_irq_flags(RxDone=1)
            sleep(1)


#
# initialize sx1278
# 
BOARD.setup()

lora = LoRaRcvCont()
lora.set_mode(MODE.STDBY)
print('mode:',lora.get_mode())
lora.set_rx_crc(True)
print('init')
# lora.set_pa_config(pa_select=0,max_power=0xFF,output_power=0xFF)
lora.set_pa_dac(False)
lora.set_hop_period(0xff)
lora.set_dio_mapping_1(0x01)
lora.set_coding_rate(1)
lora.set_freq(433)
lora.set_spreading_factor(12)  # 7-12
lora.set_bw(7)  # 0-9 
lora.clear_irq_flags(RxDone=1)
lora.set_lna_gain(GAIN.G1)
lora.set_implicit_header_mode(False)
lora.set_low_data_rate_optim(False)
lora.set_agc_auto_on(True)
lora.set_lna(lna_boost_hf=0b11)
lora.set_sync_word(0x12)
lora.set_payload_length(0x10)
# lora.set_max_payload_length(0xff)
# lora.set_preamble(0x0c)
lora.set_pa_paconfigmy(0xf6)
lora.set_symb_timeout(0x3ff)
lora.set_preamble(0x0c)
lora.set_irq_flags_mask(crc_error=True,valid_header=True,tx_done=True,cad_done=True,fhss_change_ch=True,cad_detected=True)
print(lora)
try: 
    lora.start()
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()                    
    print "exit()"

