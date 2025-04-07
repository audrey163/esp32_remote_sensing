# 🌍 Remote Sensing — ESP32-S2 Modular Sensor Framework

A flexible MicroPython-based system for collecting and transmitting data from multiple sensor types over UDP.  
Designed for ESP32-S2 devices with a shared `common/` library and modular subdirectories for each sensor type.

---

## ✅ Features

- 📶 Wi-Fi support using `common/connect_wifi.py`
- 🔐 Credential isolation in `common/secrets.py`
- 🌡️ DS18B20 temperature sensing module
- 🧭 (Planned) 9-axis IMU telemetry module
- 📤 Sends all data over UDP for logging and visualization
- 🔁 Modular: add new sensor modules as needed
- 🧠 Minimal and readable MicroPython code

---

## 🧱 Project Structure

```
remote_sensing/
├── common/                # Shared Wi-Fi + UDP logic
│   ├── connect_wifi.py
│   ├── secrets.py         # not committed (user-supplied)
│   └── udp_send.py
├── temperature_sensor/    # DS18B20 temperature logic
│   ├── main.py
│   ├── read_temperature.py
│   ├── sensors.json
├── imu_9d_sensor/         # Placeholder for 9D IMU logic
│   └── (to be implemented)
├── udp_server/            # Cross-project UDP logger
│   └── udp_server.py
├── upload_and_run.sh      # Upload script with mode selector
├── ESP32_GENERIC_S2-*.bin # ESP32 firmware (optional)
└── README.md              # You’re here!
```

---

## 🚀 Usage

### 1. 📡 Start the UDP Logging Server (on your PC)

```bash
cd udp_server
python3 udp_server.py
```

This will log all UDP packets to `*.csv` files in the udp_server directory.

---

### 2. 📦 Upload & Run ESP32 Module

From the root directory:

```bash
# Run the temperature sensor module
./upload_and_run.sh temperature_sensor

# (Future) Run the 9D IMU module
./upload_and_run.sh imu_9d_sensor
```

This script uploads the appropriate files and runs `main.py` from that module.

---

## 📤 UDP Format

All data is sent as:

```
sensor_name:value1[,value2,...]
```

Example:
```
fresh_water:17.625
imu:0.1,0.2,0.3,9.8,0.0,0.0,30,40,50
```

---

## 🛠️ Adding New Sensor Modules

1. Create a folder: `my_sensor/`
2. Add a `main.py` that imports from `common/`
3. Add any support files (e.g. `read_my_sensor.py`)
4. Update `upload_and_run.sh` to recognize your mode

---

## 🧼 Secrets File Example (`common/secrets.py`)

```python
WIFI_SSID = "your-wifi"
WIFI_PASSWORD = "your-password"
UDP_SERVER_IP = "192.168.1.123"  # Destination PC/server
```
