#!/usr/bin/env python3

import subprocess
import sys
import os

def set_home_network():
  
  items = ["CSM_add_network"] 
  ssid = input("What is the name of your home network? (Case sensitive)\n")
  password_bool = False
  is_there_password = False
  while not password_bool:
      want_password = input("Does this network have a password? (y/n)\n")
      if want_password.lower() == 'y':
          password = input("What is the password to this network? (It will be encrypted)\n")
          password_bool = True
          is_there_password = True
      elif want_password.lower() == 'n':
          password_bool = True
          password = ""
      else:
          print("Error! Re-enter input using (y/n)")
  #print(ssid)
  want_priority = False
  priority_bool = True
  while not want_priority:
      priority = input("Would you like to set a priority of connecting to this network over MINES networks? (y/n)\n")
      if priority.lower() == 'n':
          priority_bool = True
          want_priority = True
      elif priority.lower() == 'y':
          priority_bool = False
          want_priority = True
          items.append("--priority")
      else:
          print("Error! Re-enter input using (y/n)")
      while  not priority_bool:
              priority_level = input("Would you like low, medium, or high priority? (CSMwireless is set to medium)\n")
              if priority_level.lower() == "low":
                  priority = 1
                  priority_bool = True
                  items.append(str(priority))
              elif priority_level.lower() == "medium":
                  priority = 2
                  priority_bool = True
                  items.append(str(priority))
              elif priority_level.lower() == "high":
                  priority = 3
                  priority_bool = True
                  items.append(str(priority))
              else:
                  print("Error! Re-enter input using (low, medium, high)")
       
 
  try:
    response = subprocess.run(["CSM_wpa_country","get"], capture_output = True, check = True)
  except subprocess.CalledProcessError as e:
      items.append("-c")
      items.append("US")
      
    
  if is_there_password:
      items.append("-p")
      items.append(password)
  else:
      items.append("-n")
      
  items.append(str(ssid))
  subprocess.run(items)

if __name__ == "__main__":
    if os.geteuid()!= 0:
      print("Permission Denied: Must be run as super user!")
      sys.exit(1)
    set_home_network()

