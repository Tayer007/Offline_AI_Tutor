"""
Image Analysis functions using Hugging Face transformers 4.53.2 - GPU ONLY
"""
import torch
from transformers import AutoProcessor, AutoModelForImageTextToText
from typing import Optional
import logging
import base64
import io
from PIL import Image
import requests

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    def __init__(self, model_id: str, hf_token: Optional[str] = None):
        self.model_id = model_id
        self.hf_token = hf_token
        self.processor = None
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"  # Prefer GPU for images
        
    def initialize(self):
        """Initialize the image analyzer with vision model from Hugging Face - GPU PREFERRED"""
        try:
            logger.info(f"🖼️ Loading Image Analysis model from Hugging Face: {self.model_id}")
            
            if torch.cuda.is_available():
                logger.info("🚀 FORCING GPU for image processing")
            else:
                logger.warning("⚠️ GPU not available, falling back to CPU for images")
            
            # Set token for authenticated access
            token = self.hf_token if self.hf_token else None
            
            # Load processor
            logger.info("🔧 Loading processor...")
            self.processor = AutoProcessor.from_pretrained(
                self.model_id,
                token=token,
                trust_remote_code=True
            )
            
            # Only load model if not already shared from text model
            if self.model is None:
                logger.info("👁️ Loading vision model on GPU...")
                self.model = AutoModelForImageTextToText.from_pretrained(
                    self.model_id,
                    token=token,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
                
                # Force model to GPU if available
                if torch.cuda.is_available():
                    self.model = self.model.to("cuda")
                    
                self.model.eval()
            else:
                logger.info("✅ Using shared model instance")
                # If using shared model, move it to GPU for image processing
                if torch.cuda.is_available() and self.model.device.type == "cpu":
                    logger.info("📤 Moving shared model to GPU for image processing...")
                    self.model = self.model.to("cuda")
            
            logger.info(f"📍 Image model loaded on device: {self.model.device}")
            logger.info("✅ Image Analyzer initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Image Analyzer: {e}")
            if "authentication" in str(e).lower():
                logger.error("🔑 Authentication failed. Please check your Hugging Face token.")
            raise

    def ask_image_question(self, image_url: str, question: str) -> str:
        """
        Analyze an image and answer a question about it using the vision model - GPU PREFERRED
        """
        if not self.model or not self.processor:
            raise RuntimeError("Image Analyzer not initialized. Call initialize() first.")
        
        try:
            # Handle different image input types
            image = self._load_image(image_url)
            
            # Create messages with image and text
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": question}
                    ]
                }
            ]

            # Process with the vision model
            inputs = self.processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt"
            )
            
            # Move inputs to the same device as model
            device = self.model.device
            inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}
            
            logger.info(f"🖼️ Processing image on {device}")
            
            input_len = inputs["input_ids"].shape[-1]

            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_new_tokens=512, 
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )
                
            # Decode response
            text = self.processor.batch_decode(
                outputs[:, input_len:],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )

            logger.info(f"🔍 Generated image analysis response on {device}")
            
            return text[0]
    
        except Exception as e:
            logger.error(f"❌ Error analyzing image: {e}")
            return f"❌ Error analyzing image: {str(e)}"

    def _load_image(self, image_input: str) -> Image.Image:
        """Load image from URL, file path, or base64 data"""
        try:
            # Check if it's base64 data
            if image_input.startswith('data:image'):
                # Extract base64 data
                base64_data = image_input.split(',')[1]
                image_data = base64.b64decode(base64_data)
                return Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Check if it's a URL
            elif image_input.startswith(('http://', 'https://')):
                response = requests.get(image_input, timeout=10)
                response.raise_for_status()
                return Image.open(io.BytesIO(response.content)).convert('RGB')
            
            # Assume it's a file path
            else:
                return Image.open(image_input).convert('RGB')
                
        except Exception as e:
            logger.error(f"❌ Failed to load image: {e}")
            raise ValueError(f"Could not load image from: {image_input}")

    async def ask_image_question_stream(self, image_url: str, question: str):
        """Streaming version of image analysis"""
        try:
            result = self.ask_image_question(image_url, question)
            
            # Simulate streaming by yielding chunks
            words = result.split()
            current_chunk = ""
            
            for i, word in enumerate(words):
                current_chunk += word + " "
                
                # Yield chunks every few words
                if (i + 1) % 5 == 0 or i == len(words) - 1:
                    yield current_chunk.strip()
                    current_chunk = ""
                    
        except Exception as e:
            yield f"❌ Error analyzing image: {str(e)}"