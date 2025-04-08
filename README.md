# OLED System Monitor for Raspberry Pi

A lightweight Python script that displays real-time system stats on a small SSD1306 OLED display (I2C) connected to a Raspberry Pi.

This script cycles between two pages:
- **Page 1**: IP Address, CPU Usage, RAM Usage
- **Page 2**: Disk Usage, CPU Temperature, Uptime

If the display is not available, the stats are printed to the terminal instead.

---

## Requirements

- Raspberry Pi (or compatible Linux device)
- SSD1306 OLED display (I2C interface)
- Python 3
- Required Python packages:
  - `psutil`
  - `Pillow`
  - `luma.oled`

Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip fonts-dejavu
pip3 install psutil pillow luma.oled
```

---

## File Structure

```
oled_monitor.py               # Main Python script
/etc/systemd/system/
  └── oled-monitor.service    # systemd service for background execution
```

---

## Usage

Run the script manually:
```bash
python3 oled_monitor.py
```

Or make it executable:
```bash
chmod +x oled_monitor.py
./oled_monitor.py
```

---

## Running in Background (Autostart with systemd)

To run this script **automatically on boot** and **in the background**, set up a `systemd` service.

### 1. Create the service file

```bash
sudo nano /etc/systemd/system/oled-monitor.service
```

Paste this into the file:

```ini
[Unit]
Description=OLED System Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/<username>/background-scripts/oled_monitor.py
Restart=always
User=<username>
Environment=PYTHONUNBUFFERED=1
WorkingDirectory=/home/<username>/background-scripts

[Install]
WantedBy=multi-user.target
```

### 2. Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable oled-monitor.service
sudo systemctl start oled-monitor.service
```

### 3. Monitor logs (optional)

```bash
journalctl -u oled-monitor.service -f
```

---
