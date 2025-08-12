"""
Example Plugin for Hassan Ultimate Anti-Recoil
Demonstrates plugin development and integration
"""

import asyncio
import logging
from typing import Any
from src.plugins.plugin_manager import PluginBase


class ExamplePlugin(PluginBase):
    """
    Example plugin that demonstrates basic plugin functionality.
    
    Features:
    - Event handling
    - Configuration management
    - Performance monitoring
    - Custom commands
    """
    
    @property
    def name(self) -> str:
        return "example_plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Example plugin demonstrating Hassan Ultimate Anti-Recoil plugin system"
    
    async def initialize(self) -> bool:
        """Initialize the example plugin."""
        try:
            self.logger.info("Example plugin initializing...")
            
            # Set default configuration
            self.set_config("enabled", True)
            self.set_config("log_shots", False)
            self.set_config("custom_message", "Hello from Example Plugin!")
            
            # Register event handlers if plugin manager is available
            if hasattr(self.engine, 'plugin_manager'):
                self.engine.plugin_manager.register_event_handler('shot_fired', self._on_shot_fired)
                self.engine.plugin_manager.register_event_handler('weapon_changed', self._on_weapon_changed)
                self.engine.plugin_manager.register_event_handler('game_changed', self._on_game_changed)
            
            # Start background task
            self.background_task = asyncio.create_task(self._background_worker())
            
            self.logger.info("Example plugin initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize example plugin: {e}")
            return False
    
    async def cleanup(self) -> None:
        """Clean up example plugin resources."""
        try:
            self.logger.info("Example plugin cleaning up...")
            
            # Cancel background task
            if hasattr(self, 'background_task'):
                self.background_task.cancel()
                try:
                    await self.background_task
                except asyncio.CancelledError:
                    pass
            
            # Unregister event handlers
            if hasattr(self.engine, 'plugin_manager'):
                self.engine.plugin_manager.unregister_event_handler('shot_fired', self._on_shot_fired)
                self.engine.plugin_manager.unregister_event_handler('weapon_changed', self._on_weapon_changed)
                self.engine.plugin_manager.unregister_event_handler('game_changed', self._on_game_changed)
            
            self.logger.info("Example plugin cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up example plugin: {e}")
    
    async def _background_worker(self) -> None:
        """Background worker task."""
        try:
            while self.enabled:
                # Perform periodic tasks
                if self.get_config("enabled", True):
                    await self._perform_periodic_task()
                
                # Sleep for 30 seconds
                await asyncio.sleep(30)
                
        except asyncio.CancelledError:
            self.logger.debug("Background worker cancelled")
        except Exception as e:
            self.logger.error(f"Error in background worker: {e}")
    
    async def _perform_periodic_task(self) -> None:
        """Perform a periodic task."""
        try:
            # Log current performance metrics
            if hasattr(self.engine, 'get_performance_metrics'):
                metrics = self.engine.get_performance_metrics()
                shots_fired = metrics.get('shots_fired', 0)
                avg_latency = metrics.get('average_latency', 0) * 1000  # Convert to ms
                
                self.logger.debug(f"Performance check - Shots: {shots_fired}, Latency: {avg_latency:.2f}ms")
        
        except Exception as e:
            self.logger.error(f"Error in periodic task: {e}")
    
    def _on_shot_fired(self, **kwargs) -> None:
        """Handle shot fired event."""
        try:
            if self.get_config("log_shots", False):
                weapon = kwargs.get('weapon', 'unknown')
                shot_number = kwargs.get('shot_number', 0)
                self.logger.info(f"Shot fired: {weapon} (#{shot_number})")
        
        except Exception as e:
            self.logger.error(f"Error handling shot fired event: {e}")
    
    def _on_weapon_changed(self, **kwargs) -> None:
        """Handle weapon changed event."""
        try:
            old_weapon = kwargs.get('old_weapon', 'none')
            new_weapon = kwargs.get('new_weapon', 'unknown')
            self.logger.info(f"Weapon changed: {old_weapon} -> {new_weapon}")
        
        except Exception as e:
            self.logger.error(f"Error handling weapon changed event: {e}")
    
    def _on_game_changed(self, **kwargs) -> None:
        """Handle game changed event."""
        try:
            old_game = kwargs.get('old_game', 'none')
            new_game = kwargs.get('new_game', 'unknown')
            self.logger.info(f"Game changed: {old_game} -> {new_game}")
        
        except Exception as e:
            self.logger.error(f"Error handling game changed event: {e}")
    
    # Custom plugin methods
    
    def get_status(self) -> dict:
        """Get plugin status information."""
        return {
            'name': self.name,
            'version': self.version,
            'enabled': self.enabled,
            'config': {
                'enabled': self.get_config("enabled", True),
                'log_shots': self.get_config("log_shots", False),
                'custom_message': self.get_config("custom_message", "")
            },
            'background_task_running': hasattr(self, 'background_task') and not self.background_task.done()
        }
    
    def execute_command(self, command: str, *args) -> Any:
        """Execute a custom plugin command."""
        try:
            if command == "hello":
                message = self.get_config("custom_message", "Hello from Example Plugin!")
                self.logger.info(message)
                return message
            
            elif command == "toggle_logging":
                current = self.get_config("log_shots", False)
                new_value = not current
                self.set_config("log_shots", new_value)
                self.logger.info(f"Shot logging {'enabled' if new_value else 'disabled'}")
                return f"Shot logging {'enabled' if new_value else 'disabled'}"
            
            elif command == "set_message":
                if args:
                    message = " ".join(args)
                    self.set_config("custom_message", message)
                    self.logger.info(f"Custom message set to: {message}")
                    return f"Custom message set to: {message}"
                else:
                    return "Usage: set_message <message>"
            
            elif command == "get_metrics":
                if hasattr(self.engine, 'get_performance_metrics'):
                    return self.engine.get_performance_metrics()
                else:
                    return "Performance metrics not available"
            
            else:
                return f"Unknown command: {command}"
        
        except Exception as e:
            self.logger.error(f"Error executing command {command}: {e}")
            return f"Error executing command: {e}"


# Plugin registration function (optional)
def register_plugin(engine, config_manager):
    """Register the example plugin."""
    return ExamplePlugin(engine, config_manager)