#!/bin/bash

pip3 install tinydb

sudo ip ad add 192.168.7.191/24 dev enp2s0

sudo python3 nfc_handler.py
