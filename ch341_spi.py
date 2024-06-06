作者：CoderMoney
链接：https://www.zhihu.com/question/598249040/answer/3005317549
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

import ctypes

# 加载CH341的DLL文件
ch341 = ctypes.CDLL('CH341DLL.DLL')

# 定义SPI读写函数
def spi_transfer(data):
    # 选择芯片
    ch341.CH341SetStream(0x5A, 0x00)

    # 发送数据
    out_data = ctypes.create_string_buffer(data)
    ch341.CH341StreamSPI3(0, 0, len(out_data), out_data)

    # 释放芯片
    ch341.CH341SetStream(0x00, 0x00)

    # 返回读取的数据
    in_data = ctypes.create_string_buffer(len(out_data))
    ch341.CH341StreamSPI3(0, 0, len(in_data), in_data)
    return in_data.raw

# 测试代码
data_out = b'\x01\x02\x03\x04'
data_in = spi_transfer(data_out)
print(data_in)