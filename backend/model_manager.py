"""
Model Manager for downloading and caching Gemma 3n model from Hugging Face
"""
import os
import logging
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor, AutoModelForImageTextToText
from huggingface_hub import snapshot_download
from config import Settings

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model_path = None
        self.cache_dir = Path.home() / '.cache' / 'huggingface' / 'transformers'
        
    async def ensure_model_available(self) -> str:
        """
        Ensure the Gemma 3n model is available locally from Hugging Face
        
        Returns:
            str: Model identifier for Hugging Face
        """
        try:
            logger.info("📦 Checking for cached Gemma 3n model from Hugging Face...")
            
            # Set Hugging Face token if provided
            if self.settings.hf_token:
                os.environ['HUGGINGFACE_HUB_TOKEN'] = self.settings.hf_token
                logger.info("🔑 Hugging Face token configured")
            
            # Model identifier
            model_id = self.settings.hf_model_id
            
            # Check if model is already cached
            if self._is_model_cached(model_id):
                logger.info(f"✅ Found cached model: {model_id}")
                self.model_path = model_id
                return self.model_path
            
            # Download model if not cached
            logger.info(f"⬇️ Downloading Gemma 3n model from Hugging Face: {model_id}")
            logger.info("This may take a while depending on your internet connection...")
            
            # Download model files to cache
            snapshot_download(
                repo_id=model_id,
                cache_dir=self.cache_dir,
                token=self.settings.hf_token if self.settings.hf_token else None,
                resume_download=True
            )
            
            self.model_path = model_id
            logger.info(f"✅ Model downloaded and cached: {model_id}")
            
            return self.model_path
            
        except Exception as e:
            logger.error(f"❌ Failed to ensure model availability: {e}")
            if "authentication" in str(e).lower():
                logger.error("🔑 Please check your Hugging Face token in the .env file")
            elif "not found" in str(e).lower():
                logger.error("📦 Please ensure you have access to the Gemma model on Hugging Face")
            raise

    def _is_model_cached(self, model_id: str) -> bool:
        """Check if model is already cached locally"""
        try:
            # Try to load tokenizer to check if model is cached
            AutoTokenizer.from_pretrained(
                model_id,
                token=self.settings.hf_token if self.settings.hf_token else None,
                local_files_only=True
            )
            return True
        except:
            return False

    def get_model_path(self) -> str:
        """Get the current model identifier"""
        return self.model_path

    def is_model_available(self) -> bool:
        """Check if model is available"""
        return self.model_path is not None