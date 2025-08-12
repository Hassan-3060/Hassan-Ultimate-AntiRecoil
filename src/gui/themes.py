"""
Theme Manager for Hassan Ultimate Anti-Recoil
Advanced theming and appearance management
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import json

try:
    import customtkinter as ctk
except ImportError:
    ctk = None


class ThemeManager:
    """
    Advanced theme and appearance manager.
    
    Features:
    - Dark/Light theme switching
    - Custom color schemes
    - Font configuration
    - Widget styling
    - Theme persistence
    """
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Theme definitions
        self.themes = self._load_themes()
        self.current_theme = self.config_manager.get('gui.theme', 'dark')
        
        # Apply initial theme
        self._apply_theme(self.current_theme)
        
        self.logger.info("Theme manager initialized")
    
    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load theme definitions."""
        try:
            themes = {
                'dark': {
                    'name': 'Dark',
                    'appearance_mode': 'dark',
                    'color_theme': 'blue',
                    'colors': {
                        'primary': '#1f538d',
                        'secondary': '#14375e',
                        'background': '#212121',
                        'surface': '#2b2b2b',
                        'text': '#ffffff',
                        'text_secondary': '#b0b0b0',
                        'accent': '#1f538d',
                        'success': '#4caf50',
                        'warning': '#ff9800',
                        'error': '#f44336'
                    },
                    'fonts': {
                        'default': ('Segoe UI', 12),
                        'heading': ('Segoe UI', 16, 'bold'),
                        'small': ('Segoe UI', 10),
                        'mono': ('Consolas', 10)
                    }
                },
                'light': {
                    'name': 'Light',
                    'appearance_mode': 'light',
                    'color_theme': 'blue',
                    'colors': {
                        'primary': '#1976d2',
                        'secondary': '#1565c0',
                        'background': '#ffffff',
                        'surface': '#f5f5f5',
                        'text': '#000000',
                        'text_secondary': '#666666',
                        'accent': '#1976d2',
                        'success': '#388e3c',
                        'warning': '#f57c00',
                        'error': '#d32f2f'
                    },
                    'fonts': {
                        'default': ('Segoe UI', 12),
                        'heading': ('Segoe UI', 16, 'bold'),
                        'small': ('Segoe UI', 10),
                        'mono': ('Consolas', 10)
                    }
                },
                'cyberpunk': {
                    'name': 'Cyberpunk',
                    'appearance_mode': 'dark',
                    'color_theme': 'green',
                    'colors': {
                        'primary': '#00ff88',
                        'secondary': '#00cc6a',
                        'background': '#0a0a0a',
                        'surface': '#1a1a1a',
                        'text': '#00ff88',
                        'text_secondary': '#66cc99',
                        'accent': '#ff0080',
                        'success': '#00ff88',
                        'warning': '#ffff00',
                        'error': '#ff0080'
                    },
                    'fonts': {
                        'default': ('Courier New', 12),
                        'heading': ('Courier New', 16, 'bold'),
                        'small': ('Courier New', 10),
                        'mono': ('Courier New', 10)
                    }
                }
            }
            
            # Try to load custom themes from file
            themes_file = Path("config/themes.json")
            if themes_file.exists():
                with open(themes_file, 'r') as f:
                    custom_themes = json.load(f)
                    themes.update(custom_themes)
            
            return themes
            
        except Exception as e:
            self.logger.error(f"Error loading themes: {e}")
            return {
                'dark': {'name': 'Dark', 'appearance_mode': 'dark', 'color_theme': 'blue'},
                'light': {'name': 'Light', 'appearance_mode': 'light', 'color_theme': 'blue'}
            }
    
    def _apply_theme(self, theme_name: str) -> None:
        """Apply a theme."""
        try:
            if not ctk:
                return
            
            if theme_name not in self.themes:
                self.logger.warning(f"Unknown theme: {theme_name}")
                theme_name = 'dark'
            
            theme = self.themes[theme_name]
            
            # Set CustomTkinter appearance mode
            appearance_mode = theme.get('appearance_mode', 'dark')
            ctk.set_appearance_mode(appearance_mode)
            
            # Set color theme
            color_theme = theme.get('color_theme', 'blue')
            ctk.set_default_color_theme(color_theme)
            
            self.current_theme = theme_name
            self.logger.info(f"Applied theme: {theme_name}")
            
        except Exception as e:
            self.logger.error(f"Error applying theme: {e}")
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the current theme."""
        try:
            if theme_name in self.themes:
                self._apply_theme(theme_name)
                self.config_manager.set('gui.theme', theme_name)
                return True
            else:
                self.logger.error(f"Theme not found: {theme_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting theme: {e}")
            return False
    
    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return self.current_theme
    
    def get_available_themes(self) -> Dict[str, str]:
        """Get available themes."""
        return {name: theme.get('name', name) for name, theme in self.themes.items()}
    
    def get_theme_colors(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        """Get colors for a theme."""
        if theme_name is None:
            theme_name = self.current_theme
        
        theme = self.themes.get(theme_name, self.themes['dark'])
        return theme.get('colors', {})
    
    def get_theme_fonts(self, theme_name: Optional[str] = None) -> Dict[str, tuple]:
        """Get fonts for a theme."""
        if theme_name is None:
            theme_name = self.current_theme
        
        theme = self.themes.get(theme_name, self.themes['dark'])
        return theme.get('fonts', {})
    
    def create_styled_widget(self, widget_class, parent, style_name: str = 'default', **kwargs):
        """Create a styled widget."""
        try:
            if not ctk:
                return None
            
            # Get theme colors
            colors = self.get_theme_colors()
            
            # Apply style-specific colors
            if style_name == 'primary':
                kwargs.setdefault('fg_color', colors.get('primary'))
                kwargs.setdefault('text_color', colors.get('text'))
            elif style_name == 'secondary':
                kwargs.setdefault('fg_color', colors.get('secondary'))
                kwargs.setdefault('text_color', colors.get('text'))
            elif style_name == 'success':
                kwargs.setdefault('fg_color', colors.get('success'))
                kwargs.setdefault('text_color', colors.get('text'))
            elif style_name == 'warning':
                kwargs.setdefault('fg_color', colors.get('warning'))
                kwargs.setdefault('text_color', colors.get('text'))
            elif style_name == 'error':
                kwargs.setdefault('fg_color', colors.get('error'))
                kwargs.setdefault('text_color', colors.get('text'))
            
            # Create and return widget
            return widget_class(parent, **kwargs)
            
        except Exception as e:
            self.logger.error(f"Error creating styled widget: {e}")
            return widget_class(parent, **kwargs)
    
    def get_font(self, font_name: str = 'default') -> tuple:
        """Get a font tuple for the current theme."""
        fonts = self.get_theme_fonts()
        return fonts.get(font_name, ('Segoe UI', 12))
    
    def create_font(self, font_name: str = 'default', size: Optional[int] = None, weight: Optional[str] = None):
        """Create a CustomTkinter font object."""
        try:
            if not ctk:
                return None
            
            font_tuple = self.get_font(font_name)
            
            # Override size and weight if provided
            family = font_tuple[0]
            font_size = size if size is not None else (font_tuple[1] if len(font_tuple) > 1 else 12)
            font_weight = weight if weight is not None else (font_tuple[2] if len(font_tuple) > 2 else 'normal')
            
            return ctk.CTkFont(family=family, size=font_size, weight=font_weight)
            
        except Exception as e:
            self.logger.error(f"Error creating font: {e}")
            return None
    
    def export_theme(self, theme_name: str, file_path: str) -> bool:
        """Export a theme to file."""
        try:
            if theme_name not in self.themes:
                self.logger.error(f"Theme not found: {theme_name}")
                return False
            
            theme_data = self.themes[theme_name]
            
            with open(file_path, 'w') as f:
                json.dump({theme_name: theme_data}, f, indent=2)
            
            self.logger.info(f"Theme exported: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting theme: {e}")
            return False
    
    def import_theme(self, file_path: str) -> bool:
        """Import a theme from file."""
        try:
            with open(file_path, 'r') as f:
                imported_themes = json.load(f)
            
            # Add imported themes
            self.themes.update(imported_themes)
            
            # Save to themes file
            themes_file = Path("config/themes.json")
            themes_file.parent.mkdir(exist_ok=True)
            
            with open(themes_file, 'w') as f:
                json.dump(self.themes, f, indent=2)
            
            self.logger.info(f"Theme imported: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing theme: {e}")
            return False
    
    def create_custom_theme(self, name: str, base_theme: str = 'dark', **overrides) -> bool:
        """Create a custom theme based on an existing theme."""
        try:
            if base_theme not in self.themes:
                self.logger.error(f"Base theme not found: {base_theme}")
                return False
            
            # Copy base theme
            new_theme = self.themes[base_theme].copy()
            new_theme['name'] = name
            
            # Apply overrides
            for key, value in overrides.items():
                if key == 'colors' and isinstance(value, dict):
                    new_theme.setdefault('colors', {}).update(value)
                elif key == 'fonts' and isinstance(value, dict):
                    new_theme.setdefault('fonts', {}).update(value)
                else:
                    new_theme[key] = value
            
            # Add to themes
            self.themes[name] = new_theme
            
            self.logger.info(f"Created custom theme: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating custom theme: {e}")
            return False
    
    def delete_theme(self, theme_name: str) -> bool:
        """Delete a custom theme."""
        try:
            if theme_name in ['dark', 'light']:
                self.logger.error("Cannot delete built-in themes")
                return False
            
            if theme_name not in self.themes:
                self.logger.error(f"Theme not found: {theme_name}")
                return False
            
            # Switch to default theme if deleting current theme
            if theme_name == self.current_theme:
                self.set_theme('dark')
            
            # Delete theme
            del self.themes[theme_name]
            
            self.logger.info(f"Deleted theme: {theme_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting theme: {e}")
            return False
    
    def get_status_color(self, status: str) -> str:
        """Get color for a status indicator."""
        colors = self.get_theme_colors()
        
        status_colors = {
            'active': colors.get('success', '#4caf50'),
            'inactive': colors.get('text_secondary', '#666666'),
            'paused': colors.get('warning', '#ff9800'),
            'error': colors.get('error', '#f44336'),
            'calibrating': colors.get('accent', '#1976d2')
        }
        
        return status_colors.get(status.lower(), colors.get('text', '#000000'))