#!/bin/bash

#if pgrep fbi 
#then
#sudo kill $(pgrep fbi) 
#  echo "fbi stopped"
#else
#  echo "fbi not running"
#fi
 
sudo fbi -noverbose -T 2 -a -m 1900x1200  -t 5 -u ~/pic_test/pictures/* > /dev/null 2>&1&
echo "fbi started"
