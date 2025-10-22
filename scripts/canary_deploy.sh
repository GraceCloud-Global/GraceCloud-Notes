#!/bin/bash
SERVICE=gracealone
echo '🚀 Deploying canary version...'
sudo systemctl stop \
cp -r /home/ubuntu/gracealoneaba /home/ubuntu/gracealoneaba_canary
cd /home/ubuntu/gracealoneaba_canary
git pull origin main
python manage.py migrate
sudo systemctl start \
echo '✅ Canary instance deployed at /gracealoneaba_canary'
