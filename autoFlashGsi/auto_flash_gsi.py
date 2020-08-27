#coding:utf-8
#--zhongtian--

import os 
import time
import sys
import re
from colorama import init
 
init(autoreset=True)
a = sys.argv[1]
try:
	boot = sys.argv[2]
except:
	boot = " "

def getSecurityPatch(sn):
	Security = os.popen("adb -s {} shell getprop ro.vendor.build.security_patch".format(sn)).read()
                        #2020-05-01
	com = re.compile(".*?-(.*?)-.*?")
	new_security = re.findall(com, Security)
	for i in new_security:
		system_path = i + "\\system.img"
		return system_path

def flashGsi(a, boot, sn, s, system):
	os.system("adb -s {} reboot bootloader".format(sn))
	time.sleep(1)
	if a == "vts":
		os.system("fastboot flash boot {}".format(boot))
		time.sleep(1)
		os.system("fastboot -w")
	else:
		os.system("fastboot -w")
	time.sleep(1)
	os.system("fastboot reboot fastboot")
	time.sleep(2)
	os.system("fastboot flash system {}".format(system))
	time.sleep(5)
	os.system("fastboot reboot")
	print("\n")
	#output = '*'*int((s/2-37)) + "\033[0;32;40m\t{}：此设备刷GSI成功，正在重启中\033[0m".format(sn) + '*'*int((s/2-37))
	print("#####\033[0;32;40m{}:此设备刷GSI成功,正在重启中\033[0m#####".format(sn).center(s, '*'))
	#print(output)

def getDevicesSn():
    SN_list = []
    device_info = os.popen('adb devices').read()
    for line in device_info.splitlines():
        if line == 'List of devices attached':
            continue
        else:
            com = re.compile('(.*?)\tde.*?')
            SN = re.findall(com, line)
            for i in SN:
                SN_list.append(i)
    return SN_list

if __name__ == '__main__':
    width = os.get_terminal_size().columns
    sn = getDevicesSn()
    for i in sn:
        systems = getSecurityPatch(i)
        print("\n##### system.img --> \033[0;31;40m{}\033[0m".format(systems))
        print("##### If there is an error, please contact me.")
        print("##### Please contact me if you need to add xTS pre-setting or push media.")

        print("\n"+ "#####\033[0;32;40m{}:此设备正在刷GSI,请稍等!\033[0m#####".format(i).center(width, '*'))

        flashGsi(a, boot, i, width, systems)
        time.sleep(5)
    print("\n"+ "#####\033[0;32;40m共{}台手机刷GSI完成!\033[0m#####".format(len(sn)).center(width, '*'))
    # time.sleep(2)
    # if a == 'gsi':
    #     print("\n"+ "#####\033[0;31;40m请手动点击Allow USB debugging弹框\033[0m#####".center(width))
    #     time.sleep(75)
    #     os.system("python3 setting.py")
    #     time.sleep(1)
    #     os.system("python3 auto_media_push.py")
    # else:
    #     time.sleep(75)
    #     os.system("python3 setting.py")
    #print('*'*int((width/2-2)) + "\033[0;32;40m\t{}台手机刷GSI完成！\033[0m".format(len(sn)) + '*'*int((width/2-2)))