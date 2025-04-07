# the main program is running on the esp32 which has temprature sensors connected to its GPIO 13 with a 4.7k ohm resistor between vbus and GPIO 13
try:
    import connect_wifi
    import read_temperature
    from udp_send import UDPSender
    import secrets
    import time

    TEMP_PORT = 5005
    udp = UDPSender(secrets.UDP_SERVER_IP, TEMP_PORT)

    connect_wifi.connect()

    while True:
        readings = read_temperature.read_all_temperatures()
        for name, temp in readings:
            if temp is not None:
                payload = f"{temp}"
                udp.send(name, payload)
                print(f"🌡️ {name}: {temp}°C → 📤 Sent to {secrets.UDP_SERVER_IP}:{TEMP_PORT}")
            else:
                print(f"⚠️ {name}: Failed to read sensor")
        time.sleep(5)

except Exception as e:
    print("❌ Error:", e)

