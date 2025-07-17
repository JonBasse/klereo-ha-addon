# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Home Assistant add-on for Klereo pool management systems. It integrates with the Klereo API to monitor and control pool equipment through Home Assistant.

## Development Commands

### Docker Build
```bash
docker build -t klereo-addon ./klereo
```

### Testing the Add-on
```bash
# Run locally with Docker
docker run -p 8080:8080 -v /path/to/config:/data klereo-addon

# Test configuration files
python3 -c "import json; print(json.load(open('/data/options.json')))"
```

### Add-on Management
```bash
# Check configuration schema
cat klereo/config.yaml

# View logs
docker logs <container-id>

# Test API connectivity
python3 -c "from klereo_api import KlereoAPI; api = KlereoAPI('user', 'pass'); print(api.test_connection())"
```

## Architecture

### Core Components

1. **Main Application** (`klereo/rootfs/usr/bin/klereo`)
   - Entry point and main orchestration
   - Handles configuration loading, signal handling, and main loop
   - Coordinates between Klereo API and Home Assistant integration

2. **Klereo API Client** (`klereo/rootfs/usr/bin/klereo_api.py`)
   - Handles authentication and API communication with Klereo service
   - Manages JWT token refresh, caching, and rate limiting
   - Includes maintenance window detection
   - Key intervals: JWT refresh (55min), index refresh (3h55min), pool details (9m50s)

3. **Home Assistant Integration** (`klereo/rootfs/usr/bin/ha_integration.py`)
   - Manages device registration and sensor entity creation
   - Handles Home Assistant API communication
   - Updates sensor states and manages entity lifecycle

### Configuration Structure

- **Add-on Config**: `klereo/config.yaml` - Defines add-on metadata, options schema, and runtime configuration
- **Build Config**: `klereo/build.yaml` - Multi-architecture Docker build configuration
- **Runtime Config**: `/data/options.json` - User configuration loaded at runtime
- **Service Script**: `klereo/rootfs/etc/services.d/klereo/run` - Add-on startup script

### Key Features

- **Multi-pool Support**: Automatically discovers and manages multiple pools from a single Klereo account
- **Automatic Device Discovery**: Creates Home Assistant devices and sensor entities for each pool
- **Rate Limiting**: Respects API limits with intelligent caching and refresh intervals
- **Maintenance Windows**: Automatically pauses API requests during scheduled maintenance
- **Health Monitoring**: Periodic health checks for both Klereo API and Home Assistant connectivity

### Entity Naming Convention

Sensor entities follow the pattern: `sensor.klereo_{pool_id}_{parameter_name}`

Examples:
- `sensor.klereo_12345_ph`
- `sensor.klereo_12345_temperature`
- `sensor.klereo_12345_chlorine`

### Configuration Parameters

Required:
- `klereo_username`: Klereo.fr account username
- `klereo_password`: Klereo.fr account password

Optional:
- `update_interval`: Sensor update interval (300-3600s, default: 600s)
- `log_level`: Logging verbosity (debug|info|warning|error)
- `homeassistant_url`: Home Assistant core URL (default: http://supervisor/core)
- `homeassistant_token`: Long-lived access token (auto-detected if not provided)

## Development Notes

- The add-on uses Python 3.11 base images from Home Assistant
- All Python dependencies are installed in the Dockerfile
- The service runs as a daemon with proper signal handling
- Configuration is loaded from Home Assistant supervisor or environment variables
- Logging goes to both stdout and `/var/log/klereo.log`
- The add-on exposes port 8080 for potential future web interface