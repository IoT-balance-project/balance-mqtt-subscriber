#!/usr/bin/env bash
set -e

venv_dir="/opt/balance-subscriber/venv"

# Install requirements
apt install -qqq python3.12

# Create virtual environment
mkdir --parents "$(dirname $venv_dir)"
python3 -m venv $venv_dir
# Update pip
$venv_dir/bin/python -m pip install -q --upgrade pip
$venv_dir/bin/pip install --upgrade balance-subscriber

# Install the systemd service
cp --verbose ./systemd/balance-subscriber.service /etc/systemd/system/balance-subscriber.service

# Reload systemd units
systemctl daemon-reload
