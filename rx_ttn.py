#!/usr/bin/env python3
from time import sleep
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import LoRaWAN
import time
BOARD.setup()
parser = LoRaArgumentParser("LoRaWAN receiver")
from packer import *

class LoRaWANrcv(LoRa):
    def __init__(self, verbose = False):
        super(LoRaWANrcv, self).__init__(verbose)

    def on_rx_done(self):
        print("RxDone")

        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])
        # for c in payload:
        #     print('%02x' % c)
        print("Time:", str(time.ctime()))
        print("Rawinput:", payload)
        try:
            temp=payload[3]<<8 | payload[2]
            humd=payload[5]<<8 | payload[4]
            co2=payload[7]<<8 | payload[6]
            pm25=payload[9]<<8 | payload[8]
            result={'temp':temp,'humd':humd,'co2':co2,'pm25':pm25}
            print(result)

        except:
            print("cannot parse data")
        # print "Receive:", data
        lorawan = LoRaWAN.new(nwskey, appskey)
        # lorawan.read(payload)
        # print(lorawan.get_mhdr().get_mversion())
        # print(lorawan.get_mhdr().get_mtype())
        # print(lorawan.get_mic())
        # print(lorawan.compute_mic())
        # print(lorawan.valid_mic())
        # print("".join(list(map(chr, lorawan.get_payload()))))
        # print("\n")

        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)


# Init
nwskey = [0xC3, 0x24, 0x64, 0x98, 0xDE, 0x56, 0x5D, 0x8C, 0x55, 0x88, 0x7C, 0x05, 0x86, 0xF9, 0x82, 0x26]
appskey = [0x15, 0xF6, 0xF4, 0xD4, 0x2A, 0x95, 0xB0, 0x97, 0x53, 0x27, 0xB7, 0xC1, 0x45, 0x6E, 0xC5, 0x45]
lora = LoRaWANrcv(False)

# Setup
lora.set_mode(MODE.STDBY)
print('mode:',lora.get_mode())
lora.set_rx_crc(True)
print('init')
# lora.set_pa_config(pa_select=0,max_power=0xFF,output_power=0xFF)
lora.set_pa_dac(False)
lora.set_hop_period(0xff)
lora.set_dio_mapping_1(0x01)
lora.set_coding_rate(1)
lora.set_freq(434)
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
assert(lora.get_agc_auto_on() == 1)

try:
    print("Waiting for incoming LoRaWAN messages\n")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("\nKeyboardInterrupt")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
