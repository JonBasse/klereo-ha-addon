# Klereo Pool Manager Add-on Repository

This repository contains the Home Assistant add-on for Klereo pool management systems.

## Add-ons

### Klereo Pool Manager

Monitor and control your Klereo pool system directly from Home Assistant.

**Features:**
- Real-time pool parameter monitoring (pH, temperature, chlorine, etc.)
- Automatic device and sensor discovery
- Multi-pool support
- Configurable update intervals
- Native Home Assistant integration

## Installation

1. Add this repository to your Home Assistant Add-on store:
   - Go to **Supervisor** → **Add-on Store** → **⋮** → **Repositories**
   - Add: `https://github.com/JonBasse/klereo-ha-addon`

2. Install the "Klereo Pool Manager" add-on
3. Configure with your Klereo credentials
4. Start the add-on

## Configuration

Minimum required configuration:

```yaml
klereo_username: "your_username"
klereo_password: "your_password"
```

## Support

For issues and feature requests, please visit the [GitHub repository](https://github.com/JonBasse/klereo-ha-addon).

## License

This add-on is licensed under the GPL-3.0 License.

## Credits

This Home Assistant add-on was inspired by and adapted from the original Jeedom Klereo plugin by Michel_F. 

**Special thanks to:**
- **Michel_F** for the original Jeedom Klereo plugin that provided the foundation for this Home Assistant integration
- **MrWaloo** for the [jeedom-klereo repository](https://github.com/MrWaloo/jeedom-klereo) that served as inspiration for the API implementation
- **Klereo** for providing the pool management system and API

This add-on represents a complete conversion from the original Jeedom plugin to the Home Assistant add-on architecture, maintaining compatibility with the Klereo Connect API.