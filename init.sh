#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

blackfire-agent --register --server-id="$BLACKFIRE_SERVER_ID" --server-token="$BLACKFIRE_SERVER_TOKEN"
/etc/init.d/blackfire-agent restart
blackfire config --client-id="$BLACKFIRE_CLIENT_ID" --client-token="$BLACKFIRE_CLIENT_TOKEN"

pipenv run blackfire run gunicorn --bind=0.0.0.0:8000 --timeout 600 voiceMarketplace.wsgi
