#!/bin/bash
#https://superuser.com/questions/181517/how-to-execute-a-command-whenever-a-file-changes
inotifywait -e close_write,moved_to,create -m . |
while read -r directory events filename; do
  #check if file in question has been changed
  #docker will write the command to be executed in this file
  if [ "$filename" = "pipe_cmd.txt" ]; then
    echo "SOMETHING CHANGED"
    #execute the command and hope for the best
    source ./pipe_cmd.txt
  fi
done