#!/usr/bin/bash
set -e

echo "Starting Klereo Pool Manager Add-on..."

# Load configuration from Home Assistant
CONFIG_PATH="/data/options.json"

if [ ! -f "$CONFIG_PATH" ]; then
    echo "ERROR: Configuration file not found at $CONFIG_PATH"
    exit 1
fi

# Parse configuration using jq
klereo_username=$(jq -r '.klereo_username // empty' "$CONFIG_PATH")
klereo_password=$(jq -r '.klereo_password // empty' "$CONFIG_PATH")
update_interval=$(jq -r '.update_interval // 600' "$CONFIG_PATH")
log_level=$(jq -r '.log_level // "info"' "$CONFIG_PATH")

# Export configuration as environment variables
export KLEREO_USERNAME="${klereo_username}"
export KLEREO_PASSWORD="${klereo_password}"
export UPDATE_INTERVAL="${update_interval}"
export LOG_LEVEL="${log_level^^}"

# Home Assistant add-ons have automatic access to the supervisor API
export HOMEASSISTANT_URL="http://supervisor/core"
export HOMEASSISTANT_TOKEN="${SUPERVISOR_TOKEN}"

# Log startup information
echo "Log level: ${log_level}"
echo "Update interval: ${update_interval}s"
echo "Home Assistant integration: automatic via supervisor"

# Validate configuration
if [ -z "${klereo_username}" ]; then
    echo "ERROR: Klereo username is required!"
    exit 1
fi

if [ -z "${klereo_password}" ]; then
    echo "ERROR: Klereo password is required!"
    exit 1
fi

# Change to working directory
cd /usr/bin || exit 1

# Start the application
echo "Starting Klereo Pool Manager service..."
exec python3 /usr/bin/klereo