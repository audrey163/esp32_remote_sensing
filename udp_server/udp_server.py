import socket
import csv
import os
import time
import threading

class UDPServer:
    def __init__(self, name, port, csv_file, header, verbose=False):
        self.name = name
        self.port = port
        self.csv_file = csv_file
        self.header = ["sensor", "timestamp"] + header
        self.verbose = verbose
        self.running = False

    def _ensure_csv_file(self):
        file_exists = os.path.isfile(self.csv_file)
        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(self.header)

    def start(self):
        self._ensure_csv_file()
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()
        print(f"📡 [{self.name}] Listening on UDP port {self.port}, logging to {self.csv_file}")

    def _run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))

        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)

            while self.running:
                try:
                    data, addr = sock.recvfrom(1024)
                    text = data.decode().strip()
                    sensor, payload = text.split(":", 1)
                    values = payload.split(",")

                    timestamp = int(time.time())
                    row = [sensor, timestamp] + values
                    writer.writerow(row)
                    f.flush()

                    if self.verbose:
                        print(f"[{self.name}] 🧾 {sensor} @ {time.ctime(timestamp)} → {values}")

                except Exception as e:
                    print(f"[{self.name}] ❌ Error processing packet: {e}")

    def stop(self):
        self.running = False
        print(f"🛑 [{self.name}] Server stopped.")


if __name__ == "__main__":
    # Temperature sensor on port 5005
    temp_server = UDPServer(
        name="temperature",
        port=5005,
        csv_file="temperature.csv",
        header=["temperature"],
        verbose=True
    )

    # 9D telemetry sensor on port 5006
    imu_server = UDPServer(
        name="telemetry_9d",
        port=5006,
        csv_file="telemetry.csv",
        header = [
            "roll","pitch","yaw",   # rool - phi ϕ,pitch - theta θ,yaw - psi (ψ)
            "accel_x","accel_y","accel_z",
            "mag_x","mag_y","mag_z"
        ],
        verbose=True
    )

    try:
        temp_server.start()
        imu_server.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        temp_server.stop()
        imu_server.stop()
        print("🧼 All servers stopped. Logs saved.")
