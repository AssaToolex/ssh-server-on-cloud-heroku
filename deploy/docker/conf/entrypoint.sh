#!/bin/bash

if [[ -z "${SERVER_DOMAIN_NAME}" ]]; then
  export SERVER_DOMAIN_NAME="xxx-xxx-54345.herokuapp.com"
fi
echo "Domain name: ${SERVER_DOMAIN_NAME}"

if [[ -z "${USER_IDENTITYS}" ]]; then
  export USER_IDENTITYS="user01:ssh-rsa ABNaCy2AA...Wi63c8= user01@server01;user02:ssh-rsa BCNy32A54...Zi4535c0= user02@server02"
fi

if [[ -z "${SSMTP_PARAMETERS}" ]]; then
  export SSMTP_PARAMETERS="root=reports@gmail.com;mailhub=smtp.gmail.com:587;hostname=localhost;UseSTARTTLS=YES;AuthUser=reports@gmail.com;AuthPass=qwerty"
fi
echo "# new file." > /etc/ssmtp/ssmtp.conf
echo "${SSMTP_PARAMETERS}" | tr ";" "\n" | while read -r ssmpt_line; do
  echo "${user_ident}" >> /etc/ssmtp/ssmtp.conf
done


echo "Users:"
echo "${USER_IDENTITYS};:" | tr ";" "\n" | while read -r user_ident; do
  if [[ "${user_ident}" != "" || "${user_ident}" != ":" ]]; then
    # ok # echo "User set: =->${user_ident}<-="
    username=`echo ${user_ident} | cut -d: -f1`
    if [[ "${username}" != "" ]]; then
      userkey=`echo ${user_ident} | cut -d: -f2`
      # ok # echo "username: ${username}, userkey: ${userkey}."
      # sudo useradd -d /home/${username} -s /bin/bash -m ${username}
      # mkdir -p /home/${username}/.ssh
      # echo "${userkey}" >> /home/${username}/.ssh/authorized_keys
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

# Run Nginx server in daemon mode
nginx -g 'daemon on;'

# Run Nginx server in no-daemon mode
# nginx -g 'daemon off;'


# Redis

# Run Redis server in daemon mode
redis-server &

# Run Redis server in no-daemon mode
# redis-server


# Tor

# Run Tor server in daemon mode
tor &

# Run Tor server in no-daemon mode
# tor


# Custom SSHd 

# Custom SSHd server in daemon mode
# cd /tools && python3 paramiko-2104.py &

# Custom SSHd server in no-daemon mode
cd /tools && python3 paramiko-2104.py
