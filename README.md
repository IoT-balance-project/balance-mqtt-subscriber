[![Tests](https://github.com/IoT-balance-project/balance-mqtt-subscriber/actions/workflows/test.yaml/badge.svg)](https://github.com/IoT-balance-project/balance-mqtt-subscriber/actions/workflows/test.yaml)

# MQTT subscriber

A service to listen for messages and save the data.

# Installation

## Install Python package

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
pip install --upgrade balance-subscriber
```

## Set up service

Create a service account called `balance-subscriber`.

```bash
sudo useradd --system balance-subscriber
```

This user must have permissions to write to the target data directory.

Install the [systemd](https://systemd.io/) service.

```bash
cp --verbose ./systemd/balance-subscriber.service /etc/systemd/system/balance-subscriber.service
```

Enable the service

```bash
sudo systemctl enable balance-subscriber.service
```

# Configuration

Configure the service

```bash
sudo systemctl edit balance-subscriber.service
```

This will create an override configuration file in the directory `/etc/systemd/system/balance-subscriber.service.d`.
Edit this file to set the options for the service, such as the target data directory.

```unit file (systemd)
[Service]
Environment="DATA_DIR=/tmp"
Environment="HOST=localhost"
```

The available options are listed in the configuration section.

## Options

The following options are available.

| Setting  | Description                                         |
|----------|-----------------------------------------------------|
| DATA_DIR | The target directory to serialise MQTT messages to. |
| HOST     | MQTT broker host name                               |
| PORT     | MQTT broker port                                    |
| TOPICS   | MQTT topics                                         |

These settings are specified in the configuration file for the systemd service as described in the installation section.

# Usage

The app will run as a service in the background.

## Service control

Start the service

```bash
sudo systemctl start balance-subscriber.service
```

Stop the service

```bash
sudo systemctl stop balance-subscriber.service
```

## Monitoring

View service status

```bash
sudo systemctl status balance-subscriber.service
```

View logs

```
sudo journalctl -u balance-subscriber.service --since "1 hour ago"
```
