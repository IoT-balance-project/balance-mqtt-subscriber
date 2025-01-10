[![Tests](https://github.com/IoT-balance-project/balance-mqtt-subscriber/actions/workflows/test.yaml/badge.svg)](https://github.com/IoT-balance-project/balance-mqtt-subscriber/actions/workflows/test.yaml)

# MQTT subscriber

A service to listen for messages and save the data.

```mermaid
flowchart LR
publisher --> broker
broker --> subscriber
subscriber --> storage[(Storage)]
```

# Installation

There is a Bash script to install this service: [`install.sh`](install.sh).
There are further details below.

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

Reload all systemd unit files

```bash
sudo systemctl daemon-reload
```

Enable the service

```bash
sudo systemctl enable balance-subscriber.service
```

# Configuration

Configure the service using the systemd configuration editor.

```bash
sudo systemctl edit balance-subscriber.service
```

This will create or edit an override configuration file in the directory `/etc/systemd/system/balance-subscriber.service.d`.
Edit this file to set the options for the service, such as the target data directory. Each row defines an environment variable containing a configuration setting for the service.

```unit file (systemd)
[Service]
Environment="DATA_DIR=/tmp"
```

Then, restart the service as described in the service control section.

## Options

The following options are available.

| Setting      | Required | Description                                                    | Default   |
|--------------| -------- |----------------------------------------------------------------|-----------|
| `DATA_DIR`   | Required | The path of the target directory to serialise MQTT messages to. |           |
| `HOST`       | Optional | MQTT broker host name                                          | localhost |
| `PORT`       | Optional | MQTT broker port                                               | 1883      |
| `USERNAME`   | Optional | MQTT broker username                                           |           |
| `PASSWORD`   | Optional | MQTT broker password                                           |           |
| `TOPICS`     | Optional | MQTT topics                                                    | #         |
| `QOS`        | Optional | Quality of service (0, 1, 2)                                   | 0         |
| `KEEP_ALIVE` | Optional | MQTT broker keep-alive interval (time in seconds)              | 60        |
| `LOG_LEVEL`  | Optional | Logging verbosity                                              | WARNING   |
| `EXT`        | Optional | File extension for saved messages                              | .bin      |

These settings are specified in the configuration file for the systemd service as described above.

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

Restart the service

```bash
sudo systemctl restart balance-subscriber.service
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
