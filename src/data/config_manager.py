"""
Configuration Manager for Hassan Ultimate Anti-Recoil
Comprehensive configuration management with validation and persistence
"""

import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
import yaml
import copy
from datetime import datetime


@dataclass
class ConfigSchema:
    """Configuration schema definition."""
    key: str
    type: type
    default: Any
    description: str
    required: bool = False
    validator: Optional[callable] = None


class ConfigManager:
    """
    Advanced configuration management system.
    
    Features:
    - Hierarchical configuration with inheritance
    - Real-time configuration updates
    - Configuration validation and type checking
    - Multiple format support (JSON, YAML)
    - Configuration backup and restore
    - Event-driven configuration changes
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Configuration directory
        if config_dir is None:
            config_dir = Path("config")
        else:
            config_dir = Path(config_dir)
        
        self.config_dir = config_dir
        self.config_dir.mkdir(exist_ok=True)
        
        # Configuration data
        self.config: Dict[str, Any] = {}
        self.default_config: Dict[str, Any] = {}
        self.schema: Dict[str, ConfigSchema] = {}
        
        # Change tracking
        self.change_callbacks: List[callable] = []
        self.dirty_keys: set = set()
        self.last_save_time: Optional[datetime] = None
        
        # Load configuration
        self._define_schema()
        self._load_default_config()
        self._load_user_config()
        
        self.logger.info("Configuration manager initialized")
    
    def _define_schema(self) -> None:
        """Define configuration schema."""
        try:
            schemas = {
                # Engine settings
                'engine.enabled': ConfigSchema(
                    'engine.enabled', bool, True, 
                    'Enable anti-recoil engine'
                ),
                'engine.sensitivity': ConfigSchema(
                    'engine.sensitivity', float, 1.0,
                    'Global sensitivity multiplier',
                    validator=lambda x: 0.1 <= x <= 10.0
                ),
                'engine.max_latency': ConfigSchema(
                    'engine.max_latency', float, 0.001,
                    'Maximum allowed latency in seconds',
                    validator=lambda x: 0.0001 <= x <= 0.01
                ),
                
                # AI settings
                'ai.enabled': ConfigSchema(
                    'ai.enabled', bool, True,
                    'Enable AI pattern recognition'
                ),
                'ai.learning_rate': ConfigSchema(
                    'ai.learning_rate', float, 0.1,
                    'AI learning rate',
                    validator=lambda x: 0.01 <= x <= 1.0
                ),
                'ai.min_samples': ConfigSchema(
                    'ai.min_samples', int, 50,
                    'Minimum samples for AI training',
                    validator=lambda x: 10 <= x <= 1000
                ),
                
                # Security settings
                'security.stealth_mode': ConfigSchema(
                    'security.stealth_mode', bool, True,
                    'Enable stealth mode'
                ),
                'security.randomization': ConfigSchema(
                    'security.randomization', float, 0.15,
                    'Movement randomization level',
                    validator=lambda x: 0.0 <= x <= 1.0
                ),
                'security.level': ConfigSchema(
                    'security.level', str, 'high',
                    'Security level (low, medium, high, maximum)',
                    validator=lambda x: x in ['low', 'medium', 'high', 'maximum']
                ),
                
                # GUI settings
                'gui.theme': ConfigSchema(
                    'gui.theme', str, 'dark',
                    'GUI theme (dark, light)',
                    validator=lambda x: x in ['dark', 'light']
                ),
                'gui.window_size': ConfigSchema(
                    'gui.window_size', list, [1200, 800],
                    'Main window size [width, height]'
                ),
                'gui.always_on_top': ConfigSchema(
                    'gui.always_on_top', bool, False,
                    'Keep window always on top'
                ),
                
                # Hotkeys
                'hotkeys.toggle_engine': ConfigSchema(
                    'hotkeys.toggle_engine', str, 'f1',
                    'Hotkey to toggle anti-recoil engine'
                ),
                'hotkeys.next_weapon': ConfigSchema(
                    'hotkeys.next_weapon', str, 'f2',
                    'Hotkey to cycle to next weapon'
                ),
                'hotkeys.calibrate': ConfigSchema(
                    'hotkeys.calibrate', str, 'f3',
                    'Hotkey to start calibration'
                ),
                
                # Game detection
                'games.auto_detect': ConfigSchema(
                    'games.auto_detect', bool, True,
                    'Enable automatic game detection'
                ),
                'games.scan_interval': ConfigSchema(
                    'games.scan_interval', float, 2.0,
                    'Game detection scan interval in seconds',
                    validator=lambda x: 0.5 <= x <= 10.0
                ),
                
                # Performance
                'performance.max_history_size': ConfigSchema(
                    'performance.max_history_size', int, 10000,
                    'Maximum performance history size',
                    validator=lambda x: 1000 <= x <= 100000
                ),
                'performance.metrics_interval': ConfigSchema(
                    'performance.metrics_interval', float, 1.0,
                    'Metrics collection interval in seconds',
                    validator=lambda x: 0.1 <= x <= 10.0
                ),
                
                # Logging
                'logging.level': ConfigSchema(
                    'logging.level', str, 'INFO',
                    'Logging level',
                    validator=lambda x: x in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
                ),
                'logging.file_enabled': ConfigSchema(
                    'logging.file_enabled', bool, True,
                    'Enable file logging'
                ),
                'logging.console_enabled': ConfigSchema(
                    'logging.console_enabled', bool, True,
                    'Enable console logging'
                ),
            }
            
            self.schema = schemas
            self.logger.debug(f"Defined {len(schemas)} configuration schemas")
            
        except Exception as e:
            self.logger.error(f"Error defining schema: {e}")
    
    def _load_default_config(self) -> None:
        """Load default configuration."""
        try:
            # Generate default config from schema
            for key, schema in self.schema.items():
                self._set_nested_value(self.default_config, key, schema.default)
            
            # Try to load from default config file
            default_file = self.config_dir / "default_settings.json"
            if default_file.exists():
                with open(default_file, 'r') as f:
                    file_defaults = json.load(f)
                    self._merge_config(self.default_config, file_defaults)
            
            # Initialize config with defaults
            self.config = copy.deepcopy(self.default_config)
            
            self.logger.info("Default configuration loaded")
            
        except Exception as e:
            self.logger.error(f"Error loading default config: {e}")
    
    def _load_user_config(self) -> None:
        """Load user configuration."""
        try:
            config_file = self.config_dir / "user_settings.json"
            
            if config_file.exists():
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                
                # Merge with current config
                self._merge_config(self.config, user_config)
                self.logger.info("User configuration loaded")
            else:
                self.logger.info("No user configuration found, using defaults")
            
            # Validate configuration
            self._validate_config()
            
        except Exception as e:
            self.logger.error(f"Error loading user config: {e}")
    
    def _validate_config(self) -> None:
        """Validate configuration against schema."""
        try:
            errors = []
            
            for key, schema in self.schema.items():
                try:
                    value = self.get(key)
                    
                    # Type validation
                    if not isinstance(value, schema.type):
                        if schema.type == float and isinstance(value, int):
                            # Allow int->float conversion
                            self.set(key, float(value))
                        else:
                            errors.append(f"Invalid type for {key}: expected {schema.type.__name__}, got {type(value).__name__}")
                            continue
                    
                    # Custom validator
                    if schema.validator and not schema.validator(value):
                        errors.append(f"Validation failed for {key}: {value}")
                        # Reset to default
                        self.set(key, schema.default)
                
                except KeyError:
                    if schema.required:
                        errors.append(f"Required configuration missing: {key}")
                        self.set(key, schema.default)
            
            if errors:
                self.logger.warning(f"Configuration validation errors: {errors}")
            else:
                self.logger.debug("Configuration validation passed")
            
        except Exception as e:
            self.logger.error(f"Error validating config: {e}")
    
    def _merge_config(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Merge source configuration into target."""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._merge_config(target[key], value)
            else:
                target[key] = value
    
    def _set_nested_value(self, config: Dict[str, Any], key: str, value: Any) -> None:
        """Set a nested configuration value."""
        keys = key.split('.')
        current = config
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def _get_nested_value(self, config: Dict[str, Any], key: str) -> Any:
        """Get a nested configuration value."""
        keys = key.split('.')
        current = config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                raise KeyError(f"Configuration key not found: {key}")
        
        return current
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            return self._get_nested_value(self.config, key)
        except KeyError:
            if default is not None:
                return default
            
            # Try to get from default config
            try:
                return self._get_nested_value(self.default_config, key)
            except KeyError:
                if default is not None:
                    return default
                raise
    
    def set(self, key: str, value: Any, save: bool = True) -> bool:
        """Set configuration value."""
        try:
            # Validate against schema
            if key in self.schema:
                schema = self.schema[key]
                
                # Type validation
                if not isinstance(value, schema.type):
                    if schema.type == float and isinstance(value, int):
                        value = float(value)
                    else:
                        self.logger.error(f"Invalid type for {key}: expected {schema.type.__name__}")
                        return False
                
                # Custom validator
                if schema.validator and not schema.validator(value):
                    self.logger.error(f"Validation failed for {key}: {value}")
                    return False
            
            # Get old value for change detection
            try:
                old_value = self.get(key)
            except KeyError:
                old_value = None
            
            # Set the value
            self._set_nested_value(self.config, key, value)
            
            # Track changes
            if old_value != value:
                self.dirty_keys.add(key)
                self._notify_change(key, old_value, value)
            
            # Auto-save if requested
            if save:
                asyncio.create_task(self.save())
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting config {key}: {e}")
            return False
    
    def _notify_change(self, key: str, old_value: Any, new_value: Any) -> None:
        """Notify change callbacks."""
        try:
            for callback in self.change_callbacks:
                try:
                    callback(key, old_value, new_value)
                except Exception as e:
                    self.logger.error(f"Error in config change callback: {e}")
        except Exception as e:
            self.logger.error(f"Error notifying config changes: {e}")
    
    async def save(self) -> bool:
        """Save configuration to file."""
        try:
            config_file = self.config_dir / "user_settings.json"
            backup_file = self.config_dir / "user_settings.backup.json"
            
            # Create backup
            if config_file.exists():
                config_file.rename(backup_file)
            
            # Save configuration
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2, default=str)
            
            # Clear dirty flags
            self.dirty_keys.clear()
            self.last_save_time = datetime.now()
            
            self.logger.debug("Configuration saved")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
    
    def load(self) -> bool:
        """Reload configuration from file."""
        try:
            self._load_user_config()
            self.logger.info("Configuration reloaded")
            return True
        except Exception as e:
            self.logger.error(f"Error reloading configuration: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults."""
        try:
            self.config = copy.deepcopy(self.default_config)
            self.dirty_keys = set(self.config.keys())
            
            # Notify all changes
            for key in self.schema.keys():
                try:
                    value = self.get(key)
                    self._notify_change(key, None, value)
                except:
                    pass
            
            asyncio.create_task(self.save())
            self.logger.info("Configuration reset to defaults")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting configuration: {e}")
            return False
    
    def export_config(self, file_path: str, format: str = 'json') -> bool:
        """Export configuration to file."""
        try:
            file_path = Path(file_path)
            
            if format.lower() == 'json':
                with open(file_path, 'w') as f:
                    json.dump(self.config, f, indent=2, default=str)
            elif format.lower() == 'yaml':
                with open(file_path, 'w') as f:
                    yaml.dump(self.config, f, indent=2, default_flow_style=False)
            else:
                self.logger.error(f"Unsupported export format: {format}")
                return False
            
            self.logger.info(f"Configuration exported to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Import configuration from file."""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                self.logger.error(f"Configuration file not found: {file_path}")
                return False
            
            # Determine format from extension
            if file_path.suffix.lower() == '.json':
                with open(file_path, 'r') as f:
                    imported_config = json.load(f)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                with open(file_path, 'r') as f:
                    imported_config = yaml.safe_load(f)
            else:
                self.logger.error(f"Unsupported file format: {file_path.suffix}")
                return False
            
            # Merge imported configuration
            self._merge_config(self.config, imported_config)
            self._validate_config()
            
            asyncio.create_task(self.save())
            self.logger.info(f"Configuration imported from {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing configuration: {e}")
            return False
    
    def add_change_callback(self, callback: callable) -> None:
        """Add configuration change callback."""
        if callback not in self.change_callbacks:
            self.change_callbacks.append(callback)
    
    def remove_change_callback(self, callback: callable) -> None:
        """Remove configuration change callback."""
        if callback in self.change_callbacks:
            self.change_callbacks.remove(callback)
    
    def get_schema_info(self, key: str = None) -> Union[Dict[str, ConfigSchema], ConfigSchema]:
        """Get schema information."""
        if key:
            return self.schema.get(key)
        else:
            return self.schema.copy()
    
    def get_all_keys(self) -> List[str]:
        """Get all configuration keys."""
        return list(self.schema.keys())
    
    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes."""
        return len(self.dirty_keys) > 0
    
    def get_config_status(self) -> Dict[str, Any]:
        """Get configuration status information."""
        return {
            'total_keys': len(self.schema),
            'dirty_keys': len(self.dirty_keys),
            'has_unsaved_changes': self.has_unsaved_changes(),
            'last_save_time': self.last_save_time.isoformat() if self.last_save_time else None,
            'config_dir': str(self.config_dir),
            'callbacks_registered': len(self.change_callbacks)
        }