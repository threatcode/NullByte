import os
import sys
from time import sleep
from modules.logo import *
from modules.system import *

yellow="\033[1;33m"
blue="\033[1;34m"
nc="\033[00m"

class tool:
  @classmethod
  def install(self):
    while True:
      system=sys()
      os.system("clear")
      logo.ins_tnc()
      inp=input(f"{yellow}Do you want to install NullByte [Y/n]> {nc}")
      if inp=="y" or inp=="Y":
        os.system("clear")
        logo.installing()
        if system.sudo is not None:
          #require root permission
          if os.path.exists(system.conf_dir+"/NullByte"):
            pass
          else:
            os.system(system.sudo+" mkdir "+system.conf_dir+"/NullByte")
          os.system(system.sudo+" cp -r modules core NullByte.py "+system.conf_dir+"/NullByte")
          os.system(system.sudo+" cp -r core/NullByte "+system.bin)
          os.system(system.sudo+" cp -r core/nullbyte "+system.bin)
          os.system(system.sudo+" chmod +x "+system.bin+"/NullByte")
          os.system(system.sudo+" chmod +x "+system.bin+"/nullbyte")
          os.system("cd .. && "+system.sudo+" rm -rf NullByte")
          if os.path.exists(system.bin+"/NullByte") and os.path.exists(system.conf_dir+"/NullByte"):
            os.system("clear")
            logo.ins_sc()
            tmp=input(f"{blue}NullByte{nc}@{blue}space {yellow}$ {nc}")
            break
          else:
            os.system("clear")
            logo.not_ins()
            tmp=input(f"{blue}NullByte{nc}@{blue}space {yellow}$ {nc}")
            break
        else:
          if os.path.exists(system.conf_dir+"/NullByte"):
            pass
          else:
            os.system("mkdir "+system.conf_dir+"/NullByte")
          os.system("cp -r modules core NullByte.py "+system.conf_dir+"/NullByte")
          os.system("cp -r core/NullByte "+system.bin)
          os.system("cp -r core/nullbyte "+system.bin)
          os.system("chmod +x "+system.bin+"/NullByte")
          os.system("chmod +x "+system.bin+"/nullbyte")
          os.system("cd .. && rm -rf NullByte")
          if os.path.exists(system.bin+"/NullByte") and os.path.exists(system.conf_dir+"/NullByte"):
            os.system("clear")
            logo.ins_sc()
            tmp=input(f"{blue}NullByte{nc}@{blue}space {yellow}$ {nc}")
            break
          else:
            os.system("clear")
            logo.not_ins()
            tmp=input(f"{blue}NullByte{nc}@{blue}space {yellow}$ {nc}")
            break
      else:
        break

if __name__=="__main__":
  try:
    tool.install()
  except KeyboardInterrupt:
    os.system("clear")
    logo.exit()
