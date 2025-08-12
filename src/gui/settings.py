"""
Settings Panel for Hassan Ultimate Anti-Recoil
Comprehensive configuration interface
"""

import logging
import tkinter as tk
from typing import Dict, Any, Optional, List

try:
    import customtkinter as ctk
except ImportError:
    ctk = None


class SettingsPanel:
    """
    Comprehensive settings configuration panel.
    
    Features:
    - Engine configuration
    - Security settings
    - GUI preferences
    - Hotkey configuration
    - Performance tuning
    - Import/Export settings
    """
    
    def __init__(self, parent, engine, config_manager):
        self.parent = parent
        self.engine = engine
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Settings frame
        self.settings_frame = None
        self.visible = False
        
        # Setting widgets
        self.setting_widgets = {}
        
        # Create settings panel
        self._create_settings_panel()
        
        self.logger.info("Settings panel initialized")
    
    def _create_settings_panel(self) -> None:
        """Create the settings interface."""
        try:
            # Main settings frame
            self.settings_frame = ctk.CTkScrollableFrame(self.parent)
            self.settings_frame.grid_columnconfigure(0, weight=1)
            
            # Title
            title_label = ctk.CTkLabel(
                self.settings_frame,
                text="⚙️ Settings Configuration",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title_label.grid(row=0, column=0, pady=20)
            
            # Create setting sections
            row = 1
            row = self._create_engine_settings(row)
            row = self._create_security_settings(row)
            row = self._create_gui_settings(row)
            row = self._create_hotkey_settings(row)
            row = self._create_performance_settings(row)
            self._create_action_buttons(row)
            
        except Exception as e:
            self.logger.error(f"Error creating settings panel: {e}")
    
    def _create_engine_settings(self, start_row: int) -> int:
        """Create engine settings section."""
        try:
            # Engine Settings Frame
            engine_frame = ctk.CTkFrame(self.settings_frame)
            engine_frame.grid(row=start_row, column=0, padx=20, pady=10, sticky="ew")
            engine_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                engine_frame,
                text="🎮 Engine Settings",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            row = 1
            
            # Sensitivity
            sensitivity_label = ctk.CTkLabel(engine_frame, text="Global Sensitivity:")
            sensitivity_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            sensitivity_var = ctk.DoubleVar(value=self.config_manager.get('engine.sensitivity', 1.0))
            sensitivity_slider = ctk.CTkSlider(
                engine_frame, from_=0.1, to=5.0, variable=sensitivity_var,
                command=lambda v: self.config_manager.set('engine.sensitivity', float(v))
            )
            sensitivity_slider.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.setting_widgets['sensitivity'] = sensitivity_var
            row += 1
            
            # Max Latency
            latency_label = ctk.CTkLabel(engine_frame, text="Max Latency (ms):")
            latency_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            latency_var = ctk.DoubleVar(value=self.config_manager.get('engine.max_latency', 0.001) * 1000)
            latency_entry = ctk.CTkEntry(engine_frame, textvariable=latency_var)
            latency_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            latency_entry.bind('<FocusOut>', lambda e: self.config_manager.set('engine.max_latency', latency_var.get() / 1000))
            self.setting_widgets['latency'] = latency_var
            row += 1
            
            return start_row + 1
            
        except Exception as e:
            self.logger.error(f"Error creating engine settings: {e}")
            return start_row + 1
    
    def _create_security_settings(self, start_row: int) -> int:
        """Create security settings section."""
        try:
            # Security Settings Frame
            security_frame = ctk.CTkFrame(self.settings_frame)
            security_frame.grid(row=start_row, column=0, padx=20, pady=10, sticky="ew")
            security_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                security_frame,
                text="🛡️ Security Settings",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            row = 1
            
            # Stealth Mode
            stealth_var = ctk.BooleanVar(value=self.config_manager.get('security.stealth_mode', True))
            stealth_checkbox = ctk.CTkCheckBox(
                security_frame, text="Enable Stealth Mode", variable=stealth_var,
                command=lambda: self.config_manager.set('security.stealth_mode', stealth_var.get())
            )
            stealth_checkbox.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            self.setting_widgets['stealth'] = stealth_var
            row += 1
            
            # Randomization Level
            random_label = ctk.CTkLabel(security_frame, text="Randomization Level:")
            random_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            random_var = ctk.DoubleVar(value=self.config_manager.get('security.randomization', 0.15))
            random_slider = ctk.CTkSlider(
                security_frame, from_=0.0, to=1.0, variable=random_var,
                command=lambda v: self.config_manager.set('security.randomization', float(v))
            )
            random_slider.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.setting_widgets['randomization'] = random_var
            row += 1
            
            # Security Level
            level_label = ctk.CTkLabel(security_frame, text="Security Level:")
            level_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            level_var = ctk.StringVar(value=self.config_manager.get('security.level', 'high'))
            level_menu = ctk.CTkOptionMenu(
                security_frame, values=["low", "medium", "high", "maximum"], variable=level_var,
                command=lambda v: self.config_manager.set('security.level', v)
            )
            level_menu.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.setting_widgets['security_level'] = level_var
            row += 1
            
            return start_row + 1
            
        except Exception as e:
            self.logger.error(f"Error creating security settings: {e}")
            return start_row + 1
    
    def _create_gui_settings(self, start_row: int) -> int:
        """Create GUI settings section."""
        try:
            # GUI Settings Frame
            gui_frame = ctk.CTkFrame(self.settings_frame)
            gui_frame.grid(row=start_row, column=0, padx=20, pady=10, sticky="ew")
            gui_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                gui_frame,
                text="🖥️ GUI Settings",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            row = 1
            
            # Theme
            theme_label = ctk.CTkLabel(gui_frame, text="Theme:")
            theme_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            theme_var = ctk.StringVar(value=self.config_manager.get('gui.theme', 'dark'))
            theme_menu = ctk.CTkOptionMenu(
                gui_frame, values=["dark", "light"], variable=theme_var,
                command=lambda v: self.config_manager.set('gui.theme', v)
            )
            theme_menu.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.setting_widgets['theme'] = theme_var
            row += 1
            
            # Always on Top
            ontop_var = ctk.BooleanVar(value=self.config_manager.get('gui.always_on_top', False))
            ontop_checkbox = ctk.CTkCheckBox(
                gui_frame, text="Always on Top", variable=ontop_var,
                command=lambda: self.config_manager.set('gui.always_on_top', ontop_var.get())
            )
            ontop_checkbox.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            self.setting_widgets['always_on_top'] = ontop_var
            row += 1
            
            return start_row + 1
            
        except Exception as e:
            self.logger.error(f"Error creating GUI settings: {e}")
            return start_row + 1
    
    def _create_hotkey_settings(self, start_row: int) -> int:
        """Create hotkey settings section."""
        try:
            # Hotkey Settings Frame
            hotkey_frame = ctk.CTkFrame(self.settings_frame)
            hotkey_frame.grid(row=start_row, column=0, padx=20, pady=10, sticky="ew")
            hotkey_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                hotkey_frame,
                text="⌨️ Hotkey Settings",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            row = 1
            
            # Hotkey mappings
            hotkeys = [
                ("Toggle Engine", "hotkeys.toggle_engine"),
                ("Next Weapon", "hotkeys.next_weapon"),
                ("Calibrate", "hotkeys.calibrate"),
            ]
            
            for label, config_key in hotkeys:
                hotkey_label = ctk.CTkLabel(hotkey_frame, text=f"{label}:")
                hotkey_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
                
                hotkey_var = ctk.StringVar(value=self.config_manager.get(config_key, 'f1'))
                hotkey_entry = ctk.CTkEntry(hotkey_frame, textvariable=hotkey_var)
                hotkey_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
                hotkey_entry.bind('<FocusOut>', 
                    lambda e, key=config_key, var=hotkey_var: self.config_manager.set(key, var.get()))
                
                self.setting_widgets[config_key] = hotkey_var
                row += 1
            
            return start_row + 1
            
        except Exception as e:
            self.logger.error(f"Error creating hotkey settings: {e}")
            return start_row + 1
    
    def _create_performance_settings(self, start_row: int) -> int:
        """Create performance settings section."""
        try:
            # Performance Settings Frame
            perf_frame = ctk.CTkFrame(self.settings_frame)
            perf_frame.grid(row=start_row, column=0, padx=20, pady=10, sticky="ew")
            perf_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                perf_frame,
                text="⚡ Performance Settings",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            row = 1
            
            # Max History Size
            history_label = ctk.CTkLabel(perf_frame, text="Max History Size:")
            history_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            history_var = ctk.IntVar(value=self.config_manager.get('performance.max_history_size', 10000))
            history_entry = ctk.CTkEntry(perf_frame, textvariable=history_var)
            history_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            history_entry.bind('<FocusOut>', 
                lambda e: self.config_manager.set('performance.max_history_size', history_var.get()))
            self.setting_widgets['max_history'] = history_var
            row += 1
            
            # Metrics Interval
            interval_label = ctk.CTkLabel(perf_frame, text="Metrics Interval (s):")
            interval_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            interval_var = ctk.DoubleVar(value=self.config_manager.get('performance.metrics_interval', 1.0))
            interval_entry = ctk.CTkEntry(perf_frame, textvariable=interval_var)
            interval_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            interval_entry.bind('<FocusOut>', 
                lambda e: self.config_manager.set('performance.metrics_interval', interval_var.get()))
            self.setting_widgets['metrics_interval'] = interval_var
            row += 1
            
            return start_row + 1
            
        except Exception as e:
            self.logger.error(f"Error creating performance settings: {e}")
            return start_row + 1
    
    def _create_action_buttons(self, start_row: int) -> None:
        """Create action buttons section."""
        try:
            # Action Buttons Frame
            action_frame = ctk.CTkFrame(self.settings_frame)
            action_frame.grid(row=start_row, column=0, padx=20, pady=20, sticky="ew")
            action_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            # Reset to Defaults
            reset_btn = ctk.CTkButton(
                action_frame, text="Reset to Defaults",
                command=self._reset_to_defaults
            )
            reset_btn.grid(row=0, column=0, padx=5, pady=10)
            
            # Export Settings
            export_btn = ctk.CTkButton(
                action_frame, text="Export Settings",
                command=self._export_settings
            )
            export_btn.grid(row=0, column=1, padx=5, pady=10)
            
            # Import Settings
            import_btn = ctk.CTkButton(
                action_frame, text="Import Settings",
                command=self._import_settings
            )
            import_btn.grid(row=0, column=2, padx=5, pady=10)
            
            # Apply Settings
            apply_btn = ctk.CTkButton(
                action_frame, text="Apply Settings",
                command=self._apply_settings
            )
            apply_btn.grid(row=0, column=3, padx=5, pady=10)
            
        except Exception as e:
            self.logger.error(f"Error creating action buttons: {e}")
    
    def _reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        try:
            if self.config_manager.reset_to_defaults():
                self._refresh_widgets()
                self.logger.info("Settings reset to defaults")
        except Exception as e:
            self.logger.error(f"Error resetting settings: {e}")
    
    def _export_settings(self) -> None:
        """Export settings to file."""
        try:
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                title="Export Settings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                if self.config_manager.export_config(file_path):
                    self.logger.info(f"Settings exported to {file_path}")
                    
        except Exception as e:
            self.logger.error(f"Error exporting settings: {e}")
    
    def _import_settings(self) -> None:
        """Import settings from file."""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="Import Settings",
                filetypes=[("JSON files", "*.json"), ("YAML files", "*.yaml"), ("All files", "*.*")]
            )
            
            if file_path:
                if self.config_manager.import_config(file_path):
                    self._refresh_widgets()
                    self.logger.info(f"Settings imported from {file_path}")
                    
        except Exception as e:
            self.logger.error(f"Error importing settings: {e}")
    
    def _apply_settings(self) -> None:
        """Apply current settings."""
        try:
            # Force save configuration
            self.config_manager.save()
            self.logger.info("Settings applied")
        except Exception as e:
            self.logger.error(f"Error applying settings: {e}")
    
    def _refresh_widgets(self) -> None:
        """Refresh all setting widgets with current values."""
        try:
            # Update all setting widgets with current config values
            for key, widget_var in self.setting_widgets.items():
                if key == 'sensitivity':
                    widget_var.set(self.config_manager.get('engine.sensitivity', 1.0))
                elif key == 'latency':
                    widget_var.set(self.config_manager.get('engine.max_latency', 0.001) * 1000)
                elif key == 'stealth':
                    widget_var.set(self.config_manager.get('security.stealth_mode', True))
                elif key == 'randomization':
                    widget_var.set(self.config_manager.get('security.randomization', 0.15))
                elif key == 'security_level':
                    widget_var.set(self.config_manager.get('security.level', 'high'))
                elif key == 'theme':
                    widget_var.set(self.config_manager.get('gui.theme', 'dark'))
                elif key == 'always_on_top':
                    widget_var.set(self.config_manager.get('gui.always_on_top', False))
                # Add more widget updates as needed
                    
        except Exception as e:
            self.logger.error(f"Error refreshing widgets: {e}")
    
    def show(self) -> None:
        """Show the settings panel."""
        if self.settings_frame:
            self.settings_frame.grid(row=0, column=0, sticky="nsew")
            self.visible = True
    
    def hide(self) -> None:
        """Hide the settings panel."""
        if self.settings_frame:
            self.settings_frame.grid_remove()
            self.visible = False
    
    def get_current_settings(self) -> Dict[str, Any]:
        """Get current settings from widgets."""
        settings = {}
        try:
            for key, widget_var in self.setting_widgets.items():
                settings[key] = widget_var.get()
        except Exception as e:
            self.logger.error(f"Error getting current settings: {e}")
        return settings