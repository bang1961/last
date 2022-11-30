#!/bin/sh

ROOT_PATH="/home/super/projects/thyroid/WebPlatform/lt4/"
CERTIFICATE_PATH="/etc/letsencrypt/live/ltlux.duckdns.org"


if [ -d $ROOT_PATH/lt4/UTIL ]; then 
    echo "인증서를 저장할 폴더가 이미 있습니다. \n"
else
    mkdir $ROOT_PATH/UTIL
    echo "인증서를 저장할 폴더가 존재하지 않아 생성하였습니다. \n"
fi

sudo cp $CERTIFICATE_PATH/fullchain.pem $ROOT_PATH/UTIL/fullchain.pem
sudo cp $CERTIFICATE_PATH/privkey.pem $ROOT_PATH/UTIL/privkey.pem

echo "Certbot 인증서를 가져왔습니다."

sudo chmod 777 $ROOT_PATH/UTIL/fullchain.pem
sudo chmod 777 $ROOT_PATH/UTIL/privkey.pem

echo "Certbot 인증서 권한을 변경하였습니다. \n"
ls -al  $ROOT_PATH/UTIL

python $ROOT_PATH/manage.py runserver 0:9999 
