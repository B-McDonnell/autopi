def getMAC():
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/wlan0/address').read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]
  
print(getMAC())
