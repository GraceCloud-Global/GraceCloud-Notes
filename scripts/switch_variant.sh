#!/bin/bash
VARIANT=\
if [ "\" == "green" ]; then
  sed -i 's/default gracealone_blue/default gracealone_green/' /etc/nginx/sites-available/gracealone_bluegreen
else
  sed -i 's/default gracealone_green/default gracealone_blue/' /etc/nginx/sites-available/gracealone_bluegreen
fi
sudo nginx -s reload
echo "🔄 Switched live traffic to \"
