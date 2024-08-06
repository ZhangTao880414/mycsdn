#! /usr/bin/env python
#coding=utf-8
import os
import time
from ctypes import *

class USBI2C():
    ch341 = windll.LoadLibrary("CH341DLL.dll")
    def __init__(self, usb_dev = 0, i2c_dev = 0x20):
        self.usb_id   = usb_dev
        self.dev_addr = i2c_dev
        if USBI2C.ch341.CH341OpenDevice(self.usb_id) != -1:
            USBI2C.ch341.CH341SetStream(self.usb_id, 0x82)
            USBI2C.ch341.CH341CloseDevice(self.usb_id)
        else:
            print("USB CH341 Open Failed!")

    def read(self):
        if USBI2C.ch341.CH341OpenDevice(self.usb_id) != -1:
            
            rec  = (c_byte * 1)()
            ibuf = (c_byte * 9)()
            rec[0] = self.dev_addr
            
            USBI2C.ch341.CH341StreamI2C(self.usb_id, 1, rec, 9, ibuf)
            USBI2C.ch341.CH341CloseDevice(self.usb_id)
            
            return ibuf
        else:
            print("USB CH341 Open Failed!")
            return 0

    def write(self,cmd,size):
        if USBI2C.ch341.CH341OpenDevice(self.usb_id) != -1:
            tcmd = (c_byte * (size + 1))()
            ibuf = (c_byte * 1)()
            tcmd[0] = self.dev_addr
            
            for i in range (size):
                tcmd[i+1] = cmd[i] & 0xff

            USBI2C.ch341.CH341StreamI2C(self.usb_id, 6, tcmd, 0, ibuf)
            USBI2C.ch341.CH341CloseDevice(self.usb_id)
        else:
            print("USB CH341 Open Failed!")

if __name__ == "__main__":
    cmd = (c_byte * 5)(0x5a,0x05,0x00,0x01,0x60)
    size = sizeof(cmd) 
    while True:
        q = USBI2C()
        q.write(cmd,size)
        rec =q.read()
        dist    =((rec[2]&0xff)+(rec[3]&0xff)*256)
        strengh =((rec[4]&0xff)+(rec[5]&0xff)*256)
        temp    =((rec[6]&0xff)+(rec[7]&0xff)*256)/8-256
        print("Dist:",dist,"Strengh:",strengh,"Temp:",temp)
  
        time.sleep(0.05) #50ms
    
