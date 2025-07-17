#!/bin/bash
set -e

echo "$(date): Klereo Pool Manager Add-on starting..."

# Ensure log directory exists
mkdir -p /var/log

# Check if configuration exists
if [ ! -f "/data/options.json" ]; then
    echo "$(date): ERROR: Configuration file not found at /data/options.json"
    exit 1
fi

echo "$(date): Configuration found, starting Python application..."

# Set SUPERVISOR_TOKEN environment variable if not set
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN:-}"

# Start the Python application
exec python3 /usr/bin/klereo