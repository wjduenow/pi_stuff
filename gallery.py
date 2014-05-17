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

if len(sys.argv) < 2:
    error_message = """
Error: Incorrect number of arguments.
Usage: python oxm.py <start|stop>
Example: python oxm.py start
"""
    sys.exit(error_message)

def start_stream():
    print "Starting Media Stream"
    while True:
      clear_frame_buffer()
      run_app = pick_stream()
      stop_process(run_app['process'])
      exec("%s()" % (run_app['python_command']))
      print "done"


def stop_stream():
    print "Stopping Media Stream"
    stop_process('gallery')


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
    proc = subprocess.Popen(["pgrep", "-f", process_grep], stdout=subprocess.PIPE) 
    for pid in proc.stdout:
        print "Stopping %s with PID: %s" % (process_grep, pid)
        try: 
            os.kill(int(pid), signal.SIGTERM)
            #raise Exception("""wasn't able to kill the process 
            #                   HINT:use signal.SIGKILL or signal.SIGABORT""")
        except OSError as ex:
            continue

def pick_stream():
    app_selected_name = random.choice(settings['apps'].keys())
    app_selected_command = settings['apps'][app_selected_name]['python_command']
    print "Playing %s with %s" % (app_selected_name, app_selected_command)
    return settings['apps'][app_selected_name]

def show_pictures():
    print " -- SHOWING PICTURES"
    #print get_file_list(VIDEO_FORMAT,str(settings['dir_videos']))
    stream_command_str = settings['apps']['pictures']['command'].replace('DIRECTORY', settings['dir_pictures'])
    print stream_command_str
    proc = subprocess.Popen(stream_command_str, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    time.sleep(settings['pictures_time'])
    stop_process(settings['apps']['pictures']['process'])

def show_video():
    print " -- SHOWING VIDEO"
    video_list = get_file_list(tuple(settings['apps']['video']['formats']),str(settings['dir_videos']))

    selected_video = random.choice(video_list).strip()#.replace(" ", "\ ")
    selected_video = "%s%s" % (settings['dir_videos'], selected_video)
    stream_command_str = settings['apps']['video']['command'].replace('VIDEO', selected_video)
    stream_command_str = stream_command_str.replace('"', '')
    print stream_command_str
    proc = subprocess.Popen(stream_command_str, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    proc.wait()
    time.sleep(2)


#################
#  Main
#################
if __name__ == "__main__":
    command_string = str(sys.argv[1])

    if command_string == "start":
    	start_stream()
    elif command_string == "stop":
    	stop_stream()
    else:
    	print "Invalid Command"
