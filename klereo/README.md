# Klereo Pool Manager Add-on for Home Assistant

This add-on integrates Klereo pool management systems with Home Assistant, allowing you to monitor and control your pool equipment directly from your Home Assistant dashboard.

## Features

- **Real-time Pool Monitoring**: Monitor pH, temperature, chlorine levels, and other pool parameters
- **Automatic Updates**: Configurable update intervals for sensor data
- **Device Discovery**: Automatically discovers and registers all pools from your Klereo account
- **Home Assistant Integration**: Native Home Assistant entities for seamless dashboard integration
- **Multi-Pool Support**: Supports multiple pools in a single Klereo account

## Installation

1. Add this repository to your Home Assistant Add-on store
2. Install the "Klereo Pool Manager" add-on
3. Configure the add-on with your Klereo credentials
4. Start the add-on

## Configuration

### Required Settings

- **Klereo Username**: Your Klereo.fr account username
- **Klereo Password**: Your Klereo.fr account password

### Optional Settings

- **Update Interval**: How often to update sensor data (300-3600 seconds, default: 600)
- **Log Level**: Logging verbosity (debug, info, warning, error, default: info)

### Example Configuration

```yaml
klereo_username: "your_username"
klereo_password: "your_password"
update_interval: 600
log_level: "info"
```

## Usage

Once configured and started, the add-on will:

1. **Discover Pools**: Automatically find all pools in your Klereo account
2. **Register Devices**: Create Home Assistant devices for each pool
3. **Create Sensors**: Add sensor entities for each pool parameter (pH, temperature, etc.)
4. **Update Data**: Regularly update sensor values based on your configured interval

### Home Assistant Entities

The add-on creates the following types of entities:

- **Sensor Entities**: Pool parameters like pH, temperature, chlorine levels
- **Device Entities**: One device per pool for organization

Entity naming follows the pattern: `sensor.klereo_{pool_id}_{parameter_name}`

Example entities:
- `sensor.klereo_12345_ph`
- `sensor.klereo_12345_temperature`
- `sensor.klereo_12345_chlorine`

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check your Klereo credentials and internet connection
2. **No Sensors Created**: Verify that your pools have active probes and data
3. **Entities Not Updating**: Check the update interval and add-on logs

### Logging

Enable debug logging to troubleshoot issues:

```yaml
log_level: "debug"
```

Logs can be viewed in the Home Assistant Add-on logs section.

### Maintenance Windows

The Klereo service has scheduled maintenance windows. During these times, the add-on will automatically pause API requests and resume once maintenance is complete.

## API Limitations

- **JWT Token Refresh**: 55 minutes
- **Index Data Refresh**: 3 hours 55 minutes
- **Pool Details Refresh**: 9 minutes 50 seconds

These intervals are optimized to balance data freshness with API rate limits.

## Support

For issues and feature requests, please visit:
- [GitHub Repository](https://github.com/JonBasse/klereo-ha-addon)
- [Klereo Official Documentation](https://klereo.fr)

## License

This add-on is licensed under the GPL-3.0 License.

## Credits

This Home Assistant add-on was inspired by and adapted from the original Jeedom Klereo plugin by Michel_F.

**Special thanks to:**
- **Michel_F** for the original Jeedom Klereo plugin that provided the foundation for this Home Assistant integration
- **MrWaloo** for the [jeedom-klereo repository](https://github.com/MrWaloo/jeedom-klereo) that served as inspiration for the API implementation
- **Klereo** for providing the pool management system and API

This add-on represents a complete conversion from the original Jeedom plugin to the Home Assistant add-on architecture, maintaining compatibility with the Klereo Connect API.