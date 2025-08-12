"""
Plugin Manager for Hassan Ultimate Anti-Recoil
Extensible plugin system for custom functionality
"""

import logging
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Any, Optional, Type, Callable
from abc import ABC, abstractmethod
import asyncio


class PluginBase(ABC):
    """Base class for all plugins."""
    
    def __init__(self, engine, config_manager):
        self.engine = engine
        self.config_manager = config_manager
        self.logger = logging.getLogger(f"plugin.{self.__class__.__name__}")
        self.enabled = True
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass
    
    def enable(self) -> None:
        """Enable the plugin."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable the plugin."""
        self.enabled = False
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get plugin configuration value."""
        plugin_key = f"plugins.{self.name}.{key}"
        return self.config_manager.get(plugin_key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Set plugin configuration value."""
        plugin_key = f"plugins.{self.name}.{key}"
        self.config_manager.set(plugin_key, value)


class PluginManager:
    """
    Plugin management system.
    
    Features:
    - Dynamic plugin loading and unloading
    - Plugin lifecycle management
    - Configuration management
    - Event system for plugin communication
    - Dependency resolution
    - Error isolation
    """
    
    def __init__(self, engine, config_manager):
        self.engine = engine
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Plugin storage
        self.plugins: Dict[str, PluginBase] = {}
        self.plugin_classes: Dict[str, Type[PluginBase]] = {}
        
        # Plugin directories
        self.plugin_dirs = [
            Path("src/plugins"),
            Path("plugins"),  # User plugins directory
        ]
        
        # Event system
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        self.logger.info("Plugin manager initialized")
    
    async def load_plugins(self) -> None:
        """Load all available plugins."""
        try:
            for plugin_dir in self.plugin_dirs:
                if plugin_dir.exists():
                    await self._load_plugins_from_directory(plugin_dir)
            
            self.logger.info(f"Loaded {len(self.plugins)} plugins")
            
        except Exception as e:
            self.logger.error(f"Error loading plugins: {e}")
    
    async def _load_plugins_from_directory(self, plugin_dir: Path) -> None:
        """Load plugins from a specific directory."""
        try:
            for plugin_file in plugin_dir.glob("*.py"):
                if plugin_file.name.startswith("__"):
                    continue
                
                await self._load_plugin_file(plugin_file)
                
        except Exception as e:
            self.logger.error(f"Error loading plugins from {plugin_dir}: {e}")
    
    async def _load_plugin_file(self, plugin_file: Path) -> None:
        """Load a plugin from a Python file."""
        try:
            # Import the module
            module_name = plugin_file.stem
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            
            if not spec or not spec.loader:
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginBase) and 
                    obj != PluginBase):
                    
                    plugin_instance = obj(self.engine, self.config_manager)
                    
                    # Initialize plugin
                    if await plugin_instance.initialize():
                        self.plugins[plugin_instance.name] = plugin_instance
                        self.plugin_classes[plugin_instance.name] = obj
                        self.logger.info(f"Loaded plugin: {plugin_instance.name} v{plugin_instance.version}")
                    else:
                        self.logger.error(f"Failed to initialize plugin: {plugin_instance.name}")
            
        except Exception as e:
            self.logger.error(f"Error loading plugin file {plugin_file}: {e}")
    
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin."""
        try:
            if plugin_name not in self.plugins:
                self.logger.warning(f"Plugin not found: {plugin_name}")
                return False
            
            plugin = self.plugins[plugin_name]
            
            # Clean up plugin
            await plugin.cleanup()
            
            # Remove from storage
            del self.plugins[plugin_name]
            if plugin_name in self.plugin_classes:
                del self.plugin_classes[plugin_name]
            
            self.logger.info(f"Unloaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin."""
        try:
            if plugin_name in self.plugins:
                await self.unload_plugin(plugin_name)
            
            # Re-scan for the plugin
            await self.load_plugins()
            
            return plugin_name in self.plugins
            
        except Exception as e:
            self.logger.error(f"Error reloading plugin {plugin_name}: {e}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """Get a plugin instance by name."""
        return self.plugins.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, PluginBase]:
        """Get all loaded plugins."""
        return self.plugins.copy()
    
    def get_enabled_plugins(self) -> Dict[str, PluginBase]:
        """Get all enabled plugins."""
        return {name: plugin for name, plugin in self.plugins.items() if plugin.enabled}
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin."""
        try:
            if plugin_name in self.plugins:
                self.plugins[plugin_name].enable()
                self.logger.info(f"Enabled plugin: {plugin_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error enabling plugin {plugin_name}: {e}")
            return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin."""
        try:
            if plugin_name in self.plugins:
                self.plugins[plugin_name].disable()
                self.logger.info(f"Disabled plugin: {plugin_name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error disabling plugin {plugin_name}: {e}")
            return False
    
    def register_event_handler(self, event_name: str, handler: Callable) -> None:
        """Register an event handler."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append(handler)
        self.logger.debug(f"Registered event handler for {event_name}")
    
    def unregister_event_handler(self, event_name: str, handler: Callable) -> None:
        """Unregister an event handler."""
        if event_name in self.event_handlers:
            try:
                self.event_handlers[event_name].remove(handler)
                self.logger.debug(f"Unregistered event handler for {event_name}")
            except ValueError:
                pass
    
    async def emit_event(self, event_name: str, **kwargs) -> None:
        """Emit an event to all registered handlers."""
        try:
            if event_name in self.event_handlers:
                handlers = self.event_handlers[event_name].copy()
                
                for handler in handlers:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(**kwargs)
                        else:
                            handler(**kwargs)
                    except Exception as e:
                        self.logger.error(f"Error in event handler for {event_name}: {e}")
            
        except Exception as e:
            self.logger.error(f"Error emitting event {event_name}: {e}")
    
    async def cleanup(self) -> None:
        """Clean up all plugins."""
        try:
            for plugin_name in list(self.plugins.keys()):
                await self.unload_plugin(plugin_name)
            
            self.event_handlers.clear()
            self.logger.info("Plugin manager cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up plugin manager: {e}")
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Get information about all plugins."""
        plugin_info = {}
        
        for name, plugin in self.plugins.items():
            plugin_info[name] = {
                'name': plugin.name,
                'version': plugin.version,
                'description': plugin.description,
                'enabled': plugin.enabled,
                'class': plugin.__class__.__name__
            }
        
        return plugin_info