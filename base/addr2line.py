# -*- coding: utf-8 -*-

a = 0x8F4DEFD  # valgrind报的地址
b = 0x08eea000  # maps文件中模块的基址，注意要在前面加0x

c = a - b
print('%#x' % c)  # 0x63efd

# addr2line -e libapp_frame.so 0x63efd
