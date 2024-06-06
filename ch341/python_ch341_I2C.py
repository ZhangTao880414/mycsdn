#! /usr/bin/env python
#coding=utf-8
import os
import time
from ctypes import *

class USBI2C():
    ch341 = windll.LoadLibrary("CH341DLL.dll")
    def __init__(self, usb_dev = 0, i2c_dev = 0x5c):
        self.usb_id   = usb_dev
        self.dev_addr = i2c_dev
        if USBI2C.ch341.CH341OpenDevice(self.usb_id) != -1:
            USBI2C.ch341.CH341SetStream(self.usb_id, 0x82)
            USBI2C.ch341.CH341CloseDevice(self.usb_id)
        else:
            print("USB CH341 Open Failed!")

    def read(self, addr):
        if USBI2C.ch341.CH341OpenDevice(self.usb_id) != -1:
            obuf = (c_byte * 2)()
            ibuf = (c_byte * 1)()
            obuf[0] = self.dev_addr
            obuf[1] = addr
            USBI2C.ch341.CH341StreamI2C(self.usb_id, 2, obuf, 1, ibuf)
            USBI2C.ch341.CH341CloseDevice(self.usb_id)
            return ibuf[0] & 0xff
        else:
            print("USB CH341 Open Failed!")
            return 0

    def write(self, addr, dat):
        if USBI2C.ch341.CH341OpenDevice(self.usb_id) != -1:
            obuf = (c_byte * 3)()
            ibuf = (c_byte * 1)()
            obuf[0] = self.dev_addr
            obuf[1] = addr
            obuf[2] = dat & 0xff
            USBI2C.ch341.CH341StreamI2C(self.usb_id, 3, obuf, 0, ibuf)
            USBI2C.ch341.CH341CloseDevice(self.usb_id)
        else:
            print("USB CH341 Open Failed!")