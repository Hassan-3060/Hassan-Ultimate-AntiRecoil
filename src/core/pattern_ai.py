"""
AI-Powered Pattern Recognition for Hassan Ultimate Anti-Recoil
Advanced machine learning for adaptive recoil pattern recognition and compensation
"""

import asyncio
import logging
import numpy as np
import pickle
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import time

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
    import joblib
except ImportError:
    # Fallback for minimal functionality
    RandomForestRegressor = None
    StandardScaler = None
    train_test_split = None
    mean_squared_error = None
    joblib = None


@dataclass
class ShotData:
    """Represents data from a single shot."""
    timestamp: float
    weapon: str
    game: str
    shot_number: int
    mouse_movement: Tuple[float, float]
    expected_recoil: Tuple[float, float]
    applied_compensation: Tuple[float, float]
    accuracy_score: float
    player_input: Tuple[float, float]


@dataclass
class PatternMetrics:
    """Metrics for pattern recognition performance."""
    accuracy: float
    confidence: float
    adaptation_rate: float
    prediction_error: float
    samples_collected: int
    last_updated: float


class PatternAI:
    """
    AI-powered pattern recognition and adaptation system.
    
    Features:
    - Real-time pattern learning and adaptation
    - Multi-weapon pattern recognition
    - Player behavior analysis
    - Predictive recoil compensation
    - Continuous model improvement
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        
        # AI Models
        self.recoil_model: Optional[RandomForestRegressor] = None
        self.scaler: Optional[StandardScaler] = None
        
        # Training data
        self.shot_history: List[ShotData] = []
        self.max_history_size = 10000
        
        # Pattern cache
        self.learned_patterns: Dict[str, Dict] = {}
        self.pattern_metrics: Dict[str, PatternMetrics] = {}
        
        # Configuration
        self.learning_enabled = True
        self.adaptation_rate = 0.1
        self.confidence_threshold = 0.7
        self.min_samples_for_learning = 50
        
        # Model paths
        self.model_dir = Path("data/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Pattern AI initialized")
    
    async def initialize(self) -> bool:
        """Initialize the AI system."""
        try:
            self.logger.info("Initializing Pattern AI...")
            
            # Check if ML libraries are available
            if not RandomForestRegressor:
                self.logger.warning("scikit-learn not available - AI features limited")
                return True
            
            # Load existing models
            await self._load_models()
            
            # Load historical data
            await self._load_training_data()
            
            # Initialize base models if needed
            if not self.recoil_model:
                await self._initialize_base_model()
            
            self.logger.info("Pattern AI initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Pattern AI: {e}")
            return False
    
    async def cleanup(self) -> None:
        """Clean up AI resources."""
        try:
            # Save models and data
            await self._save_models()
            await self._save_training_data()
            
            self.logger.info("Pattern AI cleaned up")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up Pattern AI: {e}")
    
    async def _load_models(self) -> None:
        """Load pre-trained models."""
        try:
            model_file = self.model_dir / "recoil_model.joblib"
            scaler_file = self.model_dir / "scaler.joblib"
            
            if model_file.exists() and joblib:
                self.recoil_model = joblib.load(model_file)
                self.logger.info("Loaded recoil prediction model")
            
            if scaler_file.exists() and joblib:
                self.scaler = joblib.load(scaler_file)
                self.logger.info("Loaded feature scaler")
            
            # Load pattern cache
            patterns_file = self.model_dir / "learned_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    self.learned_patterns = json.load(f)
                self.logger.info(f"Loaded {len(self.learned_patterns)} learned patterns")
            
        except Exception as e:
            self.logger.error(f"Error loading models: {e}")
    
    async def _save_models(self) -> None:
        """Save trained models."""
        try:
            if self.recoil_model and joblib:
                model_file = self.model_dir / "recoil_model.joblib"
                joblib.dump(self.recoil_model, model_file)
                self.logger.debug("Saved recoil prediction model")
            
            if self.scaler and joblib:
                scaler_file = self.model_dir / "scaler.joblib"
                joblib.dump(self.scaler, scaler_file)
                self.logger.debug("Saved feature scaler")
            
            # Save pattern cache
            patterns_file = self.model_dir / "learned_patterns.json"
            with open(patterns_file, 'w') as f:
                json.dump(self.learned_patterns, f, indent=2)
            self.logger.debug("Saved learned patterns")
            
        except Exception as e:
            self.logger.error(f"Error saving models: {e}")
    
    async def _load_training_data(self) -> None:
        """Load historical training data."""
        try:
            data_file = self.model_dir / "shot_history.pkl"
            
            if data_file.exists():
                with open(data_file, 'rb') as f:
                    self.shot_history = pickle.load(f)
                
                # Limit history size
                if len(self.shot_history) > self.max_history_size:
                    self.shot_history = self.shot_history[-self.max_history_size:]
                
                self.logger.info(f"Loaded {len(self.shot_history)} historical shots")
            
        except Exception as e:
            self.logger.error(f"Error loading training data: {e}")
    
    async def _save_training_data(self) -> None:
        """Save training data."""
        try:
            data_file = self.model_dir / "shot_history.pkl"
            
            with open(data_file, 'wb') as f:
                pickle.dump(self.shot_history, f)
            
            self.logger.debug(f"Saved {len(self.shot_history)} shots to training data")
            
        except Exception as e:
            self.logger.error(f"Error saving training data: {e}")
    
    async def _initialize_base_model(self) -> None:
        """Initialize base AI model."""
        try:
            if not RandomForestRegressor:
                return
            
            # Create base model
            self.recoil_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1
            )
            
            # Create scaler
            self.scaler = StandardScaler()
            
            # If we have enough historical data, train immediately
            if len(self.shot_history) >= self.min_samples_for_learning:
                await self._retrain_model()
            
            self.logger.info("Initialized base AI model")
            
        except Exception as e:
            self.logger.error(f"Error initializing base model: {e}")
    
    def record_shot(self, shot_data: ShotData) -> None:
        """Record a shot for learning purposes."""
        try:
            if not self.learning_enabled:
                return
            
            # Add to history
            self.shot_history.append(shot_data)
            
            # Limit history size
            if len(self.shot_history) > self.max_history_size:
                self.shot_history.pop(0)
            
            # Update pattern cache
            self._update_pattern_cache(shot_data)
            
            # Trigger retraining if we have enough new samples
            if len(self.shot_history) % 100 == 0:  # Retrain every 100 shots
                asyncio.create_task(self._retrain_model())
            
        except Exception as e:
            self.logger.error(f"Error recording shot: {e}")
    
    def _update_pattern_cache(self, shot_data: ShotData) -> None:
        """Update cached patterns with new shot data."""
        try:
            pattern_key = f"{shot_data.game}_{shot_data.weapon}"
            
            if pattern_key not in self.learned_patterns:
                self.learned_patterns[pattern_key] = {
                    'shots': [],
                    'average_recoil': [0.0, 0.0],
                    'pattern_confidence': 0.0,
                    'last_updated': time.time()
                }
            
            pattern = self.learned_patterns[pattern_key]
            
            # Add shot data
            pattern['shots'].append({
                'shot_number': shot_data.shot_number,
                'expected_recoil': shot_data.expected_recoil,
                'actual_movement': shot_data.mouse_movement,
                'accuracy': shot_data.accuracy_score
            })
            
            # Limit stored shots
            if len(pattern['shots']) > 500:
                pattern['shots'] = pattern['shots'][-500:]
            
            # Update average recoil
            if pattern['shots']:
                avg_x = np.mean([s['expected_recoil'][0] for s in pattern['shots']])
                avg_y = np.mean([s['expected_recoil'][1] for s in pattern['shots']])
                pattern['average_recoil'] = [float(avg_x), float(avg_y)]
            
            # Update confidence based on consistency
            if len(pattern['shots']) >= 10:
                recoil_variance = np.var([s['expected_recoil'] for s in pattern['shots'][-50:]])
                pattern['pattern_confidence'] = max(0.0, min(1.0, 1.0 - recoil_variance))
            
            pattern['last_updated'] = time.time()
            
        except Exception as e:
            self.logger.error(f"Error updating pattern cache: {e}")
    
    async def _retrain_model(self) -> None:
        """Retrain the AI model with new data."""
        try:
            if not self.recoil_model or not self.scaler or len(self.shot_history) < self.min_samples_for_learning:
                return
            
            self.logger.info("Retraining AI model...")
            
            # Prepare training data
            features, targets = self._prepare_training_data()
            
            if len(features) < self.min_samples_for_learning:
                self.logger.warning("Not enough training data for retraining")
                return
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                features, targets, test_size=0.2, random_state=42
            )
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.recoil_model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.recoil_model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            
            self.logger.info(f"Model retrained - MSE: {mse:.4f}")
            
            # Save updated models
            await self._save_models()
            
        except Exception as e:
            self.logger.error(f"Error retraining model: {e}")
    
    def _prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data from shot history."""
        features = []
        targets = []
        
        try:
            for shot in self.shot_history:
                # Feature vector: [shot_number, weapon_hash, game_hash, 
                #                 mouse_movement_x, mouse_movement_y,
                #                 player_input_x, player_input_y]
                feature = [
                    shot.shot_number,
                    hash(shot.weapon) % 1000,  # Simple hash for categorical
                    hash(shot.game) % 1000,
                    shot.mouse_movement[0],
                    shot.mouse_movement[1],
                    shot.player_input[0],
                    shot.player_input[1]
                ]
                
                # Target: expected recoil compensation
                target = [shot.expected_recoil[0], shot.expected_recoil[1]]
                
                features.append(feature)
                targets.append(target)
            
            return np.array(features), np.array(targets)
            
        except Exception as e:
            self.logger.error(f"Error preparing training data: {e}")
            return np.array([]), np.array([])
    
    def get_adaptive_adjustment(self, pattern, shot_index: int) -> Optional[Tuple[float, float]]:
        """Get AI-powered adaptive adjustment for recoil compensation."""
        try:
            if not self.recoil_model or not self.scaler:
                return None
            
            # Prepare input features
            features = np.array([[
                shot_index,
                hash(pattern.weapon_name) % 1000,
                hash(pattern.game) % 1000,
                0.0,  # No mouse movement yet
                0.0,
                0.0,  # No player input yet
                0.0
            ]])
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict adjustment
            prediction = self.recoil_model.predict(features_scaled)[0]
            
            # Apply adaptation rate
            adjustment = (
                prediction[0] * self.adaptation_rate,
                prediction[1] * self.adaptation_rate
            )
            
            return adjustment
            
        except Exception as e:
            self.logger.error(f"Error getting adaptive adjustment: {e}")
            return None
    
    def analyze_pattern(self, weapon: str, game: str) -> Optional[Dict[str, Any]]:
        """Analyze learned pattern for a specific weapon/game combination."""
        try:
            pattern_key = f"{game}_{weapon}"
            
            if pattern_key not in self.learned_patterns:
                return None
            
            pattern = self.learned_patterns[pattern_key]
            
            if not pattern['shots']:
                return None
            
            # Calculate statistics
            shots = pattern['shots']
            accuracies = [s['accuracy'] for s in shots]
            
            analysis = {
                'weapon': weapon,
                'game': game,
                'total_shots': len(shots),
                'average_accuracy': np.mean(accuracies),
                'accuracy_std': np.std(accuracies),
                'pattern_confidence': pattern['pattern_confidence'],
                'average_recoil': pattern['average_recoil'],
                'last_updated': pattern['last_updated'],
                'learning_progress': min(1.0, len(shots) / 200.0)  # Progress to 200 shots
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing pattern: {e}")
            return None
    
    def predict_recoil_pattern(self, weapon: str, game: str, shot_count: int) -> Optional[List[Tuple[float, float]]]:
        """Predict recoil pattern for a weapon based on learned data."""
        try:
            if not self.recoil_model or not self.scaler:
                return None
            
            pattern = []
            
            for i in range(shot_count):
                features = np.array([[
                    i,
                    hash(weapon) % 1000,
                    hash(game) % 1000,
                    0.0, 0.0, 0.0, 0.0
                ]])
                
                features_scaled = self.scaler.transform(features)
                prediction = self.recoil_model.predict(features_scaled)[0]
                
                pattern.append((float(prediction[0]), float(prediction[1])))
            
            return pattern
            
        except Exception as e:
            self.logger.error(f"Error predicting recoil pattern: {e}")
            return None
    
    def update(self) -> None:
        """Update AI system (called periodically)."""
        try:
            # Periodic cleanup and optimization
            current_time = time.time()
            
            # Clean old patterns
            for pattern_key in list(self.learned_patterns.keys()):
                pattern = self.learned_patterns[pattern_key]
                if current_time - pattern['last_updated'] > 86400 * 7:  # 7 days
                    del self.learned_patterns[pattern_key]
            
        except Exception as e:
            self.logger.error(f"Error in AI update: {e}")
    
    # Public API methods
    
    def get_pattern_metrics(self) -> Dict[str, Any]:
        """Get AI pattern recognition metrics."""
        try:
            total_patterns = len(self.learned_patterns)
            total_shots = sum(len(p['shots']) for p in self.learned_patterns.values())
            
            if total_patterns > 0:
                avg_confidence = np.mean([p['pattern_confidence'] for p in self.learned_patterns.values()])
            else:
                avg_confidence = 0.0
            
            return {
                'total_patterns_learned': total_patterns,
                'total_shots_recorded': total_shots,
                'average_pattern_confidence': avg_confidence,
                'learning_enabled': self.learning_enabled,
                'model_trained': self.recoil_model is not None,
                'adaptation_rate': self.adaptation_rate
            }
            
        except Exception as e:
            self.logger.error(f"Error getting pattern metrics: {e}")
            return {}
    
    def enable_learning(self) -> None:
        """Enable AI learning."""
        self.learning_enabled = True
        self.logger.info("AI learning enabled")
    
    def disable_learning(self) -> None:
        """Disable AI learning."""
        self.learning_enabled = False
        self.logger.info("AI learning disabled")
    
    def set_adaptation_rate(self, rate: float) -> None:
        """Set AI adaptation rate."""
        self.adaptation_rate = max(0.0, min(1.0, rate))
        self.logger.info(f"AI adaptation rate set to {self.adaptation_rate}")
    
    def reset_learning_data(self) -> None:
        """Reset all learning data."""
        self.shot_history.clear()
        self.learned_patterns.clear()
        self.pattern_metrics.clear()
        self.logger.info("AI learning data reset")