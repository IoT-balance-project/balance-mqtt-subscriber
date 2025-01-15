#!/usr/bin/env bash
set -e

# Install the MQTT subscriber service
# Usage:
# sudo bash -x install.sh $version
# version: The version of the package to install

# Set options
venv_dir="/opt/balance-subscriber/venv"
python="$venv_dir/bin/python"
pip="$python -m pip"
version="${1:-*}"

# Install requirements
apt install -qqq python3.12 python3.12-venv

# Create virtual environment
mkdir --parents "$(dirname $venv_dir)"
python3 -m venv $venv_dir
# Update pip
$python -m pip install -q --upgrade pip
# Install the subscriber package
$pip install --upgrade balance-subscriber="$version"

# Install the systemd service
cp --verbose ./systemd/balance-subscriber.service /etc/systemd/system/balance-subscriber.service

# Reload systemd units
systemctl daemon-reload
