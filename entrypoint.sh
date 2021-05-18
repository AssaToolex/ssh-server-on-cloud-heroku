#!/bin/bash

if [[ -z "${USER_IDENTITYS}" ]]; then
  export USER_IDENTITYS="user01:ssh-rsa ABNaCy2AA...Wi63c8= user01@server01;user02:ssh-rsa BCNy32A54...Zi4535c0= user02@server02;"
fi
echo ${USER_IDENTITYS}

for user_ident in $(echo ${USER_IDENTITYS} | tr ";" "\n"); do
  # process
  echo "${user_ident}"
done


bash /conf/nginx_tutorial.conf > /etc/nginx/conf.d/tutorial.conf
echo /etc/nginx/conf.d/tutorial.conf
cat /etc/nginx/conf.d/tutorial.conf

# Run OpenSSH server in no-daemon mode
# /usr/sbin/sshd -D
systemctl start ssh

# rm -rf /etc/nginx/sites-enabled/default
nginx -g 'daemon off;'
