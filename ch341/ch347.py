'''
Author: OIDCAT
Date: 2022-07-13 15:22:17
LastEditTime: 2022-08-23 19:19:23
此处需注意Python版本位数与DLL是否匹配
'''
 
 #! /usr/bin/env python
 #coding=utf-8
import ctypes
import os
from ctypes import *
 
# 
print("进入程序")
CH347 = windll.LoadLibrary("./CH347DLL.DLL")
DevIndex = 0
I2C_addr = 0xA0
class spi_config(Structure):
        _fields_ = [
            ("iMode", c_ubyte),
            ("iClock", c_ubyte),
            ("iByteOrder", c_ubyte),
            ("iSpiWriteReadInterval", c_ushort),
            ("iSpiOutDefaultData",c_ubyte),
            ("iChipSelect", c_ulong),
            ("CS1Polarity",c_ubyte),  
            ("CS2Polarity", c_ubyte), 
            ("iIsAutoDeativeCS", c_ushort), 
            ("iActiveDelay", c_ushort), 
            ("iDelayDeactive", c_ulong),
        ]
 
def init():
    if CH347.CH347OpenDevice(DevIndex) != -1:
        print("CH347 Open succeeded")
        CH347.CH347I2C_Set(DevIndex, 3)
 
        CH347_SPI = spi_config()
        CH347_SPI.iMode = 0x03
        CH347_SPI.iClock = 0x01
        CH347_SPI.iByteOrder = 0x01
        CH347_SPI.iSpiOutDefaultData = 0xff 
        CH347_SPI.iChipSelect = 0x80
        CH347.CH347SPI_Init(DevIndex, CH347_SPI)
        # CH347.CH347CloseDevice(DevIndex)
    else:
        print("Open The CH347 Failed")
            
def read(addr):
    if CH347.CH347OpenDevice(DevIndex) != -1:
        oBuf = (c_byte *2)()
        iBuf = (c_byte *1)()
        oBuf[0] = 0xA0
        oBuf[1] = addr
        CH347.CH347StreamI2C(DevIndex, 2, oBuf, 1, iBuf)
        CH347.CH347CloseDevice(DevIndex)
        print("CH347 read succeeded")
        return iBuf[0] & 0xFF
    else:
        print("CH347I2C.CH347OpenDevice")
        return 0
 
def spi_readId(DevIndex):
    cmd_buf = (c_byte * 4)()
    len = 4
    cmd_buf[0] = 0x9F
    cmd_buf[1] = 0xFF
    cmd_buf[2] = 0xFF
    cmd_buf[3] = 0xFF
    
    CH347.CH347SPI_WriteRead(DevIndex, 0x80, len, cmd_buf)
    print("{0:x} {1:x} {2:x} {3:x}".format(cmd_buf[0], cmd_buf[1], cmd_buf[2], cmd_buf[3]))
    return cmd_buf[0] & 0xFF
 
if __name__ == "__main__":
    print("CH347 Test")
    init()
    read(0x02)
    spi_readId(DevIndex)