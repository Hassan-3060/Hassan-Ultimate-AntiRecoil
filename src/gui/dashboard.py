"""
Real-time Dashboard for Hassan Ultimate Anti-Recoil
Advanced analytics and monitoring interface
"""

import logging
import tkinter as tk
from typing import Dict, Any, List, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
import time

try:
    import customtkinter as ctk
    matplotlib_available = True
except ImportError:
    ctk = None
    matplotlib_available = False


class MetricsChart:
    """Real-time metrics chart widget."""
    
    def __init__(self, parent, title: str, y_label: str, max_points: int = 100):
        self.parent = parent
        self.title = title
        self.y_label = y_label
        self.max_points = max_points
        
        # Data storage
        self.x_data = deque(maxlen=max_points)
        self.y_data = deque(maxlen=max_points)
        
        # Create matplotlib figure
        if matplotlib_available:
            self.fig, self.ax = plt.subplots(figsize=(6, 3))
            self.ax.set_title(title)
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel(y_label)
            self.line, = self.ax.plot([], [], 'b-')
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.fig, parent)
            self.canvas_widget = self.canvas.get_tk_widget()
        else:
            # Fallback to simple text display
            self.canvas_widget = ctk.CTkLabel(parent, text=f"{title}: No data")
    
    def add_data_point(self, value: float) -> None:
        """Add a new data point."""
        if not matplotlib_available:
            self.canvas_widget.configure(text=f"{self.title}: {value:.2f}")
            return
        
        current_time = time.time()
        self.x_data.append(current_time)
        self.y_data.append(value)
        
        # Update plot
        if len(self.x_data) > 1:
            # Convert to relative time
            start_time = self.x_data[0]
            x_relative = [(t - start_time) for t in self.x_data]
            
            self.line.set_data(x_relative, list(self.y_data))
            self.ax.relim()
            self.ax.autoscale_view()
            
            self.canvas.draw()
    
    def clear(self) -> None:
        """Clear chart data."""
        self.x_data.clear()
        self.y_data.clear()
        
        if matplotlib_available:
            self.line.set_data([], [])
            self.canvas.draw()
    
    def get_widget(self):
        """Get the chart widget."""
        return self.canvas_widget


class Dashboard:
    """
    Real-time dashboard with comprehensive analytics.
    
    Features:
    - Live performance metrics
    - Real-time charts and graphs
    - Engine status monitoring
    - Security metrics display
    - Game detection status
    - AI pattern analysis
    """
    
    def __init__(self, parent, engine, config_manager):
        self.parent = parent
        self.engine = engine
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        
        # Main dashboard frame
        self.dashboard_frame = None
        self.visible = False
        
        # Metric widgets
        self.metrics_widgets = {}
        self.charts = {}
        
        # Create dashboard
        self._create_dashboard()
        
        self.logger.info("Dashboard initialized")
    
    def _create_dashboard(self) -> None:
        """Create the dashboard interface."""
        try:
            # Main dashboard frame
            self.dashboard_frame = ctk.CTkFrame(self.parent)
            self.dashboard_frame.grid_columnconfigure((0, 1), weight=1)
            self.dashboard_frame.grid_rowconfigure((1, 2, 3), weight=1)
            
            # Title
            title_label = ctk.CTkLabel(
                self.dashboard_frame,
                text="📊 Real-time Dashboard",
                font=ctk.CTkFont(size=24, weight="bold")
            )
            title_label.grid(row=0, column=0, columnspan=2, pady=20)
            
            # Create sections
            self._create_engine_status_section()
            self._create_performance_section()
            self._create_security_section()
            self._create_ai_section()
            
        except Exception as e:
            self.logger.error(f"Error creating dashboard: {e}")
    
    def _create_engine_status_section(self) -> None:
        """Create engine status section."""
        try:
            # Engine Status Frame
            status_frame = ctk.CTkFrame(self.dashboard_frame)
            status_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            status_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                status_frame,
                text="🎮 Engine Status",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            # Status indicators
            status_items = [
                ("Engine State", "engine_state"),
                ("Current Game", "current_game"),
                ("Current Weapon", "current_weapon"),
                ("Auto Detection", "auto_detection"),
                ("Stealth Mode", "stealth_mode"),
            ]
            
            for i, (label, key) in enumerate(status_items):
                label_widget = ctk.CTkLabel(status_frame, text=f"{label}:")
                label_widget.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
                
                value_widget = ctk.CTkLabel(status_frame, text="Unknown")
                value_widget.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
                
                self.metrics_widgets[key] = value_widget
            
        except Exception as e:
            self.logger.error(f"Error creating engine status section: {e}")
    
    def _create_performance_section(self) -> None:
        """Create performance metrics section."""
        try:
            # Performance Frame
            perf_frame = ctk.CTkFrame(self.dashboard_frame)
            perf_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
            perf_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                perf_frame,
                text="⚡ Performance Metrics",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            # Performance metrics
            perf_items = [
                ("Average Latency", "avg_latency"),
                ("Shots Fired", "shots_fired"),
                ("Compensations Applied", "compensations"),
                ("Shots per Minute", "shots_per_minute"),
                ("Uptime", "uptime"),
            ]
            
            for i, (label, key) in enumerate(perf_items):
                label_widget = ctk.CTkLabel(perf_frame, text=f"{label}:")
                label_widget.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
                
                value_widget = ctk.CTkLabel(perf_frame, text="0")
                value_widget.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
                
                self.metrics_widgets[key] = value_widget
            
            # Latency chart
            if matplotlib_available:
                chart_frame = ctk.CTkFrame(perf_frame)
                chart_frame.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
                
                self.charts["latency"] = MetricsChart(chart_frame, "Latency (ms)", "Milliseconds")
                self.charts["latency"].get_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            self.logger.error(f"Error creating performance section: {e}")
    
    def _create_security_section(self) -> None:
        """Create security metrics section."""
        try:
            # Security Frame
            security_frame = ctk.CTkFrame(self.dashboard_frame)
            security_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            security_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                security_frame,
                text="🛡️ Security Status",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            # Security metrics
            security_items = [
                ("Security Level", "security_level"),
                ("Detection Risk", "detection_risk"),
                ("Randomizations", "randomizations"),
                ("Stealth Operations", "stealth_ops"),
                ("Suspicious Processes", "suspicious_procs"),
            ]
            
            for i, (label, key) in enumerate(security_items):
                label_widget = ctk.CTkLabel(security_frame, text=f"{label}:")
                label_widget.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
                
                value_widget = ctk.CTkLabel(security_frame, text="Unknown")
                value_widget.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
                
                self.metrics_widgets[key] = value_widget
            
        except Exception as e:
            self.logger.error(f"Error creating security section: {e}")
    
    def _create_ai_section(self) -> None:
        """Create AI metrics section."""
        try:
            # AI Frame
            ai_frame = ctk.CTkFrame(self.dashboard_frame)
            ai_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
            ai_frame.grid_columnconfigure(1, weight=1)
            
            # Section title
            title = ctk.CTkLabel(
                ai_frame,
                text="🤖 AI Pattern Recognition",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title.grid(row=0, column=0, columnspan=2, pady=10)
            
            # AI metrics
            ai_items = [
                ("Patterns Learned", "patterns_learned"),
                ("Shots Recorded", "shots_recorded"),
                ("Pattern Confidence", "pattern_confidence"),
                ("Learning Enabled", "learning_enabled"),
                ("Model Trained", "model_trained"),
            ]
            
            for i, (label, key) in enumerate(ai_items):
                label_widget = ctk.CTkLabel(ai_frame, text=f"{label}:")
                label_widget.grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
                
                value_widget = ctk.CTkLabel(ai_frame, text="Unknown")
                value_widget.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
                
                self.metrics_widgets[key] = value_widget
            
            # Confidence chart
            if matplotlib_available:
                chart_frame = ctk.CTkFrame(ai_frame)
                chart_frame.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
                
                self.charts["confidence"] = MetricsChart(chart_frame, "Pattern Confidence", "Confidence")
                self.charts["confidence"].get_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            self.logger.error(f"Error creating AI section: {e}")
    
    def update_metrics(self) -> None:
        """Update all dashboard metrics."""
        try:
            if not self.visible or not self.engine:
                return
            
            # Engine status metrics
            self._update_engine_metrics()
            
            # Performance metrics
            self._update_performance_metrics()
            
            # Security metrics
            self._update_security_metrics()
            
            # AI metrics
            self._update_ai_metrics()
            
        except Exception as e:
            self.logger.error(f"Error updating metrics: {e}")
    
    def _update_engine_metrics(self) -> None:
        """Update engine status metrics."""
        try:
            # Engine state
            state = self.engine.state.value.title()
            self.metrics_widgets["engine_state"].configure(text=state)
            
            # Current game
            current_game = self.engine.game_detector.get_current_game()
            game_name = current_game.display_name if current_game else "Not Detected"
            self.metrics_widgets["current_game"].configure(text=game_name)
            
            # Current weapon
            weapon = getattr(self.engine, 'current_weapon', None) or "None"
            self.metrics_widgets["current_weapon"].configure(text=weapon)
            
            # Auto detection
            auto_detect = self.engine.game_detector.detection_enabled
            self.metrics_widgets["auto_detection"].configure(text="Enabled" if auto_detect else "Disabled")
            
            # Stealth mode
            stealth = self.engine.security_manager.settings.stealth_mode
            self.metrics_widgets["stealth_mode"].configure(text="Enabled" if stealth else "Disabled")
            
        except Exception as e:
            self.logger.error(f"Error updating engine metrics: {e}")
    
    def _update_performance_metrics(self) -> None:
        """Update performance metrics."""
        try:
            metrics = self.engine.get_performance_metrics()
            
            # Average latency
            latency = metrics.get('average_latency', 0) * 1000  # Convert to ms
            self.metrics_widgets["avg_latency"].configure(text=f"{latency:.2f} ms")
            
            # Add to latency chart
            if "latency" in self.charts:
                self.charts["latency"].add_data_point(latency)
            
            # Shots fired
            shots = metrics.get('shots_fired', 0)
            self.metrics_widgets["shots_fired"].configure(text=str(shots))
            
            # Compensations applied
            compensations = metrics.get('compensations_applied', 0)
            self.metrics_widgets["compensations"].configure(text=str(compensations))
            
            # Shots per minute
            spm = metrics.get('shots_per_minute', 0)
            self.metrics_widgets["shots_per_minute"].configure(text=f"{spm:.1f}")
            
            # Uptime
            uptime = metrics.get('uptime', 0)
            uptime_str = f"{int(uptime // 60)}m {int(uptime % 60)}s"
            self.metrics_widgets["uptime"].configure(text=uptime_str)
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")
    
    def _update_security_metrics(self) -> None:
        """Update security metrics."""
        try:
            security_status = self.engine.security_manager.get_security_status()
            
            # Security level
            level = security_status.get('security_level', 'unknown').title()
            self.metrics_widgets["security_level"].configure(text=level)
            
            # Detection risk
            risk = security_status.get('detection_risk_score', 0) * 100
            self.metrics_widgets["detection_risk"].configure(text=f"{risk:.1f}%")
            
            # Security metrics
            metrics = security_status.get('metrics', {})
            
            randomizations = metrics.get('randomizations_applied', 0)
            self.metrics_widgets["randomizations"].configure(text=str(randomizations))
            
            stealth_ops = metrics.get('stealth_operations', 0)
            self.metrics_widgets["stealth_ops"].configure(text=str(stealth_ops))
            
            # Suspicious processes
            suspicious = security_status.get('suspicious_processes', 0)
            self.metrics_widgets["suspicious_procs"].configure(text=str(suspicious))
            
        except Exception as e:
            self.logger.error(f"Error updating security metrics: {e}")
    
    def _update_ai_metrics(self) -> None:
        """Update AI metrics."""
        try:
            ai_metrics = self.engine.pattern_ai.get_pattern_metrics()
            
            # Patterns learned
            patterns = ai_metrics.get('total_patterns_learned', 0)
            self.metrics_widgets["patterns_learned"].configure(text=str(patterns))
            
            # Shots recorded
            shots = ai_metrics.get('total_shots_recorded', 0)
            self.metrics_widgets["shots_recorded"].configure(text=str(shots))
            
            # Pattern confidence
            confidence = ai_metrics.get('average_pattern_confidence', 0) * 100
            self.metrics_widgets["pattern_confidence"].configure(text=f"{confidence:.1f}%")
            
            # Add to confidence chart
            if "confidence" in self.charts:
                self.charts["confidence"].add_data_point(confidence)
            
            # Learning enabled
            learning = ai_metrics.get('learning_enabled', False)
            self.metrics_widgets["learning_enabled"].configure(text="Enabled" if learning else "Disabled")
            
            # Model trained
            trained = ai_metrics.get('model_trained', False)
            self.metrics_widgets["model_trained"].configure(text="Yes" if trained else "No")
            
        except Exception as e:
            self.logger.error(f"Error updating AI metrics: {e}")
    
    def show(self) -> None:
        """Show the dashboard."""
        if self.dashboard_frame:
            self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
            self.visible = True
    
    def hide(self) -> None:
        """Hide the dashboard."""
        if self.dashboard_frame:
            self.dashboard_frame.grid_remove()
            self.visible = False
    
    def clear_charts(self) -> None:
        """Clear all chart data."""
        for chart in self.charts.values():
            chart.clear()
    
    def export_metrics(self, file_path: str) -> bool:
        """Export current metrics to file."""
        try:
            # Collect all current metrics
            metrics_data = {
                'timestamp': time.time(),
                'engine_metrics': self.engine.get_performance_metrics(),
                'security_metrics': self.engine.security_manager.get_security_status(),
                'ai_metrics': self.engine.pattern_ai.get_pattern_metrics(),
            }
            
            # Save to file
            import json
            with open(file_path, 'w') as f:
                json.dump(metrics_data, f, indent=2, default=str)
            
            self.logger.info(f"Metrics exported to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting metrics: {e}")
            return False