#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

pipenv run blackfire run gunicorn --bind=0.0.0.0:8000 --timeout 600 voiceMarketplace.wsgi
