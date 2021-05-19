#!/usr/bin/env python3 

import subprocess
import sys

# parse ifconfig output and get the ip
def ParseOutputIp(output):
	arr = output.split(b'\n')
	if not arr[0].find(b'RUNNING') != -1:
		return '',False
	ipline=arr[1].decode('utf-8').strip()
	iparg=ipline.split(' ')[1]
	return iparg,True


# run ifconfig, check status code, and parse
def GetInterfaceIp(int):
	result=subprocess.run(['ifconfig', int], capture_output=True)
	if result.returncode != 0:
		return '',False
	return ParseOutputIp(result.stdout)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		# read command line arg
		ip,status=GetInterfaceIp(sys.argv[1])
		if status:
			print('Interface:',sys.argv[1],'--', 'IP:',ip)
		else:
			print('Interface inactive')
                        sys.exit(1)
	else:
		wlanip,wstatus=GetInterfaceIp('wlan0')
		ethip,estatus=GetInterfaceIp('eth0')
		if wstatus:
			print('Interface: wlan0 -- IP:',wlanip)
		elif estatus:
			print('Interface: eth0 -- IP:',wlanip)
		else:
			print('No active interface')
                        sys.exit(1)
