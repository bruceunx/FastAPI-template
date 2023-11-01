#!/bin/bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app \
  --bind 0.0.0.0:8000 \
	--daemon \
  --access-logfile access.log \
  --error-logfile error.log \
  --log-level info
