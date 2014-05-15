raspivid -n -w 1280 -h 720 -o - -t 9999999 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8080}' :demux=h264
