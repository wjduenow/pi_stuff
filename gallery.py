import sys, os
import logging
import subprocess
import signal

from os import listdir
from os.path import isfile, join
import yaml

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

if len(sys.argv) < 2:
    sys.exit("""
    Error: Incorrect number of arguments.
    Usage: python oxm.py <start|stop>
    Example: python oxm.py start""")

def start_stream():
    print "Starting Media Stream"
    clear_frame_buffer()
    stop_process()

    print get_file_list(VIDEO_FORMAT,str(settings['dir_videos']))

    print get_file_list(IMAGE_FORMAT,str(settings['dir_pictures']))

def stop_stream():
    print "Stopping Media Stream"
    clear_frame_buffer()


def get_file_list(ext_list, dir):
	onlyfiles = [ f for f in listdir(dir) if isfile(join(dir,f)) ]
	return filter(lambda k: k.endswith(ext_list), onlyfiles)

def clear_frame_buffer():
    try:
        os.system('dd if=/dev/zero of=/dev/fb0')
    except:
        print "Failed to Clear Frame Buffer"

def stop_process():
    proc = subprocess.Popen(["pgrep", 'ruby'], stdout=subprocess.PIPE) 
    for pid in proc.stdout:
        print pid
        os.kill(int(pid), signal.SIGTERM)
        try: 
            os.kill(int(pid), 0)
            raise Exception("""wasn't able to kill the process 
                               HINT:use signal.SIGKILL or signal.SIGABORT""")
        except OSError as ex:
            continue

#################
command_string = str(sys.argv[1])

if command_string == "start":
	start_stream()
elif command_string == "stop":
	stop_stream()
else:
	print "Invalid Command"