#!/bin/bash

printf '\033]2;uninstall.sh\a'

G="\033[1;34m[*] \033[0m"
S="\033[1;32m[+] \033[0m"
E="\033[1;31m[-] \033[0m"

if [[ $(id -u) != 0 ]]
then
   echo -e ""$E"Permission denied!"
   exit
fi

{
rm /bin/quack
rm /usr/local/bin/quack
rm -rf ~/quack
rm /data/data/com.termux/files/usr/bin/quack
} &> /dev/null
