#!/usr/bin/env python3
"""
Klereo API Client for Home Assistant
Converted from PHP Jeedom plugin
"""

import requests
import json
import hashlib
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

class KlereoAPI:
    """Klereo API client for pool management"""
    
    # API Configuration
    API_ROOT = "https://connect.klereo.fr/php/"
    WEB_VERSION = "393-J"
    USER_AGENT = "Home Assistant Add-on"
    
    # Update intervals
    JWT_REFRESH_INTERVAL = 55 * 60  # 55 minutes
    INDEX_REFRESH_INTERVAL = 3 * 3600 + 55 * 60  # 3 hours 55 minutes
    POOL_DETAILS_REFRESH_INTERVAL = 9 * 60 + 50  # 9 minutes 50 seconds
    
    # Maintenance windows (day_of_week: {from: HHMM, to: HHMM})
    MAINTENANCE_WINDOWS = {
        0: {'from': 145, 'to': 445},   # Sunday
        2: {'from': 130, 'to': 135},   # Tuesday
        3: {'from': 130, 'to': 135},   # Wednesday
        4: {'from': 130, 'to': 135},   # Thursday
        5: {'from': 130, 'to': 135},   # Friday
        6: {'from': 130, 'to': 135},   # Saturday
    }
    
    def __init__(self, username: str, password: str, logger: Optional[logging.Logger] = None):
        """Initialize Klereo API client"""
        self.username = username
        self.password = password
        self.logger = logger or logging.getLogger(__name__)
        
        # Cache for API data
        self.cache = {}
        
        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def _get_now(self) -> datetime:
        """Get current datetime"""
        return datetime.now()
    
    def _is_maintenance_ongoing(self) -> bool:
        """Check if maintenance is currently ongoing"""
        now = self._get_now()
        day_of_week = now.weekday()  # 0=Monday, 6=Sunday
        current_time = now.hour * 100 + now.minute
        
        # Convert Python weekday to match PHP (0=Sunday)
        php_day = 0 if day_of_week == 6 else day_of_week + 1
        
        if php_day in self.MAINTENANCE_WINDOWS:
            maintenance = self.MAINTENANCE_WINDOWS[php_day]
            if maintenance['from'] <= current_time <= maintenance['to']:
                self.logger.info(f"Maintenance ongoing: {maintenance['from']:04d}-{maintenance['to']:04d}")
                return True
        
        return False
    
    def _cache_get(self, key: str, default: Any = None) -> Any:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if entry['expires'] > time.time():
                return entry['value']
            else:
                del self.cache[key]
        return default
    
    def _cache_set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL"""
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None, 
                     headers: Optional[Dict] = None) -> Tuple[Optional[Dict], Optional[Dict]]:
        """Make HTTP request to Klereo API"""
        
        if self._is_maintenance_ongoing():
            self.logger.warning("Maintenance ongoing, skipping request")
            return None, None
        
        url = f"{self.API_ROOT}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check HTTP status
            if response.status_code != 200:
                self.logger.error(f"HTTP {response.status_code} error for {endpoint}")
                return None, None
            
            # Parse JSON response
            try:
                body = response.json()
            except json.JSONDecodeError:
                self.logger.error(f"Invalid JSON response from {endpoint}")
                return None, None
            
            # Check for API error
            if isinstance(body, dict) and 'error' in body:
                error_msg = body.get('detail', 'Unknown error')
                self.logger.error(f"API error: {error_msg}")
                return None, None
            
            return response.headers, body
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {endpoint}: {e}")
            return None, None
    
    def get_jwt_token(self) -> Optional[str]:
        """Get JWT authentication token"""
        
        # Check cache first
        cached_token = self._cache_get('jwt_token')
        if cached_token:
            return cached_token
        
        # Prepare login data
        password_hash = hashlib.sha1(self.password.encode()).hexdigest()
        login_data = {
            'login': self.username,
            'password': password_hash,
            'version': self.WEB_VERSION
        }
        
        # Make login request
        headers, body = self._make_request('GetJWT.php', method='POST', data=login_data)
        
        if not body or 'jwt' not in body:
            self.logger.error("Failed to get JWT token")
            return None
        
        jwt_token = body['jwt']
        
        # Cache token (55 minutes TTL)
        self._cache_set('jwt_token', jwt_token, self.JWT_REFRESH_INTERVAL)
        
        self.logger.debug("JWT token obtained successfully")
        return jwt_token
    
    def get_index(self) -> Optional[List[Dict]]:
        """Get list of pools from API"""
        
        # Check cache first
        cached_index = self._cache_get('index')
        if cached_index:
            return cached_index
        
        # Get JWT token
        jwt_token = self.get_jwt_token()
        if not jwt_token:
            return None
        
        # Make index request
        headers = {'Authorization': f'Bearer {jwt_token}'}
        response_headers, body = self._make_request('GetIndex.php', headers=headers)
        
        if not body or 'response' not in body:
            self.logger.error("Failed to get index")
            return None
        
        index_data = body['response']
        
        # Cache index data
        self._cache_set('index', index_data, self.INDEX_REFRESH_INTERVAL)
        
        self.logger.debug(f"Index data obtained: {len(index_data)} pools")
        return index_data
    
    def get_pools(self) -> Optional[Dict[str, str]]:
        """Get pools as dict {pool_id: pool_name}"""
        
        index = self.get_index()
        if not index:
            return None
        
        pools = {}
        for pool in index:
            pool_id = pool.get('idSystem')
            pool_name = pool.get('poolNickname')
            if pool_id and pool_name:
                pools[pool_id] = pool_name
        
        return pools
    
    def get_pool_details(self, pool_id: str) -> Optional[Dict]:
        """Get detailed information for a specific pool"""
        
        cache_key = f'pool_details_{pool_id}'
        cached_details = self._cache_get(cache_key)
        if cached_details:
            return cached_details
        
        # Get JWT token
        jwt_token = self.get_jwt_token()
        if not jwt_token:
            return None
        
        # Make pool details request
        headers = {'Authorization': f'Bearer {jwt_token}'}
        data = {'idSystem': pool_id}
        
        response_headers, body = self._make_request('GetPoolDetails.php', method='POST', 
                                                   data=data, headers=headers)
        
        if not body or 'response' not in body:
            self.logger.error(f"Failed to get pool details for {pool_id}")
            return None
        
        pool_details = body['response']
        
        # Cache pool details
        self._cache_set(cache_key, pool_details, self.POOL_DETAILS_REFRESH_INTERVAL)
        
        self.logger.debug(f"Pool details obtained for {pool_id}")
        return pool_details
    
    def get_pool_probes(self, pool_id: str) -> Optional[List[Dict]]:
        """Get probe data for a specific pool"""
        
        pool_details = self.get_pool_details(pool_id)
        if not pool_details:
            return None
        
        # Extract probes from pool details
        probes = []
        
        # This would need to be adapted based on actual API response structure
        # The PHP code suggests there are probe values with filteredValue
        if 'probes' in pool_details:
            for probe in pool_details['probes']:
                probe_data = {
                    'logicalId': probe.get('logicalId'),
                    'name': probe.get('name'),
                    'filteredValue': probe.get('filteredValue'),
                    'unit': probe.get('unit'),
                    'type': probe.get('type')
                }
                probes.append(probe_data)
        
        return probes
    
    def test_connection(self) -> bool:
        """Test if API connection is working"""
        
        try:
            jwt_token = self.get_jwt_token()
            if not jwt_token:
                return False
            
            pools = self.get_pools()
            return pools is not None
            
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
        self.logger.info("Cache cleared")

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    # This would normally come from config
    api = KlereoAPI("your_username", "your_password")
    
    # Test connection
    if api.test_connection():
        print("✓ Connection successful")
        
        # Get pools
        pools = api.get_pools()
        if pools:
            print(f"✓ Found {len(pools)} pools:")
            for pool_id, pool_name in pools.items():
                print(f"  - {pool_name} (ID: {pool_id})")
                
                # Get pool details
                details = api.get_pool_details(pool_id)
                if details:
                    print(f"    ✓ Pool details retrieved")
                    
                    # Get probes
                    probes = api.get_pool_probes(pool_id)
                    if probes:
                        print(f"    ✓ Found {len(probes)} probes")
                        for probe in probes:
                            print(f"      - {probe['name']}: {probe['filteredValue']} {probe['unit']}")
    else:
        print("✗ Connection failed")