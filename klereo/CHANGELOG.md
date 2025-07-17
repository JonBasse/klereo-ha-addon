# Changelog

All notable changes to the Klereo Pool Manager add-on will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-01-17

### Fixed
- Fixed Docker base image compatibility issues
- Fixed Python PEP 668 externally-managed-environment error
- Fixed BUILD_ARCH undefined variable issue
- Fixed add-on startup and configuration loading
- Replaced bashio dependency with direct JSON parsing

### Changed
- Removed confusing Home Assistant URL and token configuration options
- Simplified configuration to only essential Klereo credentials
- Add-ons now automatically use Home Assistant supervisor API
- Improved startup logging and error handling

## [1.0.0] - 2025-01-17

### Added
- Initial release of Klereo Pool Manager add-on for Home Assistant
- Full conversion from Jeedom plugin to Home Assistant add-on architecture
- Python-based API client for Klereo.fr service
- JWT authentication with automatic token refresh
- Support for multiple pools per account
- Automatic device and sensor discovery
- Real-time pool parameter monitoring (pH, temperature, chlorine, etc.)
- Configurable update intervals (300-3600 seconds)
- Maintenance window handling
- Comprehensive logging and error handling
- Multi-language support preparation
- Home Assistant native entity integration
- Automatic device class and icon assignment
- Efficient API caching to respect rate limits
- AppArmor security profile
- Docker containerization with multi-architecture support

### Features
- **API Integration**: Complete Klereo API client with authentication and data retrieval
- **Device Discovery**: Automatic discovery and registration of pools as Home Assistant devices
- **Sensor Management**: Dynamic creation and updating of sensor entities
- **Configuration**: User-friendly configuration interface with validation
- **Monitoring**: Real-time pool parameter monitoring with automatic updates
- **Logging**: Comprehensive logging with configurable levels
- **Security**: Secure credential handling and API communication
- **Performance**: Efficient caching and resource management

### Supported Pool Parameters
- pH Level
- Water Temperature
- Chlorine Level
- ORP/Redox Potential
- Water Level
- Additional custom probes

### Technical Details
- **Base Image**: Home Assistant Python 3.11 base images
- **Architecture Support**: armhf, armv7, aarch64, amd64, i386
- **API Endpoints**: GetJWT.php, GetIndex.php, GetPoolDetails.php
- **Update Intervals**: JWT (55min), Index (3h55min), Pool Details (9m50s)
- **Maintenance Windows**: Automatic handling of scheduled maintenance

### Documentation
- Complete README with installation and configuration instructions
- Detailed DOCS.md with advanced configuration and troubleshooting
- Configuration examples and automation samples
- Security and performance guidelines

### Security
- AppArmor security profile with restricted permissions
- Secure credential storage and handling
- HTTPS-only API communication
- Limited system access and privilege escalation prevention

### Known Limitations
- Requires active Klereo account and internet connectivity
- Subject to Klereo API rate limits and maintenance windows
- Pool control functionality not implemented in initial release
- Depends on Klereo service availability

### Migration from Jeedom
This add-on replaces the Jeedom Klereo plugin with equivalent functionality:
- All core API functionality preserved
- Configuration format adapted for Home Assistant
- Entity structure optimized for Home Assistant integration
- Improved error handling and logging
- Enhanced security and performance