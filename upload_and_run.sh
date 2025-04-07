#!/bin/bash

MODE=$1
PORT=/dev/ttyACM0
MPREMOTE=/home/audrey/.local/bin/mpremote

if [[ -z "$MODE" ]]; then
  echo "❌ Usage: ./upload_and_run.sh <mode>"
  echo "   Example: ./upload_and_run.sh temperature_sensor"
  exit 1
fi

echo "🚀 Uploading $MODE to ESP32..."

FILES=(
  "common/connect_wifi.py"
  "common/udp_send.py"
  "$MODE/main.py"
)

# Optional: include secrets if present
[[ -f "common/secrets.py" ]] && FILES+=("common/secrets.py")
[[ -f "$MODE/read_temperature.py" ]] && FILES+=("$MODE/read_temperature.py")
[[ -f "$MODE/sensors.json" ]] && FILES+=("$MODE/sensors.json")

for file in "${FILES[@]}"; do
  dest="$(basename $file)"
  echo "📄 Uploading $file ..."
  $MPREMOTE connect $PORT fs cp "$file" ":$dest"
done

echo "🧠 Running main.py..."
$MPREMOTE connect $PORT run "$MODE/main.py"

