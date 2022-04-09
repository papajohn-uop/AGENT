#!/bin/bash

cd /home/lime/AGENT/server/src
/home/lime/.local/bin/uvicorn openapi_server.main:app --host 172.16.10.208 --port 28080

