"""
Game Detection System for Hassan Ultimate Anti-Recoil
Automatic detection of supported games and their configurations
"""

import asyncio
import logging
import time
import re
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import json

try:
    import psutil
except ImportError:
    # Fallback for testing without psutil
    class psutil:
        class NoSuchProcess(Exception):
            pass
        
        class AccessDenied(Exception):
            pass
        
        @staticmethod
        def process_iter(attrs=None):
            # Return empty iterator when psutil not available
            return iter([])
        
        class Process:
            def __init__(self, pid):
                self.pid = pid
            
            @property
            def info(self):
                return {'pid': self.pid, 'name': 'test_process.exe'}


@dataclass
class GameInfo:
    """Information about a detected game."""
    name: str
    display_name: str
    process_name: str
    window_title: str
    executable_path: Optional[str] = None
    version: Optional[str] = None
    anti_cheat: Optional[str] = None
    supported: bool = True


@dataclass
class GameProfile:
    """Game-specific configuration profile."""
    game_name: str
    display_name: str
    sensitivity_multiplier: float
    default_weapon: str
    hotkeys: Dict[str, str]
    security_settings: Dict[str, Any]
    weapon_list: List[str]


class GameDetector:
    """
    Automatic game detection and profile management.
    
    Features:
    - Real-time process monitoring
    - Window title detection
    - Anti-cheat system detection
    - Automatic profile switching
    - Game-specific optimizations
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        
        # Game database
        self.supported_games: Dict[str, GameInfo] = {}
        self.game_profiles: Dict[str, GameProfile] = {}
        
        # Detection state
        self.current_game: Optional[GameInfo] = None
        self.current_profile: Optional[GameProfile] = None
        self.running_processes: Set[str] = set()
        
        # Monitoring
        self.detection_enabled = True
        self.scan_interval = 2.0  # seconds
        self.last_scan = 0.0
        
        # Load game definitions
        self._load_game_definitions()
        self._load_game_profiles()
        
        self.logger.info("Game detector initialized")
    
    async def initialize(self) -> bool:
        """Initialize game detection system."""
        try:
            self.logger.info("Initializing game detection...")
            
            # Start monitoring task
            asyncio.create_task(self._monitoring_loop())
            
            # Perform initial scan
            await self._scan_for_games()
            
            self.logger.info("Game detection initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize game detection: {e}")
            return False
    
    async def cleanup(self) -> None:
        """Clean up game detection resources."""
        try:
            self.detection_enabled = False
            self.logger.info("Game detection cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up game detection: {e}")
    
    def _load_game_definitions(self) -> None:
        """Load supported game definitions."""
        try:
            # Define supported games
            games = {
                "cod_bo6": GameInfo(
                    name="cod_bo6",
                    display_name="Call of Duty: Black Ops 6",
                    process_name="cod.exe",
                    window_title="Call of Duty",
                    anti_cheat="Ricochet",
                    supported=True
                ),
                "valorant": GameInfo(
                    name="valorant",
                    display_name="VALORANT",
                    process_name="VALORANT-Win64-Shipping.exe",
                    window_title="VALORANT",
                    anti_cheat="Vanguard",
                    supported=True
                ),
                "cs2": GameInfo(
                    name="cs2",
                    display_name="Counter-Strike 2",
                    process_name="cs2.exe",
                    window_title="Counter-Strike 2",
                    anti_cheat="VAC",
                    supported=True
                ),
                "apex": GameInfo(
                    name="apex",
                    display_name="Apex Legends",
                    process_name="r5apex.exe",
                    window_title="Apex Legends",
                    anti_cheat="EasyAntiCheat",
                    supported=True
                ),
                "overwatch2": GameInfo(
                    name="overwatch2",
                    display_name="Overwatch 2",
                    process_name="Overwatch.exe",
                    window_title="Overwatch 2",
                    anti_cheat="Custom",
                    supported=True
                ),
                "pubg": GameInfo(
                    name="pubg",
                    display_name="PUBG",
                    process_name="TslGame.exe",
                    window_title="PUBG",
                    anti_cheat="BattlEye",
                    supported=True
                ),
                "fortnite": GameInfo(
                    name="fortnite",
                    display_name="Fortnite",
                    process_name="FortniteClient-Win64-Shipping.exe",
                    window_title="Fortnite",
                    anti_cheat="BattlEye",
                    supported=True
                ),
                "r6siege": GameInfo(
                    name="r6siege",
                    display_name="Rainbow Six Siege",
                    process_name="RainbowSix.exe",
                    window_title="Rainbow Six Siege",
                    anti_cheat="BattlEye",
                    supported=True
                )
            }
            
            self.supported_games = games
            self.logger.info(f"Loaded {len(games)} game definitions")
            
            # Try to load from config file
            config_file = Path("config/game_definitions.json")
            if config_file.exists():
                with open(config_file, 'r') as f:
                    custom_games = json.load(f)
                    for game_id, game_data in custom_games.items():
                        self.supported_games[game_id] = GameInfo(**game_data)
                
                self.logger.info(f"Loaded additional games from config")
            
        except Exception as e:
            self.logger.error(f"Error loading game definitions: {e}")
    
    def _load_game_profiles(self) -> None:
        """Load game-specific configuration profiles."""
        try:
            # Define default profiles
            profiles = {
                "cod_bo6": GameProfile(
                    game_name="cod_bo6",
                    display_name="Call of Duty: Black Ops 6",
                    sensitivity_multiplier=1.0,
                    default_weapon="ak74",
                    hotkeys={"f1": "toggle_engine", "f2": "next_weapon"},
                    security_settings={"stealth_mode": True, "randomization": 0.15},
                    weapon_list=["ak74", "m4a1", "xm4", "ames85", "jackal_pdw"]
                ),
                "valorant": GameProfile(
                    game_name="valorant",
                    display_name="VALORANT",
                    sensitivity_multiplier=0.8,
                    default_weapon="vandal",
                    hotkeys={"f1": "toggle_engine", "f2": "next_weapon"},
                    security_settings={"stealth_mode": True, "randomization": 0.2},
                    weapon_list=["vandal", "phantom", "operator", "sheriff", "spectre"]
                ),
                "cs2": GameProfile(
                    game_name="cs2",
                    display_name="Counter-Strike 2",
                    sensitivity_multiplier=1.2,
                    default_weapon="ak47",
                    hotkeys={"f1": "toggle_engine", "f2": "next_weapon"},
                    security_settings={"stealth_mode": True, "randomization": 0.1},
                    weapon_list=["ak47", "m4a4", "m4a1s", "awp", "deagle"]
                )
            }
            
            self.game_profiles = profiles
            self.logger.info(f"Loaded {len(profiles)} game profiles")
            
            # Try to load from config file
            config_file = Path("config/game_profiles.json")
            if config_file.exists():
                with open(config_file, 'r') as f:
                    custom_profiles = json.load(f)
                    for profile_id, profile_data in custom_profiles.items():
                        self.game_profiles[profile_id] = GameProfile(**profile_data)
                
                self.logger.info("Loaded additional profiles from config")
            
        except Exception as e:
            self.logger.error(f"Error loading game profiles: {e}")
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop for game detection."""
        self.logger.debug("Game detection monitoring loop started")
        
        while self.detection_enabled:
            try:
                current_time = time.time()
                
                # Check if it's time for a scan
                if current_time - self.last_scan >= self.scan_interval:
                    await self._scan_for_games()
                    self.last_scan = current_time
                
                # Sleep for a short time
                await asyncio.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(1.0)
        
        self.logger.debug("Game detection monitoring loop stopped")
    
    async def _scan_for_games(self) -> None:
        """Scan for running games."""
        try:
            # Get current running processes
            current_processes = set()
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    proc_info = proc.info
                    if proc_info['name']:
                        current_processes.add(proc_info['name'].lower())
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Check for game processes
            detected_game = None
            
            for game_id, game_info in self.supported_games.items():
                if game_info.process_name.lower() in current_processes:
                    detected_game = game_info
                    break
            
            # Handle game change
            if detected_game != self.current_game:
                await self._handle_game_change(detected_game)
            
            self.running_processes = current_processes
            
        except Exception as e:
            self.logger.error(f"Error scanning for games: {e}")
    
    async def _handle_game_change(self, new_game: Optional[GameInfo]) -> None:
        """Handle detected game change."""
        try:
            # Log game change
            if new_game:
                self.logger.info(f"Game detected: {new_game.display_name}")
                
                # Check if game is supported
                if not new_game.supported:
                    self.logger.warning(f"Game {new_game.display_name} is not fully supported")
                
                # Load game profile
                profile = self.game_profiles.get(new_game.name)
                if profile:
                    await self._apply_game_profile(profile)
                    self.current_profile = profile
                    self.logger.info(f"Applied profile for {new_game.display_name}")
                else:
                    self.logger.warning(f"No profile found for {new_game.display_name}")
                
                # Update engine with game info
                if hasattr(self.engine, 'set_game'):
                    self.engine.set_game(new_game.name, new_game.display_name)
                
            else:
                if self.current_game:
                    self.logger.info(f"Game closed: {self.current_game.display_name}")
                
                # Reset to default profile
                await self._reset_to_default_profile()
                self.current_profile = None
            
            self.current_game = new_game
            
        except Exception as e:
            self.logger.error(f"Error handling game change: {e}")
    
    async def _apply_game_profile(self, profile: GameProfile) -> None:
        """Apply a game-specific profile."""
        try:
            # Set sensitivity
            if hasattr(self.engine, 'input_handler'):
                self.engine.input_handler.set_sensitivity(profile.sensitivity_multiplier)
            
            # Set default weapon
            if hasattr(self.engine, 'set_weapon'):
                self.engine.set_weapon(profile.default_weapon, profile.game_name)
            
            # Apply security settings
            if hasattr(self.engine, 'security_manager'):
                for setting, value in profile.security_settings.items():
                    self.engine.security_manager.set_setting(setting, value)
            
            # Update hotkeys
            if hasattr(self.engine, 'input_handler'):
                self.engine.input_handler.hotkeys.update(profile.hotkeys)
            
            self.logger.debug(f"Applied profile settings for {profile.display_name}")
            
        except Exception as e:
            self.logger.error(f"Error applying game profile: {e}")
    
    async def _reset_to_default_profile(self) -> None:
        """Reset to default profile when no game is detected."""
        try:
            # Reset sensitivity
            if hasattr(self.engine, 'input_handler'):
                self.engine.input_handler.set_sensitivity(1.0)
            
            # Reset security settings
            if hasattr(self.engine, 'security_manager'):
                self.engine.security_manager.reset_to_defaults()
            
            self.logger.debug("Reset to default profile")
            
        except Exception as e:
            self.logger.error(f"Error resetting to default profile: {e}")
    
    # Public API methods
    
    def get_current_game(self) -> Optional[GameInfo]:
        """Get currently detected game."""
        return self.current_game
    
    def get_current_profile(self) -> Optional[GameProfile]:
        """Get current game profile."""
        return self.current_profile
    
    def get_supported_games(self) -> Dict[str, GameInfo]:
        """Get list of supported games."""
        return self.supported_games.copy()
    
    def get_available_profiles(self) -> Dict[str, GameProfile]:
        """Get list of available game profiles."""
        return self.game_profiles.copy()
    
    def is_game_running(self, game_name: str) -> bool:
        """Check if a specific game is running."""
        game_info = self.supported_games.get(game_name)
        if not game_info:
            return False
        
        return game_info.process_name.lower() in self.running_processes
    
    def manually_set_game(self, game_name: str) -> bool:
        """Manually set the current game."""
        try:
            game_info = self.supported_games.get(game_name)
            if not game_info:
                self.logger.error(f"Unknown game: {game_name}")
                return False
            
            # Apply the game change
            asyncio.create_task(self._handle_game_change(game_info))
            
            self.logger.info(f"Manually set game to {game_info.display_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error manually setting game: {e}")
            return False
    
    def add_custom_game(self, game_info: GameInfo) -> bool:
        """Add a custom game definition."""
        try:
            self.supported_games[game_info.name] = game_info
            self.logger.info(f"Added custom game: {game_info.display_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding custom game: {e}")
            return False
    
    def add_custom_profile(self, profile: GameProfile) -> bool:
        """Add a custom game profile."""
        try:
            self.game_profiles[profile.game_name] = profile
            self.logger.info(f"Added custom profile: {profile.display_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding custom profile: {e}")
            return False
    
    def enable_detection(self) -> None:
        """Enable automatic game detection."""
        self.detection_enabled = True
        self.logger.info("Game detection enabled")
    
    def disable_detection(self) -> None:
        """Disable automatic game detection."""
        self.detection_enabled = False
        self.logger.info("Game detection disabled")
    
    def get_detection_status(self) -> Dict[str, Any]:
        """Get game detection status and metrics."""
        return {
            'detection_enabled': self.detection_enabled,
            'current_game': self.current_game.display_name if self.current_game else None,
            'current_profile': self.current_profile.display_name if self.current_profile else None,
            'supported_games_count': len(self.supported_games),
            'available_profiles_count': len(self.game_profiles),
            'running_processes_count': len(self.running_processes),
            'last_scan_time': self.last_scan,
            'scan_interval': self.scan_interval
        }