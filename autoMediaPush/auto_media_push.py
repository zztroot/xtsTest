#coding:utf-8

import os
import re
import time

def getDevicesSn():
    device_info = os.popen('adb devices').read()
    com = re.compile('(.*?)\tde.*?')
    SN = re.findall(com, device_info)
    if SN == []:
    	#print("\n**********没有设备连接，请连接设备***********")
        print(no)
    else:
    	return SN

    # for line in device_info.splitlines():
    #     if line == 'List of devices attached':
    #         continue
    #     else:
    #         com = re.compile('(.*?)\tde.*?')
    #         SN = re.findall(com, line)
    #         if SN == []:
    #         	print("\n**********没有设备连接，请连接设备***********")
    #         else:
    #         	for i in SN:
    #             	return i   print("进度:\r{0}%".format(round((i + 1) * 100 / N)), end="") time.sleep(0.01)

def pushMedia(SN_list):
    if len(SN_list) == 5:
        for i in range(5):
            os.system("start cmd /k adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN_list[i]))
    elif len(SN_list) == 4:
        for i in range(4):
            os.system("start cmd /k adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN_list[i]))
    elif len(SN_list) == 3:
        for i in range(3):
            os.system("start cmd /k adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN_list[i]))
    elif len(SN_list) == 2:
        for i in range(2):
            os.system("start cmd /k adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN_list[i]))
    elif len(SN_list) == 6:
    	for i in range(6):
    		os.system("start cmd /k adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN_list[i]))
        
	# index = 0
	# for SN in SN_list:
	# 	#print("\n一共有{}部手机正在PUSH MEDIA请勿拔掉手机\n".format(index))
	# 	# os.popen("adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN))
	# 	index += 1
	# print("\n一共有{}部手机正在PUSH MEDIA请勿拔掉手机\n".format(index))        
	# N = 100000
	# for i in range(N):
	# 	print("\r完成进度:{0}%".format(round((i + 1) * 100 / N)), end="")
	# 	time.sleep(0.01)
	# print("\nPUSH 完成")   

def pushMedia_2(SN_list):
    index = 1
    for SN in SN_list:
        print("\n一共有{}部手机正在PUSH MEDIA请勿拔掉手机\n".format(index))
        os.system("adb -s {} push android-cts-media-1.4 /sdcard/test\n".format(SN))
        
if __name__ == "__main__":
    SN_list = getDevicesSn()
    if len(SN_list) == 1:
        pushMedia_2(SN_list)
    else:
        pushMedia(SN_list)