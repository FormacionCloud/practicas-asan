#!/bin/bash
export HOME=/root

# Actualizar paquetes
apt-get update

# Instalar curl
apt-get install -y unzip curl

# Instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
rm -rf aws awscliv2.zip

# Instalar VS Code Server
curl -fsSL https://code-server.dev/install.sh | sh

# Obtener password de Secrets Manager y almacenarlo en una variable de entorno
PASSWORD=$(aws secretsmanager get-secret-value --secret-id ${CodeServerPassword} --query SecretString --output text --region ${AWS::Region})

# Fichero de configuración de VS Code Server: IP de escucha y password a partir de variable de entorno anterior
mkdir -p /home/ubuntu/.config/code-server
cat << EOF > /home/ubuntu/.config/code-server/config.yaml
bind-addr: 0.0.0.0:8080
auth: password
password: $PASSWORD
cert: false
EOF

# Asignación de permisos al usuario ubuntu
chown -R ubuntu:ubuntu /home/ubuntu/.config

# Crear fichero systemd de servicio, para que se inicie VS Code Server tras cada reinicio de la máquina
# A diferencia del proceso de instalación por parte de un usuario normal, la instalación como root no crea el servicio automáticamente
# Recuerda que el script UserData es ejecutado por el usuario root
cat << EOF > /etc/systemd/system/code-server@.service
[Unit]
Description=code-server
After=network.target

[Service]
Type=exec
ExecStart=/usr/bin/code-server
Restart=always
User=%i

[Install]
WantedBy=default.target
EOF

# Actualización del listado de ficheros de servicio
systemctl daemon-reload

# Habilitación del servicio y puesta en marcha
systemctl enable --now code-server@ubuntu
