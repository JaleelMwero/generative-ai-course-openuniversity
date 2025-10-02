# config/core_config.py
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """Intelligent configuration manager with auto-detection"""
    
    def __init__(self):
        self.config_path = Path("config/aml_config.json")
        self.default_config = {
            "ai": {
                "provider": "auto",  # auto, openai, local, hybrid
                "api_key": None,
                "model": "gpt-4",
                "enable_learning": True,
                "confidence_threshold": 0.7
            },
            "banking": {
                "simulation_mode": True,
                "core_system": "auto",  # auto, temenos, flexcube, finacle, custom
                "integration_type": "api",  # api, message_queue, file_based
                "auto_detect_changes": True
            },
            "risk": {
                "ctr_threshold": 10000,
                "suspicious_threshold": 8000,
                "high_risk_score": 70,
                "adaptive_thresholds": True
            },
            "learning": {
                "enable_adaptive_learning": True,
                "model_retraining_days": 7,
                "pattern_memory_size": 1000,
                "feedback_loop": True
            }
        }
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = {**self.default_config, **json.load(f)}
        else:
            self.config = self.default_config
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        self.config_path.parent.mkdir(exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def auto_detect_environment(self):
        """Auto-detect banking environment and AI capabilities"""
        # Detect AI providers
        ai_providers = self._detect_ai_providers()
        
        # Detect banking systems
        banking_systems = self._detect_banking_systems()
        
        # Update config based on detection
        if ai_providers:
            self.config['ai']['provider'] = ai_providers[0]  # Use best available
        else:
            self.config['ai']['provider'] = 'local'
        
        if banking_systems:
            self.config['banking']['core_system'] = banking_systems[0]
            self.config['banking']['simulation_mode'] = False
        else:
            self.config['banking']['simulation_mode'] = True
        
        self.save_config()
        return self.config
    
    def _detect_ai_providers(self) -> list:
        """Detect available AI providers"""
        providers = []
        
        # Check OpenAI
        if os.getenv('OPENAI_API_KEY'):
            providers.append('openai')
        
        # Check local models (placeholder for local LLM detection)
        if self._check_local_models():
            providers.append('local')
        
        # Check hybrid capability
        if len(providers) > 1:
            providers.append('hybrid')
        
        return providers
    
    def _detect_banking_systems(self) -> list:
        """Detect banking core systems"""
        systems = []
        
        # Check environment variables for banking systems
        banking_indicators = [
            'T24_HOME', 'FLEXCUBE_HOME', 'FINACLE_PATH',
            'CORE_BANKING_SYSTEM', 'BANKING_API_URL'
        ]
        
        for indicator in banking_indicators:
            if os.getenv(indicator):
                system_name = indicator.lower().replace('_home', '').replace('_path', '').replace('_url', '')
                systems.append(system_name)
        
        # Check for API endpoints
        if os.getenv('BANKING_API_URL'):
            systems.append('api_custom')
        
        return systems
    
    def _check_local_models(self) -> bool:
        """Check if local models are available"""
        # Placeholder for local model detection
        # This could check for Ollama, LocalAI, etc.
        return False  # Default to False for now
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration with auto-fallback"""
        provider = self.config['ai']['provider']
        
        if provider == 'auto':
            providers = self._detect_ai_providers()
            if providers:
                provider = providers[0]
            else:
                provider = 'local'
        
        return {
            'provider': provider,
            'api_key': self.config['ai']['api_key'] or os.getenv('OPENAI_API_KEY'),
            'model': self.config['ai']['model'],
            'enable_learning': self.config['ai']['enable_learning']
        }

# Global config instance
config_manager = ConfigManager()
