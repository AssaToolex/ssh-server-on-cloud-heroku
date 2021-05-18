#!/bin/bash

if [[ -z "${SERVER_DOMAIN_NAME}" ]]; then
  export SERVER_DOMAIN_NAME="xxx-xxx-54345.herokuapp.com"
fi
echo ${USER_IDENTITYS}


if [[ -z "${USER_IDENTITYS}" ]]; then
  export USER_IDENTITYS="user01:ssh-rsa ABNaCy2AA...Wi63c8= user01@server01;;;user02:ssh-rsa BCNy32A54...Zi4535c0= user02@server02"
fi
echo ${USER_IDENTITYS}

echo "Users:"
echo ${USER_IDENTITYS} | tr ";;;" "\n"
#for user_ident in $(echo ${USER_IDENTITYS} | tr ";" "\n"); do
  # process
  #echo "${user_ident}"
  # .ssh/authorized_keys
#done

echo "Port ${PORT}" >> /etc/ssh/sshd_config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config
# echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
# echo "AllowUsers Fred Wilma" >> /etc/ssh/sshd_config


# bash /conf/nginx_tutorial.conf > /etc/nginx/conf.d/tutorial.conf
# echo /etc/nginx/conf.d/tutorial.conf
# cat /etc/nginx/conf.d/tutorial.conf

bash /conf/nginx_tutorial.conf > /etc/nginx/sites-available/default
echo "# /etc/nginx/sites-available/default"
cat /etc/nginx/sites-available/default


# Run OpenSSH server in no-daemon mode
/usr/sbin/sshd -D

# Run OpenSSH server in daemon mode
# /usr/sbin/sshd


# nginx -g 'daemon off;'
