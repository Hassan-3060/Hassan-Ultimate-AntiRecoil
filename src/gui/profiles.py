"""
Profiles Panel for Hassan Ultimate Anti-Recoil
Game and weapon profile management interface
"""

import logging
import tkinter as tk
from typing import Dict, Any, Optional, List

try:
    import customtkinter as ctk
except ImportError:
    ctk = None


class ProfilesPanel:
    """
    Game and weapon profile management panel.
    
    Features:
    - Game profile selection
    - Weapon configuration
    - Profile creation and editing
    - Import/Export profiles
    - Real-time profile switching
    """
    
    def __init__(self, parent, engine, config_manager):
        self.parent = parent
        self.engine = engine
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Profiles frame
        self.profiles_frame = None
        self.visible = False
        
        # Current selections
        self.selected_game = None
        self.selected_weapon = None
        
        # Widgets
        self.game_listbox = None
        self.weapon_listbox = None
        self.profile_widgets = {}
        
        # Create profiles panel
        self._create_profiles_panel()
        
        self.logger.info("Profiles panel initialized")
    
    def _create_profiles_panel(self) -> None:
        """Create the profiles interface."""
        try:
            # Main profiles frame
            self.profiles_frame = ctk.CTkFrame(self.parent)
            self.profiles_frame.grid_columnconfigure((0, 1), weight=1)
            self.profiles_frame.grid_rowconfigure(2, weight=1)
            
            # Title
            title_label = ctk.CTkLabel(
                self.profiles_frame,
                text="🎮 Game & Weapon Profiles",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=20)
            
            # Create sections
            self._create_game_selection()
            self._create_weapon_selection()
            self._create_profile_editor()
            
        except Exception as e:
            self.logger.error(f"Error creating profiles panel: {e}")
    
    def _create_game_selection(self) -> None:
        """Create game selection section."""
        try:
            # Game Selection Frame
            game_frame = ctk.CTkFrame(self.profiles_frame)
            game_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            game_frame.grid_columnconfigure(0, weight=1)
            game_frame.grid_rowconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                game_frame,
                text="🎯 Supported Games",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, pady=10)
            
            # Games list
            games_list = ctk.CTkScrollableFrame(game_frame)
            games_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            games_list.grid_columnconfigure(0, weight=1)
            
            # Populate games
            if self.engine and hasattr(self.engine, 'game_detector'):
                supported_games = self.engine.game_detector.get_supported_games()
                
                for i, (game_id, game_info) in enumerate(supported_games.items()):
                    game_btn = ctk.CTkButton(
                        games_list,
                        text=f"{game_info.display_name}",
                        command=lambda g=game_id: self._select_game(g),
                        height=40
                    )
                    game_btn.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            
            # Current game indicator
            self.current_game_label = ctk.CTkLabel(
                game_frame,
                text="Current: Auto-Detect",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            self.current_game_label.grid(row=2, column=0, pady=5)
            
        except Exception as e:
            self.logger.error(f"Error creating game selection: {e}")
    
    def _create_weapon_selection(self) -> None:
        """Create weapon selection section."""
        try:
            # Weapon Selection Frame
            weapon_frame = ctk.CTkFrame(self.profiles_frame)
            weapon_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
            weapon_frame.grid_columnconfigure(0, weight=1)
            weapon_frame.grid_rowconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                weapon_frame,
                text="🔫 Available Weapons",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, pady=10)
            
            # Weapons list
            self.weapons_list = ctk.CTkScrollableFrame(weapon_frame)
            self.weapons_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            self.weapons_list.grid_columnconfigure(0, weight=1)
            
            # Will be populated when game is selected
            no_game_label = ctk.CTkLabel(
                self.weapons_list,
                text="Select a game to view weapons",
                font=ctk.CTkFont(size=12)
            )
            no_game_label.grid(row=0, column=0, pady=20)
            
            # Current weapon indicator
            self.current_weapon_label = ctk.CTkLabel(
                weapon_frame,
                text="Current: None",
                font=ctk.CTkFont(size=12, weight="bold")
            )
            self.current_weapon_label.grid(row=2, column=0, pady=5)
            
        except Exception as e:
            self.logger.error(f"Error creating weapon selection: {e}")
    
    def _create_profile_editor(self) -> None:
        """Create profile editor section."""
        try:
            # Profile Editor Frame
            editor_frame = ctk.CTkFrame(self.profiles_frame)
            editor_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
            editor_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                editor_frame,
                text="✏️ Profile Configuration",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            row = 1
            
            # Weapon Name
            name_label = ctk.CTkLabel(editor_frame, text="Weapon Name:")
            name_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            self.weapon_name_var = ctk.StringVar()
            name_entry = ctk.CTkEntry(editor_frame, textvariable=self.weapon_name_var)
            name_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            row += 1
            
            # Sensitivity Multiplier
            sens_label = ctk.CTkLabel(editor_frame, text="Sensitivity Multiplier:")
            sens_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            self.sensitivity_var = ctk.DoubleVar(value=1.0)
            sens_slider = ctk.CTkSlider(
                editor_frame, from_=0.1, to=5.0, variable=self.sensitivity_var
            )
            sens_slider.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            row += 1
            
            # Recoil Pattern Configuration
            pattern_label = ctk.CTkLabel(
                editor_frame,
                text="Recoil Pattern (Vertical, Horizontal):",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            pattern_label.grid(row=row, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")
            row += 1
            
            # Pattern text area
            self.pattern_text = ctk.CTkTextbox(editor_frame, height=100)
            self.pattern_text.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
            self.pattern_text.insert("1.0", "# Enter recoil pattern (one line per shot)\n# Format: vertical_compensation, horizontal_compensation\n-3.0, 0.0\n-4.0, -1.0\n-5.0, 1.0\n-4.0, -2.0")
            row += 1
            
            # Security Settings for this profile
            security_label = ctk.CTkLabel(
                editor_frame,
                text="Security Settings:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            security_label.grid(row=row, column=0, columnspan=2, padx=10, pady=(20, 5), sticky="w")
            row += 1
            
            # Randomization level for this weapon
            random_label = ctk.CTkLabel(editor_frame, text="Randomization Level:")
            random_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            self.randomization_var = ctk.DoubleVar(value=0.15)
            random_slider = ctk.CTkSlider(
                editor_frame, from_=0.0, to=0.5, variable=self.randomization_var
            )
            random_slider.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            row += 1
            
            # Action buttons
            button_frame = ctk.CTkFrame(editor_frame)
            button_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
            button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            save_btn = ctk.CTkButton(
                button_frame, text="Save Profile",
                command=self._save_profile
            )
            save_btn.grid(row=0, column=0, padx=5, pady=5)
            
            load_btn = ctk.CTkButton(
                button_frame, text="Load Profile",
                command=self._load_profile
            )
            load_btn.grid(row=0, column=1, padx=5, pady=5)
            
            test_btn = ctk.CTkButton(
                button_frame, text="Test Pattern",
                command=self._test_pattern
            )
            test_btn.grid(row=0, column=2, padx=5, pady=5)
            
            activate_btn = ctk.CTkButton(
                button_frame, text="Activate Profile",
                command=self._activate_profile
            )
            activate_btn.grid(row=0, column=3, padx=5, pady=5)
            
        except Exception as e:
            self.logger.error(f"Error creating profile editor: {e}")
    
    def _select_game(self, game_id: str) -> None:
        """Select a game and update weapon list."""
        try:
            self.selected_game = game_id
            
            # Update current game display
            if self.engine and hasattr(self.engine, 'game_detector'):
                games = self.engine.game_detector.get_supported_games()
                if game_id in games:
                    game_name = games[game_id].display_name
                    self.current_game_label.configure(text=f"Current: {game_name}")
            
            # Load weapons for this game
            self._load_weapons_for_game(game_id)
            
            # Manually set game in engine
            if self.engine and hasattr(self.engine.game_detector, 'manually_set_game'):
                self.engine.game_detector.manually_set_game(game_id)
            
            self.logger.info(f"Selected game: {game_id}")
            
        except Exception as e:
            self.logger.error(f"Error selecting game: {e}")
    
    def _load_weapons_for_game(self, game_id: str) -> None:
        """Load weapons for the selected game."""
        try:
            # Clear existing weapons
            for widget in self.weapons_list.winfo_children():
                widget.destroy()
            
            # Get game profile to find weapons
            if self.engine and hasattr(self.engine, 'game_detector'):
                profiles = self.engine.game_detector.get_available_profiles()
                
                if game_id in profiles:
                    profile = profiles[game_id]
                    weapons = profile.weapon_list
                    
                    for i, weapon in enumerate(weapons):
                        weapon_btn = ctk.CTkButton(
                            self.weapons_list,
                            text=weapon.replace('_', ' ').title(),
                            command=lambda w=weapon: self._select_weapon(w),
                            height=35
                        )
                        weapon_btn.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
                else:
                    # Default weapons if no profile found
                    default_weapons = ["assault_rifle", "submachine_gun", "sniper_rifle", "pistol"]
                    for i, weapon in enumerate(default_weapons):
                        weapon_btn = ctk.CTkButton(
                            self.weapons_list,
                            text=weapon.replace('_', ' ').title(),
                            command=lambda w=weapon: self._select_weapon(w),
                            height=35
                        )
                        weapon_btn.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            
        except Exception as e:
            self.logger.error(f"Error loading weapons for game: {e}")
    
    def _select_weapon(self, weapon: str) -> None:
        """Select a weapon and load its profile."""
        try:
            self.selected_weapon = weapon
            
            # Update current weapon display
            weapon_display = weapon.replace('_', ' ').title()
            self.current_weapon_label.configure(text=f"Current: {weapon_display}")
            
            # Load weapon profile data
            self._load_weapon_profile(weapon)
            
            # Set weapon in engine
            if self.engine and hasattr(self.engine, 'set_weapon'):
                self.engine.set_weapon(weapon, self.selected_game or "universal")
            
            self.logger.info(f"Selected weapon: {weapon}")
            
        except Exception as e:
            self.logger.error(f"Error selecting weapon: {e}")
    
    def _load_weapon_profile(self, weapon: str) -> None:
        """Load weapon profile into editor."""
        try:
            # Set weapon name
            self.weapon_name_var.set(weapon.replace('_', ' ').title())
            
            # Load default pattern or saved pattern
            # This would normally load from a weapons database
            default_patterns = {
                "assault_rifle": [
                    (-3.0, 0.0), (-4.0, -1.0), (-5.0, 1.0), (-4.0, -2.0),
                    (-3.0, 2.0), (-2.0, -1.0), (-1.0, 1.0)
                ],
                "submachine_gun": [
                    (-2.0, 0.0), (-2.5, -0.5), (-3.0, 0.5), (-2.5, -1.0),
                    (-2.0, 1.0), (-1.5, -0.5), (-1.0, 0.5)
                ],
                "sniper_rifle": [
                    (-8.0, 0.0), (-10.0, -2.0), (-8.0, 2.0)
                ],
                "pistol": [
                    (-1.5, 0.0), (-2.0, -0.5), (-1.5, 0.5)
                ]
            }
            
            pattern = default_patterns.get(weapon, [(-3.0, 0.0), (-4.0, -1.0), (-3.0, 1.0)])
            
            # Format pattern for text area
            pattern_text = "# Recoil pattern for " + weapon.replace('_', ' ').title() + "\n"
            pattern_text += "# Format: vertical_compensation, horizontal_compensation\n"
            
            for vert, horiz in pattern:
                pattern_text += f"{vert}, {horiz}\n"
            
            # Clear and set pattern text
            self.pattern_text.delete("1.0", "end")
            self.pattern_text.insert("1.0", pattern_text)
            
            # Set default sensitivity
            self.sensitivity_var.set(1.0)
            
            # Set default randomization
            self.randomization_var.set(0.15)
            
        except Exception as e:
            self.logger.error(f"Error loading weapon profile: {e}")
    
    def _save_profile(self) -> None:
        """Save current profile configuration."""
        try:
            if not self.selected_weapon:
                return
            
            # Get profile data
            profile_data = {
                'weapon_name': self.weapon_name_var.get(),
                'game': self.selected_game or 'universal',
                'sensitivity_multiplier': self.sensitivity_var.get(),
                'randomization_level': self.randomization_var.get(),
                'pattern': self._parse_pattern_text()
            }
            
            # Save to file (would normally save to database)
            import json
            from pathlib import Path
            
            profiles_dir = Path("config/weapon_profiles")
            profiles_dir.mkdir(parents=True, exist_ok=True)
            
            profile_file = profiles_dir / f"{self.selected_game}_{self.selected_weapon}.json"
            
            with open(profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            self.logger.info(f"Profile saved: {profile_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving profile: {e}")
    
    def _load_profile(self) -> None:
        """Load profile configuration from file."""
        try:
            if not self.selected_weapon:
                return
            
            from pathlib import Path
            import json
            
            profiles_dir = Path("config/weapon_profiles")
            profile_file = profiles_dir / f"{self.selected_game}_{self.selected_weapon}.json"
            
            if profile_file.exists():
                with open(profile_file, 'r') as f:
                    profile_data = json.load(f)
                
                # Update widgets
                self.weapon_name_var.set(profile_data.get('weapon_name', ''))
                self.sensitivity_var.set(profile_data.get('sensitivity_multiplier', 1.0))
                self.randomization_var.set(profile_data.get('randomization_level', 0.15))
                
                # Update pattern text
                pattern = profile_data.get('pattern', [])
                pattern_text = "# Loaded recoil pattern\n"
                pattern_text += "# Format: vertical_compensation, horizontal_compensation\n"
                
                for vert, horiz in pattern:
                    pattern_text += f"{vert}, {horiz}\n"
                
                self.pattern_text.delete("1.0", "end")
                self.pattern_text.insert("1.0", pattern_text)
                
                self.logger.info(f"Profile loaded: {profile_file}")
            
        except Exception as e:
            self.logger.error(f"Error loading profile: {e}")
    
    def _test_pattern(self) -> None:
        """Test the current recoil pattern."""
        try:
            pattern = self._parse_pattern_text()
            if pattern:
                self.logger.info(f"Testing pattern with {len(pattern)} shots")
                # Would implement pattern testing here
                
        except Exception as e:
            self.logger.error(f"Error testing pattern: {e}")
    
    def _activate_profile(self) -> None:
        """Activate the current profile."""
        try:
            if self.selected_weapon and self.engine:
                # Apply current settings to engine
                if hasattr(self.engine, 'set_weapon'):
                    self.engine.set_weapon(self.selected_weapon, self.selected_game or "universal")
                
                if hasattr(self.engine, 'input_handler'):
                    self.engine.input_handler.set_sensitivity(self.sensitivity_var.get())
                
                if hasattr(self.engine, 'security_manager'):
                    self.engine.security_manager.settings.randomization_level = self.randomization_var.get()
                
                self.logger.info(f"Activated profile for {self.selected_weapon}")
                
        except Exception as e:
            self.logger.error(f"Error activating profile: {e}")
    
    def _parse_pattern_text(self) -> List[tuple]:
        """Parse recoil pattern from text area."""
        try:
            pattern = []
            text = self.pattern_text.get("1.0", "end")
            
            for line in text.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            vert = float(parts[0].strip())
                            horiz = float(parts[1].strip())
                            pattern.append((vert, horiz))
                    except ValueError:
                        continue
            
            return pattern
            
        except Exception as e:
            self.logger.error(f"Error parsing pattern text: {e}")
            return []
    
    def show(self) -> None:
        """Show the profiles panel."""
        if self.profiles_frame:
            self.profiles_frame.grid(row=0, column=0, sticky="nsew")
            self.visible = True
            self._update_current_status()
    
    def hide(self) -> None:
        """Hide the profiles panel."""
        if self.profiles_frame:
            self.profiles_frame.grid_remove()
            self.visible = False
    
    def _update_current_status(self) -> None:
        """Update current game and weapon status."""
        try:
            if self.engine:
                # Update current game
                current_game = self.engine.game_detector.get_current_game()
                if current_game:
                    self.current_game_label.configure(text=f"Current: {current_game.display_name}")
                else:
                    self.current_game_label.configure(text="Current: Auto-Detect")
                
                # Update current weapon
                current_weapon = getattr(self.engine, 'current_weapon', None)
                if current_weapon:
                    weapon_display = current_weapon.replace('_', ' ').title()
                    self.current_weapon_label.configure(text=f"Current: {weapon_display}")
                else:
                    self.current_weapon_label.configure(text="Current: None")
            
        except Exception as e:
            self.logger.error(f"Error updating current status: {e}")