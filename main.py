#!/usr/bin/env python3
"""
Hassan Ultimate Anti-Recoil v7.0 - Professional Edition
Main entry point for the application

Author: Hassan-3060
Date: 2025-08-12 22:44:35 UTC
Version: 7.0.0 Professional Edition
"""

import sys
import asyncio
import logging
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.engine import AntiRecoilEngine
from src.gui.main_window import MainWindow
from src.utils.logger import setup_logging
from src.data.config_manager import ConfigManager


def main():
    """Main application entry point."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Hassan Ultimate Anti-Recoil v7.0 Professional Edition")
        
        # Initialize configuration
        config_manager = ConfigManager()
        
        # Initialize core engine
        engine = AntiRecoilEngine(config_manager)
        
        # Start GUI application
        app = MainWindow(engine, config_manager)
        app.run()
        
    except Exception as e:
        logging.critical(f"Fatal error in main application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()