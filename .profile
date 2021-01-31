chown root: /app && chmod -R 755 /app
mkdir /app/submissions && chmod -R 777 /app/submissions
echo "alias rm='ls'" >> /etc/profile && . /etc/profile