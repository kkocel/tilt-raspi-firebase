#!/usr/bin/env python
# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import datetime

import bluetooth._bluetooth as bluez

def print_beacons():
    dev_id = 0
    try:
        sock = bluez.hci_open_dev(dev_id)

    except:
        print ("error accessing bluetooth device...");
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    return blescan.parse_events(sock, 20)
	
def extract_temp_and_sg():
    beacons = print_beacons()	
	
    for beacon in beacons:
        temp_and_sg = beacon.split(",")[2:4]

        # check if we are dealing with valid measurements of sg
        if int(temp_and_sg[1]) > 900 and int(temp_and_sg[1]) < 1200:
            return temp_and_sg