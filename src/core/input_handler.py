"""
Universal Input Handler for Hassan Ultimate Anti-Recoil
Handles mouse and keyboard input with ultra-low latency
"""

import asyncio
import logging
import threading
import time
from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass
from queue import Queue
from enum import Enum

try:
    from pynput import mouse, keyboard
    from pynput.mouse import Button, Listener as MouseListener
    from pynput.keyboard import Key, Listener as KeyboardListener
except ImportError:
    # Fallback for testing
    mouse = None
    keyboard = None
    Button = None
    Key = None
    MouseListener = None
    KeyboardListener = None


class InputEventType(Enum):
    """Types of input events."""
    MOUSE_CLICK = "mouse_click"
    MOUSE_RELEASE = "mouse_release"
    MOUSE_MOVE = "mouse_move"
    KEY_PRESS = "key_press"
    KEY_RELEASE = "key_release"


@dataclass
class InputEvent:
    """Represents an input event."""
    type: InputEventType
    timestamp: float
    button: Optional[str] = None
    key: Optional[str] = None
    position: Optional[tuple] = None
    delta: Optional[tuple] = None


class InputHandler:
    """
    Universal input handler with ultra-low latency processing.
    
    Features:
    - Sub-millisecond input event processing
    - Universal mouse and keyboard support
    - Configurable hotkeys and macros
    - Security features for undetectable operation
    - Real-time input analytics
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        
        # Event processing
        self.event_queue = Queue()
        self.event_handlers: Dict[str, List[Callable]] = {}
        
        # Listeners
        self.mouse_listener: Optional[MouseListener] = None
        self.keyboard_listener: Optional[KeyboardListener] = None
        
        # State tracking
        self.mouse_position = (0, 0)
        self.pressed_keys = set()
        self.pressed_buttons = set()
        
        # Configuration
        self.hotkeys = {}
        self.sensitivity_multiplier = 1.0
        self.enabled = True
        
        # Performance metrics
        self.metrics = {
            'events_processed': 0,
            'average_latency': 0.0,
            'last_event_time': 0.0
        }
        
        self.logger.info("Input handler initialized")
    
    async def initialize(self) -> bool:
        """Initialize input listeners."""
        try:
            if not mouse or not keyboard:
                self.logger.error("pynput not available - input handling disabled")
                return False
            
            # Start mouse listener
            self.mouse_listener = MouseListener(
                on_click=self._on_mouse_click,
                on_move=self._on_mouse_move
            )
            self.mouse_listener.start()
            
            # Start keyboard listener
            self.keyboard_listener = KeyboardListener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self.keyboard_listener.start()
            
            # Load hotkey configuration
            self._load_hotkeys()
            
            self.logger.info("Input handlers initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize input handlers: {e}")
            return False
    
    async def cleanup(self) -> None:
        """Clean up input listeners."""
        try:
            if self.mouse_listener:
                self.mouse_listener.stop()
                self.mouse_listener = None
            
            if self.keyboard_listener:
                self.keyboard_listener.stop()
                self.keyboard_listener = None
            
            self.logger.info("Input handlers cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up input handlers: {e}")
    
    def _on_mouse_click(self, x: int, y: int, button: Button, pressed: bool) -> None:
        """Handle mouse click events."""
        try:
            event_time = time.perf_counter()
            
            # Update state
            self.mouse_position = (x, y)
            
            if pressed:
                self.pressed_buttons.add(button)
                event_type = InputEventType.MOUSE_CLICK
            else:
                self.pressed_buttons.discard(button)
                event_type = InputEventType.MOUSE_RELEASE
            
            # Create event
            event = InputEvent(
                type=event_type,
                timestamp=event_time,
                button=button.name if hasattr(button, 'name') else str(button),
                position=(x, y)
            )
            
            # Queue event for processing
            self._queue_event(event)
            
        except Exception as e:
            self.logger.error(f"Error handling mouse click: {e}")
    
    def _on_mouse_move(self, x: int, y: int) -> None:
        """Handle mouse movement events."""
        try:
            event_time = time.perf_counter()
            
            # Calculate delta
            old_x, old_y = self.mouse_position
            delta = (x - old_x, y - old_y)
            
            # Update position
            self.mouse_position = (x, y)
            
            # Create event (only if significant movement)
            if abs(delta[0]) > 0 or abs(delta[1]) > 0:
                event = InputEvent(
                    type=InputEventType.MOUSE_MOVE,
                    timestamp=event_time,
                    position=(x, y),
                    delta=delta
                )
                
                # Queue event (with throttling for performance)
                if event_time - self.metrics['last_event_time'] > 0.001:  # 1ms throttle
                    self._queue_event(event)
            
        except Exception as e:
            self.logger.error(f"Error handling mouse move: {e}")
    
    def _on_key_press(self, key) -> None:
        """Handle key press events."""
        try:
            event_time = time.perf_counter()
            
            # Convert key to string
            if hasattr(key, 'char') and key.char:
                key_str = key.char
            else:
                key_str = str(key).replace('Key.', '')
            
            # Update state
            self.pressed_keys.add(key_str)
            
            # Check for hotkeys
            self._check_hotkeys(key_str, True)
            
            # Create event
            event = InputEvent(
                type=InputEventType.KEY_PRESS,
                timestamp=event_time,
                key=key_str
            )
            
            self._queue_event(event)
            
        except Exception as e:
            self.logger.error(f"Error handling key press: {e}")
    
    def _on_key_release(self, key) -> None:
        """Handle key release events."""
        try:
            event_time = time.perf_counter()
            
            # Convert key to string
            if hasattr(key, 'char') and key.char:
                key_str = key.char
            else:
                key_str = str(key).replace('Key.', '')
            
            # Update state
            self.pressed_keys.discard(key_str)
            
            # Check for hotkeys
            self._check_hotkeys(key_str, False)
            
            # Create event
            event = InputEvent(
                type=InputEventType.KEY_RELEASE,
                timestamp=event_time,
                key=key_str
            )
            
            self._queue_event(event)
            
        except Exception as e:
            self.logger.error(f"Error handling key release: {e}")
    
    def _queue_event(self, event: InputEvent) -> None:
        """Queue an event for processing."""
        try:
            # Update metrics
            self.metrics['events_processed'] += 1
            self.metrics['last_event_time'] = event.timestamp
            
            # Queue the event
            self.event_queue.put(event)
            
        except Exception as e:
            self.logger.error(f"Error queueing event: {e}")
    
    def _check_hotkeys(self, key: str, pressed: bool) -> None:
        """Check if a hotkey combination was triggered."""
        try:
            if not pressed:
                return
            
            # Check for hotkey matches
            for hotkey_combo, action in self.hotkeys.items():
                if self._is_hotkey_pressed(hotkey_combo):
                    self._execute_hotkey_action(action)
            
        except Exception as e:
            self.logger.error(f"Error checking hotkeys: {e}")
    
    def _is_hotkey_pressed(self, hotkey_combo: str) -> bool:
        """Check if a hotkey combination is currently pressed."""
        try:
            keys = hotkey_combo.lower().split('+')
            
            for key in keys:
                key = key.strip()
                if key not in [k.lower() for k in self.pressed_keys]:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking hotkey combination: {e}")
            return False
    
    def _execute_hotkey_action(self, action: str) -> None:
        """Execute a hotkey action."""
        try:
            if action == "toggle_engine":
                if self.engine.state.value == "active":
                    self.engine.pause()
                else:
                    self.engine.resume()
            elif action == "toggle_input":
                self.enabled = not self.enabled
                self.logger.info(f"Input handling {'enabled' if self.enabled else 'disabled'}")
            
        except Exception as e:
            self.logger.error(f"Error executing hotkey action: {e}")
    
    def _load_hotkeys(self) -> None:
        """Load hotkey configuration."""
        try:
            # Default hotkeys
            self.hotkeys = {
                "f1": "toggle_engine",
                "f2": "toggle_input",
                "ctrl+shift+h": "show_help"
            }
            
            # Load from config if available
            if hasattr(self.engine, 'config_manager'):
                config_hotkeys = self.engine.config_manager.get('hotkeys', {})
                self.hotkeys.update(config_hotkeys)
            
            self.logger.info(f"Loaded {len(self.hotkeys)} hotkeys")
            
        except Exception as e:
            self.logger.error(f"Error loading hotkeys: {e}")
    
    # Public API methods
    
    def get_pending_events(self) -> List[InputEvent]:
        """Get all pending input events."""
        events = []
        
        try:
            while not self.event_queue.empty():
                event = self.event_queue.get_nowait()
                events.append(event)
        except Exception as e:
            self.logger.error(f"Error getting pending events: {e}")
        
        return events
    
    def move_mouse_relative(self, dx: float, dy: float) -> bool:
        """Move mouse relative to current position."""
        try:
            if not self.enabled or not mouse:
                return False
            
            # Apply sensitivity multiplier
            dx *= self.sensitivity_multiplier
            dy *= self.sensitivity_multiplier
            
            # Get current position
            current_x, current_y = self.mouse_position
            
            # Calculate new position
            new_x = current_x + dx
            new_y = current_y + dy
            
            # Move mouse
            mouse.Controller().position = (new_x, new_y)
            
            # Update our position tracking
            self.mouse_position = (new_x, new_y)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving mouse: {e}")
            return False
    
    def move_mouse_absolute(self, x: float, y: float) -> bool:
        """Move mouse to absolute position."""
        try:
            if not self.enabled or not mouse:
                return False
            
            # Move mouse
            mouse.Controller().position = (x, y)
            
            # Update our position tracking
            self.mouse_position = (x, y)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving mouse to absolute position: {e}")
            return False
    
    def simulate_key_press(self, key: str) -> bool:
        """Simulate a key press."""
        try:
            if not self.enabled or not keyboard:
                return False
            
            # Use keyboard controller to simulate key press
            controller = keyboard.Controller()
            
            if len(key) == 1:
                controller.press(key)
                controller.release(key)
            else:
                # Handle special keys
                special_key = getattr(Key, key, None)
                if special_key:
                    controller.press(special_key)
                    controller.release(special_key)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error simulating key press: {e}")
            return False
    
    def set_sensitivity(self, multiplier: float) -> None:
        """Set mouse sensitivity multiplier."""
        self.sensitivity_multiplier = max(0.1, min(10.0, multiplier))
        self.logger.info(f"Mouse sensitivity set to {self.sensitivity_multiplier}x")
    
    def enable(self) -> None:
        """Enable input handling."""
        self.enabled = True
        self.logger.info("Input handling enabled")
    
    def disable(self) -> None:
        """Disable input handling."""
        self.enabled = False
        self.logger.info("Input handling disabled")
    
    def is_key_pressed(self, key: str) -> bool:
        """Check if a key is currently pressed."""
        return key.lower() in [k.lower() for k in self.pressed_keys]
    
    def is_button_pressed(self, button: str) -> bool:
        """Check if a mouse button is currently pressed."""
        return button.lower() in [str(b).lower() for b in self.pressed_buttons]
    
    def get_mouse_position(self) -> tuple:
        """Get current mouse position."""
        return self.mouse_position
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get input handling performance metrics."""
        return self.metrics.copy()
    
    def add_event_handler(self, event_type: str, handler: Callable) -> None:
        """Add an event handler for specific event types."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        self.logger.debug(f"Added event handler for {event_type}")
    
    def remove_event_handler(self, event_type: str, handler: Callable) -> None:
        """Remove an event handler."""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
                self.logger.debug(f"Removed event handler for {event_type}")
            except ValueError:
                pass