# Klereo Pool Manager Add-on Documentation

## Overview

The Klereo Pool Manager add-on enables Home Assistant to communicate with Klereo pool management systems, providing real-time monitoring and control of pool equipment.

## How It Works

1. **Authentication**: The add-on authenticates with the Klereo API using your credentials
2. **Pool Discovery**: Discovers all pools associated with your Klereo account  
3. **Device Registration**: Creates Home Assistant devices for each pool
4. **Sensor Creation**: Adds sensor entities for each pool parameter
5. **Data Updates**: Periodically fetches fresh data from the Klereo API

## Configuration Options

### Klereo Settings

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `klereo_username` | string | Yes | Your Klereo.fr username |
| `klereo_password` | password | Yes | Your Klereo.fr password |

### Update Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `update_interval` | integer | 600 | Update interval in seconds (300-3600) |

### System Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `log_level` | list | info | Log level: debug, info, warning, error |

## Supported Pool Parameters

The add-on supports monitoring of various pool parameters, including:

- **pH Level**: Water acidity/alkalinity
- **Temperature**: Water temperature
- **Chlorine Level**: Free chlorine concentration
- **ORP/Redox**: Oxidation-reduction potential
- **Water Level**: Pool water level
- **Additional Probes**: Any other sensors configured in your Klereo system

## Device Classes and Units

The add-on automatically assigns appropriate device classes and units:

| Parameter | Device Class | Unit | Icon |
|-----------|--------------|------|------|
| Temperature | temperature | °C | mdi:thermometer |
| pH | - | pH | mdi:ph |
| Chlorine | - | mg/L | mdi:water-percent |
| ORP/Redox | - | mV | mdi:alpha-r-circle |
| Water Level | - | cm | mdi:waves |

## Automation Examples

### pH Alert

```yaml
automation:
  - alias: "Pool pH Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.klereo_12345_ph
      below: 6.8
      above: 7.6
    action:
      service: notify.mobile_app
      data:
        message: "Pool pH is {{ states('sensor.klereo_12345_ph') }} - Check water chemistry"
```

### Temperature Monitoring

```yaml
automation:
  - alias: "Pool Temperature Ideal"
    trigger:
      platform: numeric_state
      entity_id: sensor.klereo_12345_temperature
      above: 25
      below: 28
    action:
      service: light.turn_on
      entity_id: light.pool_status
      data:
        color_name: green
```

## Dashboard Cards

### Simple Entity Card

```yaml
type: entity
entity: sensor.klereo_12345_ph
name: "Pool pH"
```

### Gauge Card

```yaml
type: gauge
entity: sensor.klereo_12345_temperature
name: "Pool Temperature"
min: 15
max: 35
severity:
  green: 20
  yellow: 30
  red: 32
```

### History Graph

```yaml
type: history-graph
entities:
  - sensor.klereo_12345_ph
  - sensor.klereo_12345_temperature
  - sensor.klereo_12345_chlorine
hours_to_show: 24
```

## Advanced Configuration

### Multiple Pools

If you have multiple pools, each will appear as a separate device:

```yaml
# Pool 1 sensors
sensor.klereo_12345_ph
sensor.klereo_12345_temperature

# Pool 2 sensors  
sensor.klereo_67890_ph
sensor.klereo_67890_temperature
```

### Custom Update Intervals

Adjust the update interval based on your needs:

```yaml
# More frequent updates (every 5 minutes)
update_interval: 300

# Less frequent updates (every 30 minutes)
update_interval: 1800
```

## Troubleshooting

### Add-on Won't Start

1. Check your Klereo credentials are correct
2. Verify internet connectivity
3. Check the add-on logs for error messages

### No Sensors Appearing

1. Ensure your pools have active probes
2. Check that probes are reporting data in the Klereo app
3. Verify the add-on has successfully connected to both APIs

### Sensors Not Updating

1. Check the update interval configuration
2. Verify API connectivity in the logs
3. Check if maintenance windows are affecting updates

### Authentication Issues

1. Verify username and password are correct
2. Check if your Klereo account is active
3. Ensure you can log in to the Klereo web interface

## API Rate Limits

The add-on respects Klereo's API rate limits:

- JWT tokens are cached for 55 minutes
- Pool index data is cached for ~4 hours
- Pool details are cached for ~10 minutes

These limits are built into the add-on to prevent API rate limiting.

## Maintenance Windows

Klereo has scheduled maintenance windows:

- **Sunday**: 01:45 - 04:45
- **Tuesday-Saturday**: 01:30 - 01:35

During these times, the add-on will pause API requests and resume automatically.

## Security

- Passwords are securely stored in Home Assistant's configuration
- API tokens are cached in memory only
- All communications use HTTPS
- The add-on runs with limited system permissions

## Performance

- Minimal CPU usage during normal operation
- Memory usage typically under 50MB
- Network usage depends on number of pools and update frequency
- Efficient caching reduces API calls

## Support

For support, please:

1. Check the troubleshooting section
2. Review the add-on logs
3. Visit the GitHub repository for issues
4. Contact Klereo support for API-related issues