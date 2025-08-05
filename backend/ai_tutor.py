"""
AI Tutor using the cached Gemma3n E2B-it model
"""
import os
import torch
from transformers import AutoProcessor, Gemma3nForConditionalGeneration
from PIL import Image
import requests
import logging
import time
import io
import base64

# Fix Unicode encoding issues
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['HF_HUB_USER_AGENT'] = 'transformers/4.53.0; python/3.12'

logger = logging.getLogger(__name__)

class AITutor:
    def __init__(self, model_id: str, hf_token: str):
        # Use the cached E2B model instead of E4B
        self.model_id = "google/gemma-3n-e2b-it"  # This one is already cached!
        self.hf_token = hf_token
        self.model = None
        self.processor = None
        
        # Check GPU availability
        if not torch.cuda.is_available():
            logger.warning("⚠️ CUDA not available, will use CPU")
            self.device = "cpu"
        else:
            self.device = "cuda"
            logger.info(f"🎮 GPU available: {torch.cuda.get_device_name()}")
        
    def initialize(self):
        """Initialize with cached Gemma3n E2B-it model"""
        try:
            logger.info(f"🚀 Loading cached Gemma3n E2B-it: {self.model_id}")
            if torch.cuda.is_available():
                logger.info(f"🔥 GPU: {torch.cuda.get_device_name()}")
                logger.info(f"🎮 CUDA Version: {torch.version.cuda}")
                
                # Check GPU memory
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
                logger.info(f"🎯 GPU Memory: {gpu_memory:.1f}GB")
            
            # Clear GPU cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Load the cached model (should work without network issues)
            logger.info("🧠 Loading cached Gemma3n E2B-it model...")
            self.model = Gemma3nForConditionalGeneration.from_pretrained(
                self.model_id,
                device_map="auto",
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                token=self.hf_token,
                trust_remote_code=True,
                use_safetensors=True,
                low_cpu_mem_usage=True,
                max_memory={0: "11GB"} if torch.cuda.is_available() else None,
                local_files_only=True   # Use only cached files
            ).eval()
            
            # Load processor
            logger.info("🔧 Loading cached processor...")
            self.processor = AutoProcessor.from_pretrained(
                self.model_id,
                token=self.hf_token,
                trust_remote_code=True,
                local_files_only=True   # Use only cached files
            )
            
            # Check where model actually loaded
            self._check_model_devices()
            
            # Print GPU status
            if torch.cuda.is_available():
                memory_mb = torch.cuda.memory_allocated() / 1024**2
                memory_cached = torch.cuda.memory_reserved() / 1024**2
                logger.info(f"📊 GPU Memory: {memory_mb:.0f}MB allocated, {memory_cached:.0f}MB cached")
            
            logger.info("✅ Cached Gemma3n E2B-it loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize cached Gemma3n E2B-it: {e}")
            raise

    def _check_model_devices(self):
        """Check which devices the model parameters are on"""
        devices = {}
        for name, param in self.model.named_parameters():
            device = str(param.device)
            if device not in devices:
                devices[device] = 0
            devices[device] += 1
        
        logger.info("📍 Model parameter distribution:")
        for device, count in devices.items():
            logger.info(f"   {device}: {count} parameters")

    # Update the ask_ai_tutor method in ai_tutor.py to handle response style

    def ask_ai_tutor(
        self, 
        question: str, 
        subject: str = "General", 
        language: str = "English", 
        level: str = "middle_school",
        max_tokens: int = 256,
        response_style: str = "regular"  # ← ADD THIS PARAMETER
    ) -> str:
        """Generate text response using cached Gemma3n E2B-it"""
        if not self.model or not self.processor:
            raise RuntimeError("AI Tutor not initialized. Call initialize() first.")
        
        # Validate token count
        max_tokens = max(50, min(2048, max_tokens))
        
        # Create level and subject-specific system prompt
        level_descriptions = {
            "elementary": "elementary school students (age 6-12)",
            "middle_school": "middle school students (age 12-15)", 
            "high_school": "high school students (age 15-18)",
            "university": "university students",
            "graduate": "graduate students and researchers",
            "professional": "professionals in the field"
        }
        
        level_desc = level_descriptions.get(level, "students")
        
        # Build system prompt
        system_content = f"You are a helpful {subject} tutor. Explain concepts clearly and appropriately for {level_desc}. Always respond in {language}. Be educational, engaging, and provide examples when helpful."
        
        # Handle response style modifications
        modified_question = question
        
        if response_style == "effective":
            # Add effective instruction prefix to the question
            style_prefix = "Provide a response without any introductory explanations, meta-responses, preface, or contextualization."
            modified_question = style_prefix + question
            
        elif response_style != "regular" and response_style != "effective":
            # Handle custom response style
            if response_style.strip():  # If there's a custom instruction
                modified_question = response_style.strip() + ": " + question
        
        # Create chat messages using the official format
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_content}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": modified_question}]  # ← Use modified question
            }
        ]
        
        try:
            start_time = time.time()
            
            # Apply chat template
            inputs = self.processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            ).to(self.model.device)
            
            input_len = inputs["input_ids"].shape[-1]
            
            # Generate with user-specified token count
            with torch.inference_mode():
                generation = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )
                
                # Sync if on GPU
                if str(self.model.device).startswith("cuda"):
                    torch.cuda.synchronize()
                    
                generation = generation[0][input_len:]
            
            # Decode response
            response = self.processor.decode(generation, skip_special_tokens=True)
            
            inference_time = time.time() - start_time
            tokens_generated = len(generation)
            
            # Log performance with device info, token count, and style
            device_info = "GPU" if str(self.model.device).startswith("cuda") else "CPU"
            style_info = f" [{response_style}]" if response_style != "regular" else ""
            logger.info(f"⚡ {device_info} Gemma3n E2B-it: {tokens_generated} tokens in {inference_time:.3f}s ({tokens_generated/inference_time:.1f} tok/s) [max: {max_tokens}]{style_info}")
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"❌ Error in Gemma3n E2B-it inference: {e}")
            raise

    def ask_image_question(self, image_input, question: str) -> str:
        """Analyze image using cached Gemma3n E2B-it vision capabilities"""
        if not self.model or not self.processor:
            raise RuntimeError("AI Tutor not initialized. Call initialize() first.")
        
        try:
            # Handle different image input types
            image = self._load_image(image_input)
            
            # Create chat messages with image
            messages = [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are a helpful AI assistant that can analyze images and answer questions about them in detail."}]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": question}
                    ]
                }
            ]
            
            start_time = time.time()
            
            # Apply chat template with image
            inputs = self.processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            ).to(self.model.device)
            
            input_len = inputs["input_ids"].shape[-1]
            
            # Generate with vision
            with torch.inference_mode():
                generation = self.model.generate(
                    **inputs,
                    max_new_tokens=300,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )
                
                if str(self.model.device).startswith("cuda"):
                    torch.cuda.synchronize()
                    
                generation = generation[0][input_len:]
            
            # Decode response
            response = self.processor.decode(generation, skip_special_tokens=True)
            
            inference_time = time.time() - start_time
            tokens_generated = len(generation)
            
            device_info = "GPU" if str(self.model.device).startswith("cuda") else "CPU"
            logger.info(f"🖼️ {device_info} Gemma3n E2B-it Vision: {tokens_generated} tokens in {inference_time:.3f}s ({tokens_generated/inference_time:.1f} tok/s)")
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"❌ Error in Gemma3n E2B-it vision: {e}")
            return f"Error analyzing image: {str(e)}"

    def _load_image(self, image_input) -> Image.Image:
        """Load image from URL, file path, or base64 data"""
        try:
            # Check if it's base64 data
            if isinstance(image_input, str) and image_input.startswith('data:image'):
                # Extract base64 data
                base64_data = image_input.split(',')[1]
                image_data = base64.b64decode(base64_data)
                return Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Check if it's a URL
            elif isinstance(image_input, str) and image_input.startswith(('http://', 'https://')):
                response = requests.get(image_input, timeout=10)
                response.raise_for_status()
                return Image.open(io.BytesIO(response.content)).convert('RGB')
            
            # Assume it's a file path or PIL Image
            elif isinstance(image_input, str):
                return Image.open(image_input).convert('RGB')
            elif isinstance(image_input, Image.Image):
                return image_input.convert('RGB')
            
            else:
                raise ValueError(f"Unsupported image input type: {type(image_input)}")
                
        except Exception as e:
            logger.error(f"❌ Failed to load image: {e}")
            raise ValueError(f"Could not load image: {str(e)}")

    async def ask_ai_tutor_stream(
        self, 
        question: str, 
        subject: str = "General", 
        language: str = "English", 
        level: str = "middle_school"
    ):
        """Streaming version"""
        try:
            response = self.ask_ai_tutor(question, subject, language, level)
            
            # Simulate streaming by yielding chunks
            words = response.split()
            current_chunk = ""
            
            for i, word in enumerate(words):
                current_chunk += word + " "
                
                if (i + 1) % 3 == 0 or i == len(words) - 1:
                    yield current_chunk.strip()
                    current_chunk = ""
                    
        except Exception as e:
            logger.error(f"❌ Error in Gemma3n E2B-it streaming: {e}")
            raise

    def get_model_size_info(self):
        """Get model info with device distribution"""
        if not self.model:
            return "Model not loaded"
        
        try:
            total_params = sum(p.numel() for p in self.model.parameters())
            
            # Check device distribution
            devices = {}
            for param in self.model.parameters():
                device = str(param.device)
                if device not in devices:
                    devices[device] = 0
                devices[device] += 1
            
            device_info = ", ".join([f"{count} params on {device}" for device, count in devices.items()])
            
            if torch.cuda.is_available():
                memory_mb = torch.cuda.memory_allocated() / 1024**2
                return f"Gemma3n E2B-it: {total_params/1e6:.1f}M total params ({device_info}), {memory_mb:.0f}MB GPU"
            else:
                return f"Gemma3n E2B-it: {total_params/1e6:.1f}M total params ({device_info})"
        except:
            return "Gemma3n E2B-it (Cached Model)"
