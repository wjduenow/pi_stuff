#!/bin/bash
SERVICE='omxplayer'

#declare -a videos=( "EarthTimeLapseViewfromSpace.mp4" "Clouds-Time_lapse_19.mp4" );

videos[1]="EarthTimeLapseViewfromSpace.mp4"
videos[0]="Clouds-Time_lapse_19.mp4"

while true; do
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
echo "running" # sleep 1
else
# omxplayer --no-osd  Clouds-Time_lapse_19.mp4 &

selected_video=${videos[($RANDOM % ${#videos[@]}) + 1 ]}

echo $selected_video

omxplayer --no-osd $selected_video & 

fi
done
