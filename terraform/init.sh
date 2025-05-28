#!/bin/bash
apt-get update
apt-get install -y nodejs npm git
npm install -g pm2

# Clone ou update ton repo (adapter URL et branche)
if [ ! -d "/home/${USER}/iot-api" ]; then
  git clone https://github.com/ton-user/ton-repo.git /home/${USER}/iot-api
else
  cd /home/${USER}/iot-api
  git pull origin main
fi

cd /home/${USER}/iot-api
npm install
pm2 start index.js --name iot-api || pm2 restart iot-api
pm2 save
