#!/usr/bin/env bash
set -e

# Install the systemd service
cp --verbose ./systemd/balance-subscriber.service /etc/systemd/system/balance-subscriber.service
