"""
Security Manager for Hassan Ultimate Anti-Recoil
Advanced security features and anti-cheat bypass capabilities
"""

import asyncio
import logging
import random
import time
import hashlib
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import psutil


class SecurityLevel(Enum):
    """Security operation levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"


@dataclass
class SecuritySettings:
    """Security configuration settings."""
    stealth_mode: bool = True
    randomization_level: float = 0.15
    anti_detection: bool = True
    process_hiding: bool = True
    memory_protection: bool = True
    movement_humanization: bool = True
    timing_randomization: bool = True
    signature_obfuscation: bool = True


class SecurityManager:
    """
    Advanced security manager for anti-cheat bypass and stealth operation.
    
    Features:
    - Movement humanization and randomization
    - Anti-detection mechanisms
    - Process hiding and obfuscation
    - Memory protection
    - Timing randomization
    - Signature obfuscation
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        
        # Security settings
        self.settings = SecuritySettings()
        self.security_level = SecurityLevel.HIGH
        
        # Randomization parameters
        self.movement_variance = 0.15  # 15% variance
        self.timing_variance = 0.1     # 10% timing variance
        self.pattern_variance = 0.2    # 20% pattern variance
        
        # Anti-detection state
        self.last_movement_time = 0.0
        self.movement_pattern_history = []
        self.detection_risk_score = 0.0
        
        # Process monitoring
        self.monitored_processes = set()
        self.suspicious_processes = {
            "cheatengine", "processhacker", "x64dbg", "ollydbg",
            "ida", "wireshark", "procmon", "autoruns"
        }
        
        # Security metrics
        self.security_metrics = {
            'randomizations_applied': 0,
            'detections_avoided': 0,
            'risk_score': 0.0,
            'stealth_operations': 0
        }
        
        self.logger.info("Security manager initialized")
    
    async def initialize(self) -> bool:
        """Initialize security systems."""
        try:
            self.logger.info("Initializing security systems...")
            
            # Start security monitoring
            asyncio.create_task(self._security_monitoring_loop())
            
            # Initialize obfuscation
            self._initialize_obfuscation()
            
            # Setup process monitoring
            self._setup_process_monitoring()
            
            self.logger.info("Security systems initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize security systems: {e}")
            return False
    
    async def cleanup(self) -> None:
        """Clean up security resources."""
        try:
            self.logger.info("Security systems cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up security systems: {e}")
    
    def _initialize_obfuscation(self) -> None:
        """Initialize signature obfuscation."""
        try:
            # Randomize internal timings
            random.seed(int(time.time()) % 1000)
            
            # Generate unique session identifier
            session_data = f"{time.time()}{os.getpid()}{random.random()}"
            self.session_id = hashlib.md5(session_data.encode()).hexdigest()[:8]
            
            self.logger.debug("Obfuscation initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing obfuscation: {e}")
    
    def _setup_process_monitoring(self) -> None:
        """Setup process monitoring for security threats."""
        try:
            # Get initial process list
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    self.monitored_processes.add(proc_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.logger.debug(f"Monitoring {len(self.monitored_processes)} processes")
            
        except Exception as e:
            self.logger.error(f"Error setting up process monitoring: {e}")
    
    async def _security_monitoring_loop(self) -> None:
        """Main security monitoring loop."""
        self.logger.debug("Security monitoring loop started")
        
        while True:
            try:
                # Check for suspicious processes
                await self._check_suspicious_processes()
                
                # Update detection risk score
                self._update_risk_score()
                
                # Perform security cleanup
                self._security_cleanup()
                
                # Sleep for monitoring interval
                await asyncio.sleep(5.0)
                
            except Exception as e:
                self.logger.error(f"Error in security monitoring: {e}")
                await asyncio.sleep(1.0)
    
    async def _check_suspicious_processes(self) -> None:
        """Check for suspicious processes that might indicate monitoring."""
        try:
            current_processes = set()
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    current_processes.add(proc_name)
                    
                    # Check if suspicious
                    for suspicious in self.suspicious_processes:
                        if suspicious in proc_name:
                            self.logger.warning(f"Suspicious process detected: {proc_name}")
                            self._handle_suspicious_process(proc_name)
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Update monitored processes
            self.monitored_processes = current_processes
            
        except Exception as e:
            self.logger.error(f"Error checking suspicious processes: {e}")
    
    def _handle_suspicious_process(self, process_name: str) -> None:
        """Handle detection of suspicious process."""
        try:
            # Increase detection risk
            self.detection_risk_score += 0.2
            
            # Activate maximum stealth mode
            if self.detection_risk_score > 0.5:
                self.security_level = SecurityLevel.MAXIMUM
                self.settings.stealth_mode = True
                self.settings.randomization_level = min(0.5, self.settings.randomization_level * 1.5)
                
                self.logger.warning("Activated maximum stealth mode due to suspicious activity")
            
            self.security_metrics['detections_avoided'] += 1
            
        except Exception as e:
            self.logger.error(f"Error handling suspicious process: {e}")
    
    def _update_risk_score(self) -> None:
        """Update overall detection risk score."""
        try:
            # Decay risk score over time
            current_time = time.time()
            time_factor = min(1.0, (current_time - self.last_movement_time) / 300.0)  # 5 minutes
            self.detection_risk_score *= (1.0 - time_factor * 0.1)
            
            # Ensure bounds
            self.detection_risk_score = max(0.0, min(1.0, self.detection_risk_score))
            
            # Update metrics
            self.security_metrics['risk_score'] = self.detection_risk_score
            
        except Exception as e:
            self.logger.error(f"Error updating risk score: {e}")
    
    def _security_cleanup(self) -> None:
        """Perform periodic security cleanup."""
        try:
            # Limit movement history size
            if len(self.movement_pattern_history) > 1000:
                self.movement_pattern_history = self.movement_pattern_history[-500:]
            
            # Reset risk score if very low
            if self.detection_risk_score < 0.01:
                self.detection_risk_score = 0.0
            
        except Exception as e:
            self.logger.error(f"Error in security cleanup: {e}")
    
    def randomize_movement(self, x_delta: float, y_delta: float) -> Tuple[float, float]:
        """Apply security randomization to mouse movements."""
        try:
            if not self.settings.movement_humanization:
                return x_delta, y_delta
            
            current_time = time.time()
            
            # Calculate randomization level based on security level
            if self.security_level == SecurityLevel.MAXIMUM:
                randomization = self.settings.randomization_level * 2.0
            elif self.security_level == SecurityLevel.HIGH:
                randomization = self.settings.randomization_level * 1.5
            elif self.security_level == SecurityLevel.MEDIUM:
                randomization = self.settings.randomization_level
            else:
                randomization = self.settings.randomization_level * 0.5
            
            # Apply randomization
            x_variance = random.uniform(-randomization, randomization)
            y_variance = random.uniform(-randomization, randomization)
            
            # Add subtle human-like micro-movements
            micro_x = random.uniform(-0.1, 0.1)
            micro_y = random.uniform(-0.1, 0.1)
            
            # Apply timing-based randomization
            time_factor = 1.0
            if self.settings.timing_randomization:
                if current_time - self.last_movement_time < 0.05:  # Very fast movements
                    time_factor = random.uniform(0.8, 1.2)
            
            # Calculate final movement
            final_x = (x_delta + x_delta * x_variance + micro_x) * time_factor
            final_y = (y_delta + y_delta * y_variance + micro_y) * time_factor
            
            # Add to movement history for pattern analysis
            self.movement_pattern_history.append({
                'timestamp': current_time,
                'original': (x_delta, y_delta),
                'randomized': (final_x, final_y),
                'variance': (x_variance, y_variance)
            })
            
            # Update metrics
            self.security_metrics['randomizations_applied'] += 1
            self.last_movement_time = current_time
            
            return final_x, final_y
            
        except Exception as e:
            self.logger.error(f"Error randomizing movement: {e}")
            return x_delta, y_delta
    
    def randomize_timing(self, base_delay: float) -> float:
        """Apply timing randomization to delays."""
        try:
            if not self.settings.timing_randomization:
                return base_delay
            
            # Apply randomization based on security level
            variance = self.timing_variance
            if self.security_level == SecurityLevel.MAXIMUM:
                variance *= 2.0
            elif self.security_level == SecurityLevel.HIGH:
                variance *= 1.5
            
            # Random timing adjustment
            adjustment = random.uniform(-variance, variance)
            randomized_delay = base_delay * (1.0 + adjustment)
            
            # Ensure minimum delay
            return max(0.001, randomized_delay)
            
        except Exception as e:
            self.logger.error(f"Error randomizing timing: {e}")
            return base_delay
    
    def should_apply_compensation(self) -> bool:
        """Determine if compensation should be applied based on security analysis."""
        try:
            # Always apply if stealth mode is disabled
            if not self.settings.stealth_mode:
                return True
            
            # Calculate probability based on risk score
            base_probability = 0.95  # 95% base chance
            risk_reduction = self.detection_risk_score * 0.3  # Up to 30% reduction
            
            probability = base_probability - risk_reduction
            
            # Random decision
            should_apply = random.random() < probability
            
            if not should_apply:
                self.security_metrics['stealth_operations'] += 1
            
            return should_apply
            
        except Exception as e:
            self.logger.error(f"Error determining compensation application: {e}")
            return True
    
    def analyze_movement_pattern(self) -> Dict[str, float]:
        """Analyze movement patterns for detection risk."""
        try:
            if len(self.movement_pattern_history) < 10:
                return {'risk': 0.0, 'regularity': 0.0, 'humanness': 1.0}
            
            recent_movements = self.movement_pattern_history[-50:]  # Last 50 movements
            
            # Calculate movement regularity (lower is better)
            x_movements = [m['randomized'][0] for m in recent_movements]
            y_movements = [m['randomized'][1] for m in recent_movements]
            
            x_variance = np.var(x_movements) if x_movements else 0
            y_variance = np.var(y_movements) if y_movements else 0
            
            # Calculate timing regularity
            timestamps = [m['timestamp'] for m in recent_movements]
            time_deltas = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
            timing_variance = np.var(time_deltas) if len(time_deltas) > 1 else 0
            
            # Calculate risk metrics
            regularity_risk = 1.0 / (1.0 + x_variance + y_variance)  # High variance = low risk
            timing_risk = 1.0 / (1.0 + timing_variance * 1000)       # High timing variance = low risk
            
            overall_risk = (regularity_risk + timing_risk) / 2.0
            humanness_score = 1.0 - overall_risk
            
            return {
                'risk': overall_risk,
                'regularity': regularity_risk,
                'timing_risk': timing_risk,
                'humanness': humanness_score
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing movement pattern: {e}")
            return {'risk': 0.0, 'regularity': 0.0, 'humanness': 1.0}
    
    # Public API methods
    
    def perform_checks(self) -> None:
        """Perform security checks (called periodically by engine)."""
        try:
            # Update detection risk based on movement patterns
            pattern_analysis = self.analyze_movement_pattern()
            self.detection_risk_score = max(self.detection_risk_score, pattern_analysis['risk'] * 0.5)
            
            # Adjust security level based on risk
            if self.detection_risk_score > 0.8:
                self.security_level = SecurityLevel.MAXIMUM
            elif self.detection_risk_score > 0.6:
                self.security_level = SecurityLevel.HIGH
            elif self.detection_risk_score > 0.3:
                self.security_level = SecurityLevel.MEDIUM
            else:
                self.security_level = SecurityLevel.LOW
            
        except Exception as e:
            self.logger.error(f"Error performing security checks: {e}")
    
    def set_setting(self, setting: str, value: Any) -> bool:
        """Set a security setting."""
        try:
            if hasattr(self.settings, setting):
                setattr(self.settings, setting, value)
                self.logger.info(f"Security setting {setting} set to {value}")
                return True
            else:
                self.logger.error(f"Unknown security setting: {setting}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error setting security setting: {e}")
            return False
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status and metrics."""
        try:
            pattern_analysis = self.analyze_movement_pattern()
            
            return {
                'security_level': self.security_level.value,
                'stealth_mode': self.settings.stealth_mode,
                'detection_risk_score': self.detection_risk_score,
                'randomization_level': self.settings.randomization_level,
                'movement_humanness': pattern_analysis.get('humanness', 0.0),
                'suspicious_processes': len([p for p in self.monitored_processes 
                                           if any(s in p for s in self.suspicious_processes)]),
                'metrics': self.security_metrics.copy()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting security status: {e}")
            return {}
    
    def set_security_level(self, level: SecurityLevel) -> None:
        """Set security operation level."""
        self.security_level = level
        
        # Adjust settings based on level
        if level == SecurityLevel.MAXIMUM:
            self.settings.randomization_level = 0.5
            self.settings.stealth_mode = True
            self.settings.anti_detection = True
        elif level == SecurityLevel.HIGH:
            self.settings.randomization_level = 0.3
            self.settings.stealth_mode = True
            self.settings.anti_detection = True
        elif level == SecurityLevel.MEDIUM:
            self.settings.randomization_level = 0.15
            self.settings.stealth_mode = True
            self.settings.anti_detection = True
        else:  # LOW
            self.settings.randomization_level = 0.05
            self.settings.stealth_mode = False
            self.settings.anti_detection = False
        
        self.logger.info(f"Security level set to {level.value}")
    
    def reset_to_defaults(self) -> None:
        """Reset security settings to defaults."""
        self.settings = SecuritySettings()
        self.security_level = SecurityLevel.HIGH
        self.detection_risk_score = 0.0
        self.movement_pattern_history.clear()
        self.logger.info("Security settings reset to defaults")
    
    def enable_stealth_mode(self) -> None:
        """Enable stealth mode."""
        self.settings.stealth_mode = True
        self.logger.info("Stealth mode enabled")
    
    def disable_stealth_mode(self) -> None:
        """Disable stealth mode."""
        self.settings.stealth_mode = False
        self.logger.info("Stealth mode disabled")