#!/usr/bin/python
import time
import sys, os
import logging
import subprocess
import signal

from os import listdir
from os.path import isfile, join
import yaml
import random


######
with open('./gallery.yml', 'r') as f:
  settings = yaml.load(f)

VIDEO_FORMAT = (
    '.mov',
    '.api',
    '.m4v',
    '.mpeg',
    )

IMAGE_FORMAT = (
    '.png',
    '.jpg',
    '.jpeg',
    '.gif',
    )

APPS = {'video': "omxplayer --no-osd VIDEO", 
        'pictures': "sudo fbi -noverbose -T 2 -a -m 1900x1200  -t 5 -u DIRECTORY > /dev/null 2>&1&"
       }

if len(sys.argv) < 2:
    sys.exit("""
    Error: Incorrect number of arguments.
    Usage: python oxm.py <start|stop>
    Example: python oxm.py start""")

def start_stream():
    print "Starting Media Stream"
    while True:
      clear_frame_buffer()
      stop_process('ruby')
      show_pictures()
      print "done"

    #print get_file_list(VIDEO_FORMAT,str(settings['dir_videos']))

    #print get_file_list(IMAGE_FORMAT,str(settings['dir_pictures']))

def stop_stream():
    print "Stopping Media Stream"
    clear_frame_buffer()


def get_file_list(ext_list, dir):
	onlyfiles = [ f for f in listdir(dir) if isfile(join(dir,f)) ]
	return filter(lambda k: k.endswith(ext_list), onlyfiles)

def clear_frame_buffer():
    try:
        os.system('dd if=/dev/zero of=/dev/fb0 >> /dev/null 2>&1&')
    except:
        print "Failed to Clear Frame Buffer"

def stop_process(process_grep):
    #http://stackoverflow.com/questions/4214773/kill-process-with-python
    proc = subprocess.Popen(["pgrep", process_grep], stdout=subprocess.PIPE) 
    for pid in proc.stdout:
        print "Stopping %s with PID: %s" % (process_grep, pid)
        try: 
            os.kill(int(pid), signal.SIGTERM)
            #raise Exception("""wasn't able to kill the process 
            #                   HINT:use signal.SIGKILL or signal.SIGABORT""")
        except OSError as ex:
            continue

def pick_stream():
    app_selected_name = random.choice(APPS.keys())
    app_selected_command = APPS[app_selected_name]
    print "Playing %s with %s" % (app_selected_name, app_selected_command)

def show_pictures():
    stream_command_str = APPS['pictures'].replace('DIRECTORY', settings['dir_pictures'])
    print stream_command_str
    proc = subprocess.Popen('top', shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    time.sleep(15)

#################
command_string = str(sys.argv[1])

if command_string == "start":
	start_stream()
elif command_string == "stop":
	stop_stream()
else:
	print "Invalid Command"