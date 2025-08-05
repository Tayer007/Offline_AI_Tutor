"""
Configuration management for Offline AI Tutor using Hugging Face
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Hugging Face settings
    hf_token: str = ""
    hf_model_id: str = "google/gemma-3n-e2b-it"
    
    # Server settings
    backend_port: int = 8000
    frontend_port: int = 3000
    
    # Model generation settings
    max_new_tokens: int = 512
    temperature: float = 0.7
    do_sample: bool = True
    
    # Cache settings
    model_cache_dir: str = "./models_cache"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Try to load from different locations
        env_locations = [
            Path(__file__).parent / ".env",  # Same directory as config.py
            Path.cwd() / ".env",             # Current working directory
            Path(__file__).parent.parent / ".env"  # Parent directory
        ]
        
        for env_path in env_locations:
            if env_path.exists():
                print(f"Found .env file at: {env_path}")
                # Manually load the .env file
                self._load_env_file(env_path)
                break
        else:
            print("Warning: No .env file found. Checking environment variables...")
            
        # Fallback to environment variables
        if not self.hf_token:
            self.hf_token = os.getenv('HF_TOKEN', '')
            
        if not self.hf_token:
            self.hf_token = os.getenv('HUGGINGFACE_HUB_TOKEN', '')
            
        print(f"HF Token configured: {'Yes' if self.hf_token and len(self.hf_token) > 10 else 'No'}")
    
    def _load_env_file(self, env_path: Path):
        """Manually load environment variables from .env file"""
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        if key == 'HF_TOKEN':
                            self.hf_token = value
                        elif key == 'HF_MODEL_ID':
                            self.hf_model_id = value
                        elif key == 'BACKEND_PORT':
                            self.backend_port = int(value)
                        elif key == 'FRONTEND_PORT':
                            self.frontend_port = int(value)
                        elif key == 'MAX_NEW_TOKENS':
                            self.max_new_tokens = int(value)
                        elif key == 'TEMPERATURE':
                            self.temperature = float(value)
                        elif key == 'MODEL_CACHE_DIR':
                            self.model_cache_dir = value
                            
        except Exception as e:
            print(f"Error loading .env file: {e}")

@lru_cache()
def get_settings():
    return Settings()