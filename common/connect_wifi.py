import network
import time
from secrets import WIFI_SSID, WIFI_PASSWORD

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    for _ in range(20):
        if wlan.isconnected():
            break
        time.sleep(1)

    if wlan.isconnected():
        print("Connected:", wlan.ifconfig()[0])
    else:
        print("Failed to connect to Wi-Fi")

