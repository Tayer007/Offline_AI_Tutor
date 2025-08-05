"""
Robust Flask Backend for AI Tutor - Fixed for multiple responses
"""
from flask import Flask, request
from flask_socketio import SocketIO, emit, disconnect
import json
import uuid
import time
import os
from dotenv import load_dotenv
import asyncio
import logging
from threading import Timer, Lock
import torch
import traceback

# Import your actual AI classes
from ai_tutor import AITutor
from model_manager import ModelManager
from config import get_settings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize SocketIO with robust settings
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=False,
    engineio_logger=False,
    ping_timeout=900,
    ping_interval=30,
    max_http_buffer_size=10000000,
    always_connect=True,
    manage_session=True
)

# Global variables with thread safety
settings = None
model_manager = None
ai_tutor = None
image_analyzer = None
models_loaded = False
loading_in_progress = False
response_lock = Lock()  # Thread safety for responses

# Track active connections
active_connections = {}
connection_lock = Lock()

def send_loading_status(message):
    """Send loading status to all connected clients with error handling"""
    try:
        with connection_lock:
            if active_connections:
                socketio.emit('model_loading_status', {
                    'message': message,
                    'timestamp': time.time()
                })
                print(f"📡 Status sent to {len(active_connections)} clients: {message}")
            else:
                print(f"📡 Status (no clients): {message}")
    except Exception as e:
        print(f"⚠️ Failed to send status: {e}")

def initialize_models():
    """Initialize AI models with robust error handling"""
    global settings, model_manager, ai_tutor, image_analyzer, models_loaded, loading_in_progress
    
    if loading_in_progress:
        print("⚠️ Model loading already in progress...")
        return
        
    loading_in_progress = True
    
    try:
        print("🚀 Starting AI Tutor Backend...")
        send_loading_status("🚀 Starting AI Tutor Backend...")
        
        # Get settings with fallback
        try:
            settings = get_settings()
            send_loading_status("📋 Configuration loaded...")
        except Exception as e:
            print(f"⚠️ Using fallback settings: {e}")
            class FallbackSettings:
                hf_model_id = "google/gemma-3n-e2b-it"
                hf_token = None
            settings = FallbackSettings()
        
        # Validate HF token
        if not settings.hf_token or settings.hf_token == "your_hugging_face_token_here":
            print("❌ HF_TOKEN environment variable not found!")
            send_loading_status("🔧 Waiting for HuggingFace token...")
            token = input("Enter your HuggingFace token: ")
            settings.hf_token = token
            print("✅ Token set temporarily")
        
        print(f"✅ HF Token present: {bool(settings.hf_token)}")
        send_loading_status("🔑 HuggingFace token validated...")
        
        # Initialize model manager
        print("📦 Loading Gemma model from cache...")
        send_loading_status("📦 Checking cached models...")
        
        try:
            model_manager = ModelManager(settings)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            model_id = loop.run_until_complete(model_manager.ensure_model_available())
            send_loading_status(f"✅ Model found: {model_id}")
        except Exception as e:
            print(f"⚠️ Model manager failed, using direct model ID: {e}")
            model_id = "google/gemma-3n-e2b-it"
            send_loading_status("📦 Using cached model directly...")
        
        # Initialize AI tutor
        print("🎓 Initializing AI Tutor...")
        send_loading_status("🎓 Loading AI Tutor model...")
        
        ai_tutor = AITutor(model_id, settings.hf_token)
        ai_tutor.initialize()
        
        send_loading_status("✅ AI Tutor loaded successfully!")
        
        # Initialize Image Analyzer
        print("🖼️ Setting up Image Analyzer...")
        send_loading_status("🖼️ Setting up Image Analyzer...")
        
        try:
            image_analyzer = ai_tutor  # Share the same model instance
            print("✅ Image Analyzer using shared model")
            send_loading_status("✅ Image Analyzer ready!")
        except Exception as e:
            print(f"⚠️ Image Analyzer failed: {e}")
            send_loading_status("⚠️ Image analysis unavailable - text-only mode")
            image_analyzer = None
        
        models_loaded = True
        loading_in_progress = False
        
        print("✅ All models initialized successfully!")
        send_loading_status("🎉 All AI models loaded! Ready to chat!")
        
        Timer(2.0, lambda: send_loading_status("✨ AI Tutor is ready for questions!")).start()
        
    except Exception as e:
        print(f"❌ Failed to initialize models: {e}")
        traceback.print_exc()
        send_loading_status(f"❌ Model loading failed: {str(e)}")
        loading_in_progress = False
        models_loaded = False
        raise

def send_keep_alive():
    """Send periodic keep-alive with robust error handling"""
    try:
        with connection_lock:
            if active_connections:
                socketio.emit('keep_alive', {
                    'timestamp': time.time(),
                    'status': 'ready' if models_loaded else 'loading',
                    'active_connections': len(active_connections)
                })
    except Exception as e:
        print(f"⚠️ Keep-alive failed: {e}")
    
    Timer(25.0, send_keep_alive).start()

@app.route('/')
def index():
    return {
        "status": "AI Tutor Backend Running", 
        "websocket": "Connect to /socket.io/",
        "models_loaded": models_loaded,
        "active_connections": len(active_connections),
        "text_model": "ready" if ai_tutor else "loading" if loading_in_progress else "failed",
        "image_model": "ready" if image_analyzer else "unavailable",
        "loading_in_progress": loading_in_progress
    }

@app.route('/health')
def health():
    return {
        "status": "healthy" if models_loaded else "loading" if loading_in_progress else "failed",
        "tutor_ready": ai_tutor is not None,
        "image_analyzer_ready": image_analyzer is not None,
        "websocket_endpoint": "/socket.io/",
        "models_loaded": models_loaded,
        "loading_in_progress": loading_in_progress,
        "active_connections": len(active_connections),
        "model_id": getattr(settings, 'hf_model_id', 'unknown') if settings else "unknown",
        "gpu_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name() if torch.cuda.is_available() else "N/A"
    }

@socketio.on('ask_ai_tutor')
def handle_text_tutor(data):
    client_id = request.sid
    
    print(f"\n" + "="*80)
    print(f"🎓 NEW REQUEST FROM CLIENT: {client_id}")
    print(f"📥 Raw data received: {data}")
    print(f"🔍 Data type: {type(data)}")
    print(f"🕐 Request time: {time.time()}")
    print(f"="*80)
    
    try:
        message_id = str(uuid.uuid4())
        user_message = data.get('message', 'NO_MESSAGE')
        settings_data = data.get('settings', {})
        
        # Extract max_tokens from settings
        max_tokens = settings_data.get('max_tokens', 256)
        
        print(f"🆔 Generated message_id: {message_id}")
        print(f"💬 User message: '{user_message}'")
        print(f"⚙️ Settings: {settings_data}")
        print(f"⚡ Max tokens: {max_tokens}")
        
        if not models_loaded or not ai_tutor:
            print(f"❌ MODELS NOT READY - models_loaded: {models_loaded}, ai_tutor: {ai_tutor is not None}")
            emit('error', {
                'type': 'error',
                'message': 'AI models are still loading.',
                'context': 'text-tutor'
            })
            return
        
        print(f"✅ Models ready, proceeding with generation")
        
        # Step 1: Send start signal
        print(f"📤 STEP 1: Sending text_response_start to {client_id}")
        try:
            emit('text_response_start', {
                'type': 'text_response_start',
                'message_id': message_id,
                'timestamp': time.time()
            })
            print(f"✅ text_response_start sent successfully")
        except Exception as e:
            print(f"❌ FAILED to send text_response_start: {e}")
            return
        
        # Step 2: Generate response
        print(f"🔄 STEP 2: Generating AI response...")
        start_time = time.time()
        
        try:
            response = ai_tutor.ask_ai_tutor(
                question=user_message,
                subject=settings_data.get('subject', 'General'),
                language=settings_data.get('language', 'English'),
                level=settings_data.get('level', 'middle_school'),
                max_tokens=max_tokens  # ← PASS THE TOKEN COUNT
            )
            
            generation_time = time.time() - start_time
            print(f"✅ AI response generated in {generation_time:.2f}s")
            print(f"📝 Response length: {len(response)} characters")
            
            # PRINT THE FULL RESPONSE SO WE CAN SEE IT
            print(f"\n{'🤖 FULL AI RESPONSE:':=^80}")
            print(response)
            print(f"{'END OF AI RESPONSE':=^80}\n")
            
        except Exception as e:
            print(f"❌ AI GENERATION FAILED: {e}")
            import traceback
            traceback.print_exc()
            response = f"Error generating response: {str(e)}"
            
            # PRINT THE ERROR RESPONSE TOO
            print(f"\n{'❌ ERROR RESPONSE:':=^80}")
            print(response)
            print(f"{'END OF ERROR RESPONSE':=^80}\n")
        
        # Step 3: Send response
        print(f"📤 STEP 3: Sending text_response_chunk to {client_id}")
        print(f"📦 Chunk content length: {len(response)}")
        try:
            emit('text_response_chunk', {
                'type': 'text_response_chunk',
                'message_id': message_id,
                'content': response,
                'timestamp': time.time()
            })
            print(f"✅ text_response_chunk sent successfully ({len(response)} chars)")
        except Exception as e:
            print(f"❌ FAILED to send text_response_chunk: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 4: Send completion
        print(f"📤 STEP 4: Sending text_response_complete to {client_id}")
        try:
            emit('text_response_complete', {
                'type': 'text_response_complete',
                'message_id': message_id,
                'timestamp': time.time()
            })
            print(f"✅ text_response_complete sent successfully")
        except Exception as e:
            print(f"❌ FAILED to send text_response_complete: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"🎉 REQUEST COMPLETED for {client_id}")
        print(f"="*80 + "\n")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR in handler: {e}")
        import traceback
        traceback.print_exc()
        print(f"="*80 + "\n")

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    
    with connection_lock:
        if client_id in active_connections:
            connection_info = active_connections.pop(client_id)
            print(f'🔌 Client {client_id} disconnected after {connection_info["message_count"]} messages (Remaining: {len(active_connections)})')
        else:
            print(f'🔌 Unknown client disconnected: {client_id}')

@socketio.on('ping')
def handle_ping(data):
    """Handle ping from client to keep connection alive"""
    client_id = request.sid
    
    with connection_lock:
        if client_id in active_connections:
            active_connections[client_id]['last_ping'] = time.time()
    
    try:
        emit('pong', {'timestamp': time.time(), 'client_id': client_id})
    except Exception as e:
        print(f"❌ Error sending pong to {client_id}: {e}")

@socketio.on('ask_image_question')
def handle_image_analysis(data):
    client_id = request.sid
    
    with response_lock:
        try:
            image_url = data['image_url']
            question = data['question']
            
            print(f"🖼️ Processing image analysis for {client_id}: {question[:50]}...")
            
            if not models_loaded or not image_analyzer:
                emit('error', {
                    'type': 'error',
                    'message': 'Image analysis is not available. Running in text-only mode.',
                    'context': 'image-analyzer',
                    'timestamp': time.time(),
                    'client_id': client_id
                })
                return
            
            emit('image_analysis_start', {
                'type': 'image_analysis_start',
                'timestamp': time.time(),
                'client_id': client_id
            })
            
            try:
                result = image_analyzer.ask_image_question(image_url, question)
                
                emit('image_analysis_result', {
                    'type': 'image_analysis_result',
                    'result': result,
                    'timestamp': time.time(),
                    'client_id': client_id
                })
                
                print(f"✅ Image analysis completed for {client_id}")
                
            except Exception as e:
                print(f"❌ Error in image analysis for {client_id}: {e}")
                emit('error', {
                    'type': 'error',
                    'message': f"Error analyzing image: {str(e)}",
                    'context': 'image-analyzer',
                    'timestamp': time.time(),
                    'client_id': client_id
                })
            
        except Exception as e:
            print(f"❌ Image analysis handler error for {client_id}: {e}")
            traceback.print_exc()

if __name__ == '__main__':
    print("🚀 Starting Robust AI Tutor Backend")
    print("📡 WebSocket endpoint: ws://localhost:5000/socket.io/")
    print("🌐 HTTP endpoint: http://localhost:5000/")
    print("🔍 Health check: http://localhost:5000/health")
    
    # Start keep-alive mechanism
    print("💓 Starting keep-alive mechanism...")
    Timer(10.0, send_keep_alive).start()
    
    # Initialize models
    try:
        initialize_models()
    except Exception as e:
        print(f"❌ Model initialization failed: {e}")
        print("⚠️ Starting server anyway - models can be loaded later")
    
    # Run with SocketIO
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        use_reloader=False,
        allow_unsafe_werkzeug=True
    )