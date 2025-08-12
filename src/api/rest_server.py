"""
REST API Server for Hassan Ultimate Anti-Recoil
FastAPI-based REST server for remote control and integration
"""

import asyncio
import logging
import uvicorn
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI, HTTPException, Depends, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    # Fallback for when FastAPI is not available
    FastAPI = None
    HTTPException = None
    FASTAPI_AVAILABLE = False


# API Models
class EngineStatus(BaseModel):
    """Engine status response model."""
    state: str
    current_game: Optional[str] = None
    current_weapon: Optional[str] = None
    performance_metrics: Dict[str, Any] = {}
    security_status: Dict[str, Any] = {}


class WeaponProfile(BaseModel):
    """Weapon profile model."""
    name: str
    display_name: str
    game: str
    weapon_class: str
    vertical_pattern: List[float]
    horizontal_pattern: List[float]
    timing_pattern: List[float]
    base_sensitivity: float = 1.0
    ads_sensitivity: float = 0.8


class ConfigUpdate(BaseModel):
    """Configuration update model."""
    key: str
    value: Any


class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class RestServer:
    """
    REST API server for Hassan Ultimate Anti-Recoil.
    
    Features:
    - Engine control and monitoring
    - Configuration management
    - Weapon profile management
    - Performance metrics
    - Security status
    - Plugin integration
    - WebSocket support for real-time updates
    """
    
    def __init__(self, engine, config_manager, port: int = 8080):
        self.engine = engine
        self.config_manager = config_manager
        self.port = port
        self.logger = logging.getLogger(__name__)
        
        # API server
        self.app: Optional[FastAPI] = None
        self.server_task: Optional[asyncio.Task] = None
        
        # Authentication
        self.security = HTTPBearer() if FASTAPI_AVAILABLE else None
        self.api_key = "hassan-ultimate-antirecoil-2024"  # In production, use proper key management
        
        # Initialize server
        if FASTAPI_AVAILABLE:
            self._create_app()
        else:
            self.logger.warning("FastAPI not available - REST API disabled")
        
        self.logger.info("REST API server initialized")
    
    def _create_app(self) -> None:
        """Create FastAPI application."""
        try:
            @asynccontextmanager
            async def lifespan(app: FastAPI):
                # Startup
                self.logger.info("REST API server starting...")
                yield
                # Shutdown
                self.logger.info("REST API server shutting down...")
            
            # Create FastAPI app
            self.app = FastAPI(
                title="Hassan Ultimate Anti-Recoil API",
                description="Professional anti-recoil control API",
                version="7.0.0",
                lifespan=lifespan
            )
            
            # CORS middleware
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],  # In production, restrict this
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Setup routes
            self._setup_routes()
            
        except Exception as e:
            self.logger.error(f"Error creating FastAPI app: {e}")
    
    def _verify_api_key(self, credentials: HTTPAuthorizationCredentials = Depends(None)) -> bool:
        """Verify API key authentication."""
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authentication credentials"
            )
        
        if credentials.credentials != self.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        return True
    
    def _setup_routes(self) -> None:
        """Setup API routes."""
        try:
            # Health check
            @self.app.get("/health")
            async def health_check():
                return {"status": "healthy", "service": "Hassan Ultimate Anti-Recoil API"}
            
            # Engine status
            @self.app.get("/api/v1/engine/status", response_model=EngineStatus)
            async def get_engine_status(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    current_game = None
                    if hasattr(self.engine, 'game_detector'):
                        game_info = self.engine.game_detector.get_current_game()
                        current_game = game_info.display_name if game_info else None
                    
                    return EngineStatus(
                        state=self.engine.state.value,
                        current_game=current_game,
                        current_weapon=getattr(self.engine, 'current_weapon', None),
                        performance_metrics=self.engine.get_performance_metrics(),
                        security_status=self.engine.security_manager.get_security_status()
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # Engine control
            @self.app.post("/api/v1/engine/start")
            async def start_engine(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    success = await self.engine.start()
                    return APIResponse(
                        success=success,
                        message="Engine started" if success else "Failed to start engine"
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/engine/stop")
            async def stop_engine(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    success = await self.engine.stop()
                    return APIResponse(
                        success=success,
                        message="Engine stopped" if success else "Failed to stop engine"
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/engine/pause")
            async def pause_engine(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    self.engine.pause()
                    return APIResponse(success=True, message="Engine paused")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/engine/resume")
            async def resume_engine(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    self.engine.resume()
                    return APIResponse(success=True, message="Engine resumed")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # Configuration management
            @self.app.get("/api/v1/config")
            async def get_config(key: Optional[str] = None, authenticated: bool = Depends(self._verify_api_key)):
                try:
                    if key:
                        value = self.config_manager.get(key)
                        return APIResponse(success=True, message="Configuration retrieved", data={key: value})
                    else:
                        # Return all configuration
                        return APIResponse(success=True, message="All configuration retrieved", data=self.config_manager.config)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/config")
            async def update_config(config_update: ConfigUpdate, authenticated: bool = Depends(self._verify_api_key)):
                try:
                    success = self.config_manager.set(config_update.key, config_update.value)
                    return APIResponse(
                        success=success,
                        message=f"Configuration updated: {config_update.key}" if success else "Failed to update configuration"
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # Weapon management
            @self.app.get("/api/v1/weapons")
            async def get_weapons(game: Optional[str] = None, authenticated: bool = Depends(self._verify_api_key)):
                try:
                    if hasattr(self.engine, 'weapon_loader'):
                        if game:
                            weapons = self.engine.weapon_loader.get_weapons_for_game(game)
                        else:
                            weapons = {}
                            for game_name in self.engine.weapon_loader.get_all_games():
                                weapons[game_name] = self.engine.weapon_loader.get_weapons_for_game(game_name)
                        
                        # Convert to serializable format
                        serializable_weapons = {}
                        for key, weapon_dict in weapons.items():
                            if isinstance(weapon_dict, dict):
                                serializable_weapons[key] = {
                                    name: {
                                        'name': w.name,
                                        'display_name': w.display_name,
                                        'weapon_class': w.weapon_class,
                                        'damage': w.damage,
                                        'fire_rate': w.fire_rate,
                                        'accuracy': w.accuracy,
                                        'range': w.range,
                                        'mobility': w.mobility,
                                        'control': w.control
                                    } for name, w in weapon_dict.items()
                                }
                        
                        return APIResponse(success=True, message="Weapons retrieved", data=serializable_weapons)
                    else:
                        return APIResponse(success=False, message="Weapon loader not available")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/weapons/select")
            async def select_weapon(game: str, weapon: str, authenticated: bool = Depends(self._verify_api_key)):
                try:
                    success = self.engine.set_weapon(weapon, game)
                    return APIResponse(
                        success=success,
                        message=f"Selected weapon: {weapon}" if success else "Failed to select weapon"
                    )
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # Game detection
            @self.app.get("/api/v1/games")
            async def get_games(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    if hasattr(self.engine, 'game_detector'):
                        games = self.engine.game_detector.get_supported_games()
                        serializable_games = {
                            name: {
                                'name': info.name,
                                'display_name': info.display_name,
                                'process_name': info.process_name,
                                'anti_cheat': info.anti_cheat,
                                'supported': info.supported
                            } for name, info in games.items()
                        }
                        return APIResponse(success=True, message="Games retrieved", data=serializable_games)
                    else:
                        return APIResponse(success=False, message="Game detector not available")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/games/select")
            async def select_game(game: str, authenticated: bool = Depends(self._verify_api_key)):
                try:
                    if hasattr(self.engine, 'game_detector'):
                        success = self.engine.game_detector.manually_set_game(game)
                        return APIResponse(
                            success=success,
                            message=f"Selected game: {game}" if success else "Failed to select game"
                        )
                    else:
                        return APIResponse(success=False, message="Game detector not available")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # Performance metrics
            @self.app.get("/api/v1/metrics")
            async def get_metrics(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    metrics = {
                        'engine': self.engine.get_performance_metrics(),
                        'security': self.engine.security_manager.get_security_status(),
                        'input': self.engine.input_handler.get_metrics() if hasattr(self.engine, 'input_handler') else {},
                        'ai': self.engine.pattern_ai.get_pattern_metrics() if hasattr(self.engine, 'pattern_ai') else {}
                    }
                    return APIResponse(success=True, message="Metrics retrieved", data=metrics)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # Security controls
            @self.app.post("/api/v1/security/level")
            async def set_security_level(level: str, authenticated: bool = Depends(self._verify_api_key)):
                try:
                    from src.core.security import SecurityLevel
                    if level.upper() in [l.name for l in SecurityLevel]:
                        security_level = SecurityLevel[level.upper()]
                        self.engine.security_manager.set_security_level(security_level)
                        return APIResponse(success=True, message=f"Security level set to {level}")
                    else:
                        return APIResponse(success=False, message="Invalid security level")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            # AI controls
            @self.app.post("/api/v1/ai/enable")
            async def enable_ai(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    if hasattr(self.engine, 'pattern_ai'):
                        self.engine.pattern_ai.enable_learning()
                        return APIResponse(success=True, message="AI learning enabled")
                    else:
                        return APIResponse(success=False, message="AI not available")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            @self.app.post("/api/v1/ai/disable")
            async def disable_ai(authenticated: bool = Depends(self._verify_api_key)):
                try:
                    if hasattr(self.engine, 'pattern_ai'):
                        self.engine.pattern_ai.disable_learning()
                        return APIResponse(success=True, message="AI learning disabled")
                    else:
                        return APIResponse(success=False, message="AI not available")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=str(e))
            
            self.logger.debug("API routes setup complete")
            
        except Exception as e:
            self.logger.error(f"Error setting up API routes: {e}")
    
    async def start(self) -> bool:
        """Start the REST API server."""
        try:
            if not FASTAPI_AVAILABLE or not self.app:
                self.logger.error("FastAPI not available - cannot start REST server")
                return False
            
            self.logger.info(f"Starting REST API server on port {self.port}")
            
            # Create server task
            config = uvicorn.Config(
                app=self.app,
                host="0.0.0.0",
                port=self.port,
                log_level="info",
                access_log=False
            )
            
            server = uvicorn.Server(config)
            self.server_task = asyncio.create_task(server.serve())
            
            self.logger.info(f"REST API server started on http://0.0.0.0:{self.port}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start REST API server: {e}")
            return False
    
    async def stop(self) -> bool:
        """Stop the REST API server."""
        try:
            if self.server_task:
                self.server_task.cancel()
                try:
                    await self.server_task
                except asyncio.CancelledError:
                    pass
                
                self.server_task = None
            
            self.logger.info("REST API server stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping REST API server: {e}")
            return False
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get API server information."""
        return {
            'available': FASTAPI_AVAILABLE,
            'port': self.port,
            'running': self.server_task is not None and not self.server_task.done(),
            'endpoints': [
                'GET /health',
                'GET /api/v1/engine/status',
                'POST /api/v1/engine/start',
                'POST /api/v1/engine/stop',
                'POST /api/v1/engine/pause',
                'POST /api/v1/engine/resume',
                'GET /api/v1/config',
                'POST /api/v1/config',
                'GET /api/v1/weapons',
                'POST /api/v1/weapons/select',
                'GET /api/v1/games',
                'POST /api/v1/games/select',
                'GET /api/v1/metrics',
                'POST /api/v1/security/level',
                'POST /api/v1/ai/enable',
                'POST /api/v1/ai/disable'
            ]
        }