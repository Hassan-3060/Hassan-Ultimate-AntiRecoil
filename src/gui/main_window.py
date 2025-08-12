"""
Main Window for Hassan Ultimate Anti-Recoil v7.0
Modern CustomTkinter interface with real-time dashboard and controls
"""

import logging
import asyncio
import threading
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, Optional

try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
except ImportError:
    # Fallback for testing
    ctk = None
    Image = None
    ImageTk = None

from src.gui.dashboard import Dashboard
from src.gui.settings import SettingsPanel
from src.gui.profiles import ProfilesPanel
from src.gui.themes import ThemeManager


class MainWindow:
    """
    Main application window with modern CustomTkinter interface.
    
    Features:
    - Modern dark/light theme support
    - Real-time dashboard with metrics
    - Comprehensive settings panel
    - Profile management interface
    - Status monitoring and controls
    - Responsive layout design
    """
    
    def __init__(self, engine, config_manager):
        self.engine = engine
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Check if CustomTkinter is available
        if not ctk:
            self.logger.error("CustomTkinter not available - GUI will not work")
            raise ImportError("CustomTkinter required for GUI")
        
        # GUI components
        self.root: Optional[ctk.CTk] = None
        self.theme_manager: Optional[ThemeManager] = None
        self.dashboard: Optional[Dashboard] = None
        self.settings_panel: Optional[SettingsPanel] = None
        self.profiles_panel: Optional[ProfilesPanel] = None
        
        # Layout frames
        self.main_frame: Optional[ctk.CTkFrame] = None
        self.sidebar_frame: Optional[ctk.CTkFrame] = None
        self.content_frame: Optional[ctk.CTkFrame] = None
        
        # Control widgets
        self.status_label: Optional[ctk.CTkLabel] = None
        self.toggle_button: Optional[ctk.CTkButton] = None
        self.current_game_label: Optional[ctk.CTkLabel] = None
        self.current_weapon_label: Optional[ctk.CTkLabel] = None
        
        # State
        self.current_panel = "dashboard"
        self.running = False
        
        # Initialize GUI
        self._create_window()
        self._setup_layout()
        self._setup_components()
        self._setup_bindings()
        
        self.logger.info("Main window initialized")
    
    def _create_window(self) -> None:
        """Create the main application window."""
        try:
            # Set appearance mode and theme
            ctk.set_appearance_mode(self.config_manager.get('gui.theme', 'dark'))
            ctk.set_default_color_theme("blue")
            
            # Create main window
            self.root = ctk.CTk()
            self.root.title("Hassan Ultimate Anti-Recoil v7.0 - Professional Edition")
            
            # Window configuration
            window_size = self.config_manager.get('gui.window_size', [1200, 800])
            self.root.geometry(f"{window_size[0]}x{window_size[1]}")
            self.root.minsize(800, 600)
            
            # Window icon (if available)
            try:
                icon_path = "assets/icons/app_icon.ico"
                self.root.iconbitmap(icon_path)
            except:
                pass  # Icon not available
            
            # Center window on screen
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (window_size[0] // 2)
            y = (self.root.winfo_screenheight() // 2) - (window_size[1] // 2)
            self.root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")
            
            # Always on top setting
            if self.config_manager.get('gui.always_on_top', False):
                self.root.attributes('-topmost', True)
            
            self.logger.debug("Main window created")
            
        except Exception as e:
            self.logger.error(f"Error creating main window: {e}")
            raise
    
    def _setup_layout(self) -> None:
        """Setup the main window layout."""
        try:
            # Configure grid weights
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_rowconfigure(0, weight=1)
            
            # Create main frames
            self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
            self.sidebar_frame.grid_propagate(False)
            
            self.content_frame = ctk.CTkFrame(self.root, corner_radius=0)
            self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            # Status bar frame
            self.status_frame = ctk.CTkFrame(self.root, height=40, corner_radius=0)
            self.status_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 10))
            self.status_frame.grid_columnconfigure(1, weight=1)
            
            self.logger.debug("Main layout setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up layout: {e}")
            raise
    
    def _setup_components(self) -> None:
        """Setup GUI components."""
        try:
            # Initialize theme manager
            self.theme_manager = ThemeManager(self.config_manager)
            
            # Setup sidebar
            self._setup_sidebar()
            
            # Setup status bar
            self._setup_status_bar()
            
            # Initialize panels
            self.dashboard = Dashboard(self.content_frame, self.engine, self.config_manager)
            self.settings_panel = SettingsPanel(self.content_frame, self.engine, self.config_manager)
            self.profiles_panel = ProfilesPanel(self.content_frame, self.engine, self.config_manager)
            
            # Show default panel
            self._show_panel("dashboard")
            
            self.logger.debug("GUI components setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up components: {e}")
            raise
    
    def _setup_sidebar(self) -> None:
        """Setup the sidebar navigation."""
        try:
            # App title and version
            title_label = ctk.CTkLabel(
                self.sidebar_frame,
                text="Hassan Ultimate\nAnti-Recoil v7.0",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.grid(row=0, column=0, padx=20, pady=(20, 30))
            
            # Navigation buttons
            nav_buttons = [
                ("Dashboard", "dashboard", "📊"),
                ("Profiles", "profiles", "🎮"),
                ("Settings", "settings", "⚙️"),
            ]
            
            self.nav_buttons = {}
            
            for i, (text, panel_id, icon) in enumerate(nav_buttons):
                btn = ctk.CTkButton(
                    self.sidebar_frame,
                    text=f"{icon} {text}",
                    command=lambda p=panel_id: self._show_panel(p),
                    height=40,
                    font=ctk.CTkFont(size=14)
                )
                btn.grid(row=i+1, column=0, padx=20, pady=5, sticky="ew")
                self.nav_buttons[panel_id] = btn
            
            # Engine control section
            control_frame = ctk.CTkFrame(self.sidebar_frame)
            control_frame.grid(row=10, column=0, padx=20, pady=20, sticky="ew")
            
            control_label = ctk.CTkLabel(
                control_frame,
                text="Engine Control",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            control_label.grid(row=0, column=0, padx=10, pady=(10, 5))
            
            # Toggle button
            self.toggle_button = ctk.CTkButton(
                control_frame,
                text="🔴 Start Engine",
                command=self._toggle_engine,
                height=35,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            self.toggle_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
            
            # Current game/weapon display
            self.current_game_label = ctk.CTkLabel(
                control_frame,
                text="Game: Not Detected",
                font=ctk.CTkFont(size=10)
            )
            self.current_game_label.grid(row=2, column=0, padx=10, pady=2)
            
            self.current_weapon_label = ctk.CTkLabel(
                control_frame,
                text="Weapon: None",
                font=ctk.CTkFont(size=10)
            )
            self.current_weapon_label.grid(row=3, column=0, padx=10, pady=(2, 10))
            
            # Configure sidebar grid
            self.sidebar_frame.grid_rowconfigure(20, weight=1)
            
        except Exception as e:
            self.logger.error(f"Error setting up sidebar: {e}")
    
    def _setup_status_bar(self) -> None:
        """Setup the status bar."""
        try:
            # Status indicator
            self.status_indicator = ctk.CTkLabel(
                self.status_frame,
                text="🔴",
                font=ctk.CTkFont(size=16)
            )
            self.status_indicator.grid(row=0, column=0, padx=10, pady=5)
            
            # Status text
            self.status_label = ctk.CTkLabel(
                self.status_frame,
                text="Engine Stopped",
                font=ctk.CTkFont(size=12)
            )
            self.status_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            # Performance metrics
            self.perf_label = ctk.CTkLabel(
                self.status_frame,
                text="Latency: N/A | Shots: 0",
                font=ctk.CTkFont(size=10)
            )
            self.perf_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
            
        except Exception as e:
            self.logger.error(f"Error setting up status bar: {e}")
    
    def _setup_bindings(self) -> None:
        """Setup event bindings."""
        try:
            # Window close event
            self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)
            
            # Configuration change callbacks
            self.config_manager.add_change_callback(self._on_config_change)
            
            # Keyboard shortcuts
            self.root.bind('<F1>', lambda e: self._toggle_engine())
            self.root.bind('<F2>', lambda e: self._show_panel('profiles'))
            self.root.bind('<F3>', lambda e: self._show_panel('settings'))
            self.root.bind('<Control-q>', lambda e: self._on_window_close())
            
            self.logger.debug("Event bindings setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up bindings: {e}")
    
    def _show_panel(self, panel_id: str) -> None:
        """Show a specific panel."""
        try:
            # Hide all panels
            if self.dashboard:
                self.dashboard.hide()
            if self.settings_panel:
                self.settings_panel.hide()
            if self.profiles_panel:
                self.profiles_panel.hide()
            
            # Show selected panel
            if panel_id == "dashboard":
                self.dashboard.show()
            elif panel_id == "settings":
                self.settings_panel.show()
            elif panel_id == "profiles":
                self.profiles_panel.show()
            
            # Update navigation button states
            for btn_id, btn in self.nav_buttons.items():
                if btn_id == panel_id:
                    btn.configure(fg_color=("gray75", "gray25"))
                else:
                    btn.configure(fg_color=("gray84", "gray16"))
            
            self.current_panel = panel_id
            self.logger.debug(f"Switched to panel: {panel_id}")
            
        except Exception as e:
            self.logger.error(f"Error showing panel {panel_id}: {e}")
    
    def _toggle_engine(self) -> None:
        """Toggle the anti-recoil engine."""
        try:
            if not self.engine:
                return
            
            if self.engine.state.value == "active":
                # Stop engine
                asyncio.create_task(self.engine.stop())
                self.toggle_button.configure(text="🔴 Start Engine")
                self.status_label.configure(text="Engine Stopped")
                self.status_indicator.configure(text="🔴")
            else:
                # Start engine
                asyncio.create_task(self.engine.start())
                self.toggle_button.configure(text="🟢 Stop Engine")
                self.status_label.configure(text="Engine Running")
                self.status_indicator.configure(text="🟢")
            
        except Exception as e:
            self.logger.error(f"Error toggling engine: {e}")
            messagebox.showerror("Error", f"Failed to toggle engine: {e}")
    
    def _on_config_change(self, key: str, old_value: Any, new_value: Any) -> None:
        """Handle configuration changes."""
        try:
            if key == 'gui.theme':
                ctk.set_appearance_mode(new_value)
            elif key == 'gui.always_on_top':
                self.root.attributes('-topmost', new_value)
            elif key == 'gui.window_size':
                self.root.geometry(f"{new_value[0]}x{new_value[1]}")
            
        except Exception as e:
            self.logger.error(f"Error handling config change: {e}")
    
    def _update_status(self) -> None:
        """Update status displays."""
        try:
            if not self.engine:
                return
            
            # Update game detection
            current_game = self.engine.game_detector.get_current_game()
            if current_game:
                self.current_game_label.configure(text=f"Game: {current_game.display_name}")
            else:
                self.current_game_label.configure(text="Game: Not Detected")
            
            # Update weapon
            if hasattr(self.engine, 'current_weapon') and self.engine.current_weapon:
                self.current_weapon_label.configure(text=f"Weapon: {self.engine.current_weapon}")
            else:
                self.current_weapon_label.configure(text="Weapon: None")
            
            # Update performance metrics
            metrics = self.engine.get_performance_metrics()
            latency = metrics.get('average_latency', 0) * 1000  # Convert to ms
            shots = metrics.get('shots_fired', 0)
            self.perf_label.configure(text=f"Latency: {latency:.1f}ms | Shots: {shots}")
            
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
    
    def _status_update_loop(self) -> None:
        """Status update loop (runs in separate thread)."""
        while self.running:
            try:
                # Update status on main thread
                self.root.after(0, self._update_status)
                
                # Sleep for update interval
                threading.Event().wait(1.0)  # Update every second
                
            except Exception as e:
                self.logger.error(f"Error in status update loop: {e}")
    
    def _on_window_close(self) -> None:
        """Handle window close event."""
        try:
            self.logger.info("Closing application...")
            
            # Stop engine if running
            if self.engine and self.engine.state.value == "active":
                asyncio.create_task(self.engine.stop())
            
            # Save configuration
            if self.config_manager and self.config_manager.has_unsaved_changes():
                asyncio.create_task(self.config_manager.save())
            
            # Stop GUI update loop
            self.running = False
            
            # Destroy window
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            self.logger.error(f"Error closing window: {e}")
    
    def run(self) -> None:
        """Run the GUI application."""
        try:
            self.logger.info("Starting GUI application...")
            
            # Start status update loop
            self.running = True
            status_thread = threading.Thread(target=self._status_update_loop, daemon=True)
            status_thread.start()
            
            # Start main GUI loop
            self.root.mainloop()
            
        except Exception as e:
            self.logger.error(f"Error running GUI: {e}")
            raise
        finally:
            self.running = False
    
    # Public API methods
    
    def show_message(self, title: str, message: str, type: str = "info") -> None:
        """Show a message dialog."""
        try:
            if type == "error":
                messagebox.showerror(title, message)
            elif type == "warning":
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
        except Exception as e:
            self.logger.error(f"Error showing message: {e}")
    
    def ask_confirmation(self, title: str, message: str) -> bool:
        """Ask for user confirmation."""
        try:
            return messagebox.askyesno(title, message)
        except Exception as e:
            self.logger.error(f"Error asking confirmation: {e}")
            return False
    
    def get_current_panel(self) -> str:
        """Get currently active panel."""
        return self.current_panel
    
    def switch_to_panel(self, panel_id: str) -> None:
        """Switch to a specific panel."""
        self._show_panel(panel_id)
    
    def update_theme(self, theme: str) -> None:
        """Update GUI theme."""
        try:
            ctk.set_appearance_mode(theme)
            self.config_manager.set('gui.theme', theme)
        except Exception as e:
            self.logger.error(f"Error updating theme: {e}")