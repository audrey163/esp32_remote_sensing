import machine, onewire, ds18x20, time
import ujson as json
import sys

ds_pin = machine.Pin(13)
ow = onewire.OneWire(ds_pin)
ds = ds18x20.DS18X20(ow)

CONFIG_FILE = "sensors.json"

def load_sensor_map():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except:
        print("❌ Failed to load sensor map.")
        return {}

def read_all_temperatures():
    sensor_map = load_sensor_map()
    roms = ds.scan()
    time.sleep_ms(100)

    if not roms:
        return []

    # Check for unknown sensors
    for rom in roms:
        rom_hex = ''.join('{:02x}'.format(b) for b in rom)
        if rom_hex not in sensor_map:
            print(f"🆕 New sensor detected: {rom_hex}")
            print(f"❌ ERROR: Sensor is not named in sensors.yaml. Please edit the file and re-upload.")
            sys.exit()

    temps = []
    ds.convert_temp()
    time.sleep_ms(750)

    for rom in roms:
        rom_hex = ''.join('{:02x}'.format(b) for b in rom)
        name = sensor_map[rom_hex]
        try:
            temp = ds.read_temp(rom)
            temps.append((name, temp))
        except Exception as e:
            temps.append((name, None))  # or skip instead
    return temps

