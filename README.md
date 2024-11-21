[![Tests](https://github.com/IoT-balance-project/balance-mqtt-subscriber/actions/workflows/test.yaml/badge.svg)](https://github.com/IoT-balance-project/balance-mqtt-subscriber/actions/workflows/test.yaml)

# MQTT subscriber

A service to listen for messages and save the data.

# Installation

Create a service user.

Create a virtual environment

```bash
sudo mkdir -p /opt/balance-subscriber
sudo python3 -m venv /opt/balance-subscriber/venv
```

Activate the virtual environment

```bash
source /opt/balance-subscriber/venv/bin/activate
```

Install this package

```bash
pip install balance-subscriber
```

# Usage

The app will run as a service in the background.

## Monitoring

View service status

```bash
sudo systemctl status balance-subscriber.service
```

View logs

```
sudo journalctl -u balance-subscriber.service --since "1 hour ago"
```
