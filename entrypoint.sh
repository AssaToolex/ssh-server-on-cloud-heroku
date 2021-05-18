#!/bin/bash

if [[ -z "${SERVER_DOMAIN_NAME}" ]]; then
  export SERVER_DOMAIN_NAME="xxx-xxx-54345.herokuapp.com"
fi
echo "Domain name: ${SERVER_DOMAIN_NAME}"


if [[ -z "${USER_IDENTITYS}" ]]; then
  export USER_IDENTITYS="user01:ssh-rsa ABNaCy2AA...Wi63c8= user01@server01;user02:ssh-rsa BCNy32A54...Zi4535c0= user02@server02"
fi

echo "Users:"
echo "${USER_IDENTITYS};:" | tr ";" "\n" | \
while read user_ident; do
  # ok # echo "User set: =->${user_ident}<-="
  if [[ "${user_ident}" != "" ]]; then
    if [[ "${user_ident}" != ":" ]]; then
      echo "${user_ident}" | tr ":" "\n" | read username userkey
      echo "User: ${username}, Key: ${userkey}"
      if [[ "${username}" != "" ]]; then
        echo "User-do: ${username}"
        # .ssh/authorized_keys
      fi
    fi
  fi
done


# SSHd

echo "Port 22022" >> /etc/ssh/sshd_config
echo "PermitRootLogin no" >> /etc/ssh/sshd_config
echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config
# echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
# echo "AllowUsers Fred Wilma" >> /etc/ssh/sshd_config

# Run OpenSSH server in no-daemon mode
# /usr/sbin/sshd -D

# Run OpenSSH server in daemon mode
/usr/sbin/sshd


# Squid

# Run Squid server in daemon mode
squid3


# Nginx

bash /conf/nginx_default.conf > /etc/nginx/sites-available/default
echo "# Nginx config in /etc/nginx/sites-available/default"
cat /etc/nginx/sites-available/default

nginx -g 'daemon off;'
