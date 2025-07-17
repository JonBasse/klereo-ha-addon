#!/usr/bin/env python3
"""
Home Assistant Integration for Klereo Pool Manager
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from klereo_api import KlereoAPI

class HomeAssistantIntegration:
    """Home Assistant integration for Klereo pools"""
    
    def __init__(self, ha_url: str, ha_token: str, api_client: KlereoAPI, logger: Optional[logging.Logger] = None):
        """Initialize Home Assistant integration"""
        self.ha_url = ha_url.rstrip('/')
        self.ha_token = ha_token
        self.api_client = api_client
        self.logger = logger or logging.getLogger(__name__)
        
        # Device and entity tracking
        self.registered_devices = {}
        self.registered_entities = {}
        
        # Session for HTTP requests
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            headers = {
                'Authorization': f'Bearer {self.ha_token}',
                'Content-Type': 'application/json'
            }
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session
    
    async def _make_ha_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[Dict]:
        """Make request to Home Assistant API"""
        
        session = await self._get_session()
        url = f"{self.ha_url}/api/{endpoint}"
        
        try:
            if method.upper() == 'GET':
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
            elif method.upper() == 'POST':
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
            
            self.logger.error(f"Home Assistant API error: {response.status} for {endpoint}")
            return None
            
        except Exception as e:
            self.logger.error(f"Home Assistant request failed: {e}")
            return None
    
    def _generate_device_id(self, pool_id: str) -> str:
        """Generate unique device ID for pool"""
        return f"klereo_pool_{pool_id}"
    
    def _generate_entity_id(self, pool_id: str, probe_name: str) -> str:
        """Generate unique entity ID for pool probe"""
        sanitized_name = probe_name.lower().replace(' ', '_').replace('-', '_')
        return f"sensor.klereo_{pool_id}_{sanitized_name}"
    
    async def register_device(self, pool_id: str, pool_name: str) -> bool:
        """Register pool device in Home Assistant"""
        
        device_id = self._generate_device_id(pool_id)
        
        if device_id in self.registered_devices:
            return True
        
        device_data = {
            'device_id': device_id,
            'name': f"Klereo Pool: {pool_name}",
            'model': 'Klereo Pool System',
            'manufacturer': 'Klereo',
            'sw_version': '1.0.0',
            'identifiers': [[device_id, pool_id]],
            'via_device': 'klereo_addon'
        }
        
        # Register device via Home Assistant device registry
        response = await self._make_ha_request('device_registry', method='POST', data=device_data)
        
        if response:
            self.registered_devices[device_id] = {
                'pool_id': pool_id,
                'pool_name': pool_name,
                'registered_at': datetime.now()
            }
            self.logger.info(f"Device registered: {pool_name} (ID: {device_id})")
            return True
        
        self.logger.error(f"Failed to register device: {pool_name}")
        return False
    
    async def register_sensor_entity(self, pool_id: str, probe_data: Dict) -> bool:
        """Register sensor entity for pool probe"""
        
        device_id = self._generate_device_id(pool_id)
        entity_id = self._generate_entity_id(pool_id, probe_data['name'])
        
        if entity_id in self.registered_entities:
            return True
        
        entity_data = {
            'entity_id': entity_id,
            'name': f"{probe_data['name']}",
            'device_id': device_id,
            'state_class': 'measurement',
            'unit_of_measurement': probe_data.get('unit', ''),
            'device_class': self._get_device_class(probe_data),
            'icon': self._get_icon(probe_data),
            'unique_id': f"klereo_{pool_id}_{probe_data['logicalId']}"
        }
        
        # Register entity via Home Assistant entity registry
        response = await self._make_ha_request('entity_registry', method='POST', data=entity_data)
        
        if response:
            self.registered_entities[entity_id] = {
                'pool_id': pool_id,
                'probe_data': probe_data,
                'registered_at': datetime.now()
            }
            self.logger.info(f"Sensor registered: {probe_data['name']} (ID: {entity_id})")
            return True
        
        self.logger.error(f"Failed to register sensor: {probe_data['name']}")
        return False
    
    def _get_device_class(self, probe_data: Dict) -> Optional[str]:
        """Get appropriate device class for probe"""
        
        probe_type = probe_data.get('type', '').lower()
        probe_name = probe_data.get('name', '').lower()
        
        if 'temperature' in probe_name or 'temp' in probe_name:
            return 'temperature'
        elif 'ph' in probe_name:
            return None  # pH doesn't have a specific device class
        elif 'chlorine' in probe_name or 'cl' in probe_name:
            return None  # Chlorine doesn't have a specific device class
        elif 'orp' in probe_name or 'redox' in probe_name:
            return None  # ORP doesn't have a specific device class
        elif 'level' in probe_name or 'water' in probe_name:
            return None  # Water level doesn't have a specific device class
        
        return None
    
    def _get_icon(self, probe_data: Dict) -> str:
        """Get appropriate icon for probe"""
        
        probe_name = probe_data.get('name', '').lower()
        
        if 'temperature' in probe_name or 'temp' in probe_name:
            return 'mdi:thermometer'
        elif 'ph' in probe_name:
            return 'mdi:ph'
        elif 'chlorine' in probe_name or 'cl' in probe_name:
            return 'mdi:water-percent'
        elif 'orp' in probe_name or 'redox' in probe_name:
            return 'mdi:alpha-r-circle'
        elif 'level' in probe_name or 'water' in probe_name:
            return 'mdi:waves'
        
        return 'mdi:gauge'
    
    async def update_sensor_state(self, pool_id: str, probe_data: Dict) -> bool:
        """Update sensor state in Home Assistant"""
        
        entity_id = self._generate_entity_id(pool_id, probe_data['name'])
        
        if entity_id not in self.registered_entities:
            # Register entity if not exists
            await self.register_sensor_entity(pool_id, probe_data)
        
        state_data = {
            'entity_id': entity_id,
            'state': probe_data.get('filteredValue', 0),
            'attributes': {
                'unit_of_measurement': probe_data.get('unit', ''),
                'friendly_name': probe_data.get('name', ''),
                'device_class': self._get_device_class(probe_data),
                'last_updated': datetime.now().isoformat()
            }
        }
        
        # Update state via Home Assistant states API
        response = await self._make_ha_request(f"states/{entity_id}", method='POST', data=state_data)
        
        if response:
            self.logger.debug(f"State updated: {probe_data['name']} = {probe_data.get('filteredValue', 0)}")
            return True
        
        self.logger.error(f"Failed to update state: {probe_data['name']}")
        return False
    
    async def discover_and_register_pools(self) -> bool:
        """Discover all pools and register them as devices"""
        
        pools = self.api_client.get_pools()
        if not pools:
            self.logger.error("No pools found")
            return False
        
        success_count = 0
        
        for pool_id, pool_name in pools.items():
            # Register device
            if await self.register_device(pool_id, pool_name):
                success_count += 1
                
                # Get and register sensors for this pool
                probes = self.api_client.get_pool_probes(pool_id)
                if probes:
                    for probe in probes:
                        await self.register_sensor_entity(pool_id, probe)
        
        self.logger.info(f"Successfully registered {success_count}/{len(pools)} pools")
        return success_count > 0
    
    async def update_all_sensors(self) -> bool:
        """Update all sensor states"""
        
        pools = self.api_client.get_pools()
        if not pools:
            return False
        
        success_count = 0
        
        for pool_id, pool_name in pools.items():
            probes = self.api_client.get_pool_probes(pool_id)
            if probes:
                for probe in probes:
                    if await self.update_sensor_state(pool_id, probe):
                        success_count += 1
        
        self.logger.debug(f"Updated {success_count} sensors")
        return success_count > 0
    
    async def test_ha_connection(self) -> bool:
        """Test Home Assistant connection"""
        
        try:
            response = await self._make_ha_request('config')
            if response:
                self.logger.info("Home Assistant connection test successful")
                return True
            else:
                self.logger.error("Home Assistant connection test failed")
                return False
        except Exception as e:
            self.logger.error(f"Home Assistant connection test failed: {e}")
            return False
    
    async def cleanup(self) -> None:
        """Clean up resources"""
        if self.session and not self.session.closed:
            await self.session.close()

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        logging.basicConfig(level=logging.DEBUG)
        
        # Initialize API client
        api = KlereoAPI("username", "password")
        
        # Initialize Home Assistant integration
        ha_integration = HomeAssistantIntegration(
            ha_url="http://supervisor/core",
            ha_token="your_token_here",
            api_client=api
        )
        
        # Test connections
        if api.test_connection():
            print("✓ Klereo API connection successful")
            
            if await ha_integration.test_ha_connection():
                print("✓ Home Assistant connection successful")
                
                # Discover and register pools
                if await ha_integration.discover_and_register_pools():
                    print("✓ Pool discovery and registration successful")
                    
                    # Update all sensors
                    if await ha_integration.update_all_sensors():
                        print("✓ Sensor update successful")
                
        await ha_integration.cleanup()
    
    asyncio.run(main())