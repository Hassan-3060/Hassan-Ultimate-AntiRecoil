"""
Dynamic Weapon Loader for Hassan Ultimate Anti-Recoil
Universal weapon profile management and loading system
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import importlib

from src.weapons.bo6_weapons import WeaponProfile, get_all_bo6_weapons
from src.weapons.valorant_weapons import get_all_valorant_weapons
from src.weapons.cs2_weapons import get_all_cs2_weapons


class WeaponLoader:
    """
    Dynamic weapon profile loader and manager.
    
    Features:
    - Multi-game weapon profile support
    - Dynamic loading from modules and files
    - Custom weapon profile creation
    - Profile caching and optimization
    - Import/Export functionality
    - Real-time profile updates
    """
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Weapon profile cache
        self.weapon_cache: Dict[str, Dict[str, WeaponProfile]] = {}
        self.custom_weapons: Dict[str, WeaponProfile] = {}
        
        # Game modules mapping
        self.game_modules = {
            "cod_bo6": "src.weapons.bo6_weapons",
            "valorant": "src.weapons.valorant_weapons",
            "cs2": "src.weapons.cs2_weapons"
        }
        
        # Initialize loader
        self._load_all_weapons()
        self._load_custom_weapons()
        
        self.logger.info("Weapon loader initialized")
    
    def _load_all_weapons(self) -> None:
        """Load all weapon profiles from game modules."""
        try:
            # Load Black Ops 6 weapons
            self.weapon_cache["cod_bo6"] = get_all_bo6_weapons()
            self.logger.info(f"Loaded {len(self.weapon_cache['cod_bo6'])} BO6 weapons")
            
            # Load VALORANT weapons
            self.weapon_cache["valorant"] = get_all_valorant_weapons()
            self.logger.info(f"Loaded {len(self.weapon_cache['valorant'])} VALORANT weapons")
            
            # Load CS2 weapons
            self.weapon_cache["cs2"] = get_all_cs2_weapons()
            self.logger.info(f"Loaded {len(self.weapon_cache['cs2'])} CS2 weapons")
            
            # Total weapons loaded
            total_weapons = sum(len(weapons) for weapons in self.weapon_cache.values())
            self.logger.info(f"Total weapons loaded: {total_weapons}")
            
        except Exception as e:
            self.logger.error(f"Error loading weapon profiles: {e}")
    
    def _load_custom_weapons(self) -> None:
        """Load custom weapon profiles from files."""
        try:
            custom_dir = Path("config/custom_weapons")
            if not custom_dir.exists():
                return
            
            for file_path in custom_dir.glob("*.json"):
                try:
                    with open(file_path, 'r') as f:
                        weapon_data = json.load(f)
                    
                    # Convert to WeaponProfile object
                    weapon = WeaponProfile(**weapon_data)
                    self.custom_weapons[weapon.name] = weapon
                    
                    self.logger.debug(f"Loaded custom weapon: {weapon.name}")
                    
                except Exception as e:
                    self.logger.error(f"Error loading custom weapon {file_path}: {e}")
            
            if self.custom_weapons:
                self.logger.info(f"Loaded {len(self.custom_weapons)} custom weapons")
            
        except Exception as e:
            self.logger.error(f"Error loading custom weapons: {e}")
    
    def get_weapon(self, game: str, weapon_name: str) -> Optional[WeaponProfile]:
        """Get a specific weapon profile."""
        try:
            # Check cache first
            if game in self.weapon_cache:
                weapon = self.weapon_cache[game].get(weapon_name.lower())
                if weapon:
                    return weapon
            
            # Check custom weapons
            weapon = self.custom_weapons.get(weapon_name.lower())
            if weapon:
                return weapon
            
            # Try to load dynamically
            if game in self.game_modules:
                try:
                    module = importlib.import_module(self.game_modules[game])
                    if hasattr(module, 'get_weapon_by_name'):
                        weapon = module.get_weapon_by_name(weapon_name)
                        if weapon:
                            # Cache for future use
                            if game not in self.weapon_cache:
                                self.weapon_cache[game] = {}
                            self.weapon_cache[game][weapon_name.lower()] = weapon
                            return weapon
                except ImportError:
                    pass
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting weapon {weapon_name} for {game}: {e}")
            return None
    
    def get_weapons_for_game(self, game: str) -> Dict[str, WeaponProfile]:
        """Get all weapons for a specific game."""
        try:
            weapons = {}
            
            # Get from cache
            if game in self.weapon_cache:
                weapons.update(self.weapon_cache[game])
            
            # Add custom weapons for this game
            for weapon_name, weapon in self.custom_weapons.items():
                if hasattr(weapon, 'game') and weapon.game == game:
                    weapons[weapon_name] = weapon
            
            return weapons
            
        except Exception as e:
            self.logger.error(f"Error getting weapons for game {game}: {e}")
            return {}
    
    def get_all_games(self) -> List[str]:
        """Get list of all supported games."""
        games = list(self.weapon_cache.keys())
        
        # Add games from custom weapons
        for weapon in self.custom_weapons.values():
            if hasattr(weapon, 'game') and weapon.game not in games:
                games.append(weapon.game)
        
        return sorted(games)
    
    def get_weapon_classes_for_game(self, game: str) -> List[str]:
        """Get all weapon classes for a specific game."""
        try:
            weapons = self.get_weapons_for_game(game)
            classes = set()
            
            for weapon in weapons.values():
                classes.add(weapon.weapon_class)
            
            return sorted(list(classes))
            
        except Exception as e:
            self.logger.error(f"Error getting weapon classes for {game}: {e}")
            return []
    
    def get_weapons_by_class(self, game: str, weapon_class: str) -> Dict[str, WeaponProfile]:
        """Get weapons by class for a specific game."""
        try:
            weapons = self.get_weapons_for_game(game)
            filtered_weapons = {}
            
            for name, weapon in weapons.items():
                if weapon.weapon_class.lower() == weapon_class.lower():
                    filtered_weapons[name] = weapon
            
            return filtered_weapons
            
        except Exception as e:
            self.logger.error(f"Error getting weapons by class {weapon_class} for {game}: {e}")
            return {}
    
    def search_weapons(self, query: str, game: Optional[str] = None) -> Dict[str, WeaponProfile]:
        """Search for weapons by name or display name."""
        try:
            results = {}
            query_lower = query.lower()
            
            # Search in specific game
            if game:
                weapons = self.get_weapons_for_game(game)
                for name, weapon in weapons.items():
                    if (query_lower in name.lower() or 
                        query_lower in weapon.display_name.lower()):
                        results[f"{game}:{name}"] = weapon
            else:
                # Search in all games
                for game_name in self.get_all_games():
                    weapons = self.get_weapons_for_game(game_name)
                    for name, weapon in weapons.items():
                        if (query_lower in name.lower() or 
                            query_lower in weapon.display_name.lower()):
                            results[f"{game_name}:{name}"] = weapon
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error searching weapons: {e}")
            return {}
    
    def create_custom_weapon(self, weapon_data: Dict[str, Any]) -> bool:
        """Create a custom weapon profile."""
        try:
            # Validate required fields
            required_fields = ['name', 'display_name', 'weapon_class']
            for field in required_fields:
                if field not in weapon_data:
                    self.logger.error(f"Missing required field: {field}")
                    return False
            
            # Set default values
            defaults = {
                'damage': 75,
                'fire_rate': 75,
                'accuracy': 75,
                'range': 75,
                'mobility': 75,
                'control': 75,
                'vertical_pattern': [-3.0, -4.0, -3.5, -3.0, -2.5],
                'horizontal_pattern': [0.0, -1.0, 1.0, -0.5, 0.5],
                'timing_pattern': [0.1, 0.1, 0.1, 0.1, 0.1],
                'base_sensitivity': 1.0,
                'ads_sensitivity': 0.8
            }
            
            # Merge with defaults
            for key, value in defaults.items():
                weapon_data.setdefault(key, value)
            
            # Create weapon profile
            weapon = WeaponProfile(**weapon_data)
            
            # Add to custom weapons
            self.custom_weapons[weapon.name.lower()] = weapon
            
            # Save to file
            self._save_custom_weapon(weapon)
            
            self.logger.info(f"Created custom weapon: {weapon.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating custom weapon: {e}")
            return False
    
    def _save_custom_weapon(self, weapon: WeaponProfile) -> None:
        """Save custom weapon to file."""
        try:
            custom_dir = Path("config/custom_weapons")
            custom_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = custom_dir / f"{weapon.name}.json"
            
            with open(file_path, 'w') as f:
                json.dump(asdict(weapon), f, indent=2)
            
            self.logger.debug(f"Saved custom weapon to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving custom weapon: {e}")
    
    def delete_custom_weapon(self, weapon_name: str) -> bool:
        """Delete a custom weapon profile."""
        try:
            weapon_name_lower = weapon_name.lower()
            
            if weapon_name_lower not in self.custom_weapons:
                self.logger.error(f"Custom weapon not found: {weapon_name}")
                return False
            
            # Remove from cache
            del self.custom_weapons[weapon_name_lower]
            
            # Remove file
            custom_dir = Path("config/custom_weapons")
            file_path = custom_dir / f"{weapon_name}.json"
            
            if file_path.exists():
                file_path.unlink()
            
            self.logger.info(f"Deleted custom weapon: {weapon_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting custom weapon: {e}")
            return False
    
    def export_weapon(self, game: str, weapon_name: str, file_path: str) -> bool:
        """Export a weapon profile to file."""
        try:
            weapon = self.get_weapon(game, weapon_name)
            if not weapon:
                self.logger.error(f"Weapon not found: {weapon_name}")
                return False
            
            with open(file_path, 'w') as f:
                json.dump(asdict(weapon), f, indent=2)
            
            self.logger.info(f"Exported weapon {weapon_name} to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting weapon: {e}")
            return False
    
    def import_weapon(self, file_path: str, as_custom: bool = True) -> bool:
        """Import a weapon profile from file."""
        try:
            with open(file_path, 'r') as f:
                weapon_data = json.load(f)
            
            if as_custom:
                return self.create_custom_weapon(weapon_data)
            else:
                # Import as regular weapon (would require game specification)
                weapon = WeaponProfile(**weapon_data)
                game = weapon_data.get('game', 'custom')
                
                if game not in self.weapon_cache:
                    self.weapon_cache[game] = {}
                
                self.weapon_cache[game][weapon.name.lower()] = weapon
                
                self.logger.info(f"Imported weapon {weapon.name} for game {game}")
                return True
            
        except Exception as e:
            self.logger.error(f"Error importing weapon: {e}")
            return False
    
    def get_recommended_settings(self, game: str, weapon_name: str) -> Dict[str, Any]:
        """Get recommended settings for a weapon."""
        try:
            weapon = self.get_weapon(game, weapon_name)
            if not weapon:
                return {}
            
            # Get game-specific recommendations
            if game in self.game_modules:
                try:
                    module = importlib.import_module(self.game_modules[game])
                    if hasattr(module, 'get_recommended_settings'):
                        return module.get_recommended_settings(weapon_name)
                except ImportError:
                    pass
            
            # Default recommendations
            return {
                "base_sensitivity": weapon.base_sensitivity,
                "ads_sensitivity": weapon.ads_sensitivity,
                "randomization": 0.1,
                "security_level": "medium"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting recommended settings: {e}")
            return {}
    
    def get_weapon_stats(self) -> Dict[str, Any]:
        """Get weapon loading statistics."""
        try:
            stats = {
                'total_games': len(self.weapon_cache),
                'total_weapons': sum(len(weapons) for weapons in self.weapon_cache.values()),
                'custom_weapons': len(self.custom_weapons),
                'games': {}
            }
            
            for game, weapons in self.weapon_cache.items():
                stats['games'][game] = {
                    'weapon_count': len(weapons),
                    'weapon_classes': len(self.get_weapon_classes_for_game(game))
                }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting weapon stats: {e}")
            return {}
    
    def reload_weapons(self) -> bool:
        """Reload all weapon profiles."""
        try:
            self.weapon_cache.clear()
            self.custom_weapons.clear()
            
            self._load_all_weapons()
            self._load_custom_weapons()
            
            self.logger.info("Weapon profiles reloaded")
            return True
            
        except Exception as e:
            self.logger.error(f"Error reloading weapons: {e}")
            return False
    
    def validate_weapon_profile(self, weapon_data: Dict[str, Any]) -> List[str]:
        """Validate a weapon profile data structure."""
        errors = []
        
        try:
            required_fields = ['name', 'display_name', 'weapon_class']
            for field in required_fields:
                if field not in weapon_data:
                    errors.append(f"Missing required field: {field}")
            
            # Validate pattern arrays
            pattern_fields = ['vertical_pattern', 'horizontal_pattern', 'timing_pattern']
            for field in pattern_fields:
                if field in weapon_data:
                    if not isinstance(weapon_data[field], list):
                        errors.append(f"{field} must be a list")
                    elif not weapon_data[field]:
                        errors.append(f"{field} cannot be empty")
            
            # Validate numeric ranges
            numeric_fields = {
                'damage': (1, 200),
                'fire_rate': (1, 100),
                'accuracy': (1, 100),
                'range': (1, 100),
                'mobility': (1, 100),
                'control': (1, 100),
                'base_sensitivity': (0.1, 10.0),
                'ads_sensitivity': (0.1, 10.0)
            }
            
            for field, (min_val, max_val) in numeric_fields.items():
                if field in weapon_data:
                    value = weapon_data[field]
                    if not isinstance(value, (int, float)):
                        errors.append(f"{field} must be a number")
                    elif not (min_val <= value <= max_val):
                        errors.append(f"{field} must be between {min_val} and {max_val}")
            
        except Exception as e:
            errors.append(f"Validation error: {e}")
        
        return errors