#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/foldcloud"
REPOSITORY="https://github.com/AnnavarapuJashwanth/ProtienStructure.git"
APP_USER="ubuntu"

apt-get update
apt-get install -y git python3 python3-venv python3-pip

if [ ! -d "${APP_DIR}/.git" ]; then
  git clone --branch main "${REPOSITORY}" "${APP_DIR}"
else
  git -C "${APP_DIR}" pull --ff-only origin main
fi

python3 -m venv "${APP_DIR}/.venv"
"${APP_DIR}/.venv/bin/pip" install --upgrade pip
"${APP_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

install -o "${APP_USER}" -g "${APP_USER}" -d "${APP_DIR}"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"
install -o root -g root -m 0644 \
  "${APP_DIR}/deploy/foldcloud.service" \
  /etc/systemd/system/foldcloud.service

systemctl daemon-reload
systemctl enable --now foldcloud.service
