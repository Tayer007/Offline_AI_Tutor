# Offline_AI_Tutor
An offline AI tutor that could transform education in developing countries by running on existing school computers.
📋 **[Read our Impact Statement](IMPACT_STATEMENT.md)** to understand the global educational potential of this project.


Offline AI Tutor : A comprehensive offline desktop application powered by Google's **Gemma-3n-e2b-it** model from Hugging Face, designed as an educational AI tutor with multilingual support, educational level adaptation, and vision capabilities for image analysis.

![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Node.js](https://img.shields.io/badge/node.js-18%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![AI Model](https://img.shields.io/badge/AI-Gemma--3n--e2b--it-orange)

## 🌟 Key Features

### 🧠 Dual AI Capabilities
- **📚 Text Tutor**: Interactive chat-based learning with streaming responses
- **🖼️ Image Analyzer**: Visual learning assistant for diagrams, charts, scientific images, and educational content
- **🔄 Real-time Processing**: Live response generation with typing indicators
- **💾 Local Processing**: 100% offline operation after initial setup

### 🎨 Educational Customization
- **Subject Areas**: 12+ predefined subjects (Computer Science, Mathematics, Physics, Biology, Chemistry, History, Literature, Psychology, Economics, Art, Music) + custom options
- **Languages**: 11+ languages (English, German, Spanish, French, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, Arabic) + custom language input
- **Education Levels**: Elementary (6-11) → Professional + custom levels
- **⚡ Response Length Control**: Choose from Quick (128 tokens), Standard (256 tokens), Detailed (512 tokens), Comprehensive (1024 tokens), or custom token count (50-2048)
- **🎯 Response Style Control**: Choose between Regular (standard explanations) or Effective (direct, no-fluff responses) or custom instruction prefixes
- **Smart Context**: Responses automatically adapted to chosen subject, language, education level, desired length, and response style

### 🔒 Privacy & Security
- **100% Local Processing**: No data sent to external servers during operation
- **Offline Ready**: Complete offline functionality after initial model download
- **Model Caching**: One-time download via Hugging Face Hub, permanent local storage
- **Privacy First**: All conversations, images, and data stay on your device
- **Secure Communication**: WebSocket communication between frontend and backend

### 🚀 Modern User Experience
- **Electron Desktop App**: Native desktop experience across platforms
- **Tabbed Interface**: Separate tabs for text tutoring and image analysis
- **Drag & Drop**: Easy image upload with live preview
- **Responsive Design**: Adapts to different screen sizes and resolutions
- **Real-time Feedback**: Connection status, loading indicators, and error handling
- **Customizable Responses**: Full control over response length and detail level

## 🏗️ Architecture

### Backend (Python + Flask)
- **🔥 Flask + SocketIO**: Real-time WebSocket communication
- **🤗 Transformers 4.53.2**: Latest Hugging Face transformers library
- **🎯 Gemma-3n-e2b-it**: Google's instruction-tuned multimodal model
- **⚡ GPU Acceleration**: CUDA support with CPU fallback
- **📦 Model Management**: Automatic downloading and caching

### Frontend (Electron + Web Technologies)
- **⚡ Electron 28+**: Cross-platform desktop application framework
- **🌐 Socket.IO Client**: Real-time WebSocket communication
- **🎨 Modern CSS**: Clean, educational-focused design
- **📱 Responsive UI**: Mobile-friendly layout with accessibility features

### Communication
- **🔗 WebSocket Protocol**: Real-time bidirectional communication via Socket.IO
- **📡 Event-Driven**: Asynchronous message handling for smooth user experience
- **🔄 Auto-Reconnection**: Automatic connection recovery with retry logic

## 📦 Installation

> **🚀 Coming Soon**: We're working on a **code-free, one-click installer** for Windows, macOS, and Linux that will eliminate all manual setup steps. The installer will automatically handle dependencies, authentication, and model downloads with just a few clicks!

### Prerequisites
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Python 3.9+** - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)
- **8GB+ RAM** (16GB+ recommended for optimal performance)
- **NVIDIA GPU with 8GB+ VRAM** (required for smooth operation)
- **36GB+ free storage** (50GB+ recommended)
- **Hugging Face Account with token** - [Get yours here](https://huggingface.co/settings/tokens)

### System Requirements
- **Minimum**: 8GB RAM, 36GB free storage, quad-core CPU
- **Recommended**: 16GB+ RAM, 50GB free storage, octa-core CPU, NVIDIA GPU with 8GB+ VRAM
- **GPU Requirements**: 8GB+ VRAM highly recommended for smooth operation
- **Storage Breakdown**: ~30GB for model files + ~6GB for application and dependencies

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/Tayer007/Offline_AI_Tutor.git
cd Offline_AI_Tutor
```

2. **Run automated setup**
```bash
python setup.py
```
This will automatically install all dependencies and check system requirements

3. **Accept Gemma License** (Do this first!)
   - Visit: https://huggingface.co/google/gemma-3n-e2b-it
   - Click "Agree and access repository"
   - This is required to download the model

4. **Configure your Hugging Face Authentication**
   
   **Method 1: CLI Login (Recommended)**
   ```bash
   # Install Hugging Face CLI if not already installed
   pip install huggingface_hub
   
   # Login using CLI (recommended method)
   huggingface-cli login
   # OR alternatively
   hf auth login
   
   # Paste your token when prompted
   ```
   
   **Method 2: Environment File (Alternative)**
   - Edit `.env` file in the project root
   - Replace `your_hugging_face_token_here` with your actual token
   - **Note**: If you experience authentication issues with the .env method, use CLI login instead

### Manual Setup (Alternative)

**Backend Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend Dependencies:**
```bash
cd frontend
npm install
```

## 🚀 Running the Application

### Development Mode (Separate Processes)

**Terminal 1 - Backend:**
```bash
cd backend

# Windows (PowerShell) - REQUIRED
# From project root
cd backend
$env:TORCHDYNAMO_DISABLE="1"
python app.py

# Linux/macOS - REQUIRED
# From project root
cd backend
export TORCHDYNAMO_DISABLE=1
python app.py
```
> **⚠️ IMPORTANT**: The `TORCHDYNAMO_DISABLE=1` environment variable is **required** before running the backend. This disables PyTorch's TorchDynamo compiler which can cause compatibility issues with certain model operations and transformer library versions. Without this setting, you may encounter compilation errors, slow performance, or unexpected crashes during model loading or inference.

**Terminal 2 - Start the frontend:**
```bash
# From project root
cd frontend
npm start
```



**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### First Run
- **Authentication Setup**: Ensure Hugging Face authentication is configured (CLI login recommended)
- **Model Download**: The first startup will download ~30GB of model files
- **Download Time**: 30-60 minutes depending on internet speed (large model files)
- **Progress**: Monitor download progress in the console
- **GPU Requirements**: Ensure 8GB+ VRAM available before starting
- **Offline Usage**: After initial download, works completely offline

## 💻 Usage Guide

### Text Tutor
1. **Select Subject**: Choose from predefined subjects or enter custom
2. **Choose Language**: Select response language (11+ options)
3. **Set Education Level**: Pick appropriate complexity level
4. **Choose Response Length**: Select from Quick/Standard/Detailed/Comprehensive or set custom token count
5. **Select Response Style**: Choose Regular (explanatory) or Effective (direct) or custom instruction prefix
6. **Ask Questions**: Type your question and press Enter or click "Ask Tutor"
7. **View Responses**: Real-time streaming responses with educational formatting

**Response Length Options:**
- **Quick (128 tokens)**: Brief, concise answers
- **Standard (256 tokens)**: Balanced explanations (default)
- **Detailed (512 tokens)**: In-depth explanations with examples
- **Comprehensive (1024 tokens)**: Thorough coverage with multiple perspectives
- **Custom (50-2048 tokens)**: Set your exact preferred length

**Response Style Options:**
- **Regular**: Standard educational explanations with context and background
- **Effective**: Direct, concise responses without introductory explanations, meta-responses, preface, or contextualization
- **Custom**: Set your own instruction prefix (e.g., "Be extremely brief:", "Use analogies:", etc.)

**Example Questions:**
- "Explain quantum physics for high school students"
- "Help me understand calculus derivatives"
- "What is machine learning in simple terms?"
- "Erkläre mir Photosynthese auf Deutsch" (German)

### Image Analyzer
1. **Upload Image**: Drag & drop, browse files, or paste URL
2. **Preview**: Review uploaded image before analysis
3. **Ask Question**: Type specific questions about the image
4. **Analyze**: Click "Analyze Image" for AI-powered insights
5. **Results**: View detailed analysis with educational context

**Supported Images:**
- 📊 Charts, graphs, data visualizations
- 🔬 Scientific diagrams and processes
- 📚 Historical documents and images
- 🎨 Artwork and visual compositions
- 🧮 Mathematical problems and equations
- 🗺️ Maps and geographical features

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Hugging Face Configuration
HF_TOKEN=your_actual_token_here
HF_MODEL_ID=google/gemma-3n-e2b-it

# Server Configuration
BACKEND_PORT=5000
FRONTEND_PORT=3000

# Model Configuration
MAX_NEW_TOKENS=512
TEMPERATURE=0.7
DO_SAMPLE=true

# Cache Configuration
MODEL_CACHE_DIR=./models_cache
```

### Advanced Settings
- **GPU Memory**: Automatically managed, configurable in `ai_tutor.py`
- **Model Precision**: BFloat16 (GPU) / Float32 (CPU)
- **Cache Location**: `~/.cache/huggingface/transformers/`
- **Connection Settings**: Configurable timeouts and retry logic

## 🔧 Troubleshooting

### Common Issues

**"Connection Failed" Error**
```bash
# Check if backend is running
curl http://localhost:5000/health

# Restart backend with required environment variable
cd backend
$env:TORCHDYNAMO_DISABLE="1"  # Windows PowerShell
# OR
export TORCHDYNAMO_DISABLE=1  # Linux/macOS
python app.py
```

**Model Download Fails**
- **Authentication Issues**: If .env file token doesn't work, use CLI login instead:
  ```bash
  huggingface-cli login
  # OR
  hf auth login
  ```
- Verify Hugging Face token is correct and has been accepted via CLI
- Check internet connection (stable connection required for 30GB download)
- Ensure you've accepted Gemma license **before** attempting download
- Verify sufficient storage space (36GB+ free)
- Try clearing cache: `rm -rf ~/.cache/huggingface/`
- Consider downloading during off-peak hours for better speeds

**Backend Startup Issues**
- **Always set** `TORCHDYNAMO_DISABLE=1` before running `python app.py`
- This prevents PyTorch compilation issues that can cause crashes
- Check PyTorch installation: `python -c "import torch; print(torch.__version__)"`
- Verify CUDA compatibility if using GPU

**GPU Out of Memory**
- **Hardware Requirements**: Ensure you have at least 8GB VRAM + 3GB free RAM (model uses GPU-RAM offloading)
- **Total Memory Needed**: ~11GB combined (8GB VRAM + 3GB RAM for shared GPU memory)
- Close all other GPU-intensive applications (games, video editing, mining)
- Close unnecessary browser tabs and applications to free up RAM
- Check GPU memory usage: `nvidia-smi`
- Check RAM usage: Task Manager (Windows) or `htop` (Linux/macOS)
- **Cannot reduce memory**: Model requires minimum 11GB total - reducing settings won't help
- Consider upgrading to a GPU with 12GB+ VRAM for pure GPU operation
- CPU fallback available but significantly slower

**Slow Performance**
- **GPU Required**: Ensure 8GB+ VRAM GPU is being used
- Check GPU utilization: `nvidia-smi`
- Enable GPU acceleration if not already active
- Increase system RAM to 16GB+ for optimal performance
- Close other memory-intensive applications
- Upgrade to faster storage (SSD recommended)
- For CPU-only: Performance will be significantly slower but functional

**Important Note: This project was designed to work with a quantized (4-bit) version of Gemma 3n that would require only 4GB RAM and no GPU. We implemented the full, unquantized model purely for demonstration and availability purposes. In theory, a properly quantized version would make this educational AI accessible on basic institutional PCs worldwide. For more details on the intended vision and global impact, please read our [IMPACT_STATEMENT.md](IMPACT_STATEMENT.md).**

**Frontend Won't Start**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules && npm install

# Check Node.js version
node --version  # Should be 18+
```

### Platform-Specific Issues

**Windows Specific**
- **PowerShell Execution Policy**: Set `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **PyTorch CUDA**: Ensure CUDA toolkit is installed for GPU acceleration
- **Antivirus**: Add project folder to antivirus exclusions
- **Environment Variables**: Use PowerShell syntax: `$env:TORCHDYNAMO_DISABLE="1"`

**macOS Specific**
- **Permission Issues**: Run `chmod +x setup.py` if needed
- **Xcode Tools**: Install with `xcode-select --install`
- **Homebrew**: Use for Python/Node.js installation
- **Environment Variables**: Use bash syntax: `export TORCHDYNAMO_DISABLE=1`

**Linux Specific**
- **Dependencies**: Install `build-essential python3-dev`
- **CUDA**: Install NVIDIA CUDA toolkit for GPU support
- **Display**: Ensure X11 forwarding for GUI applications
- **Environment Variables**: Use bash syntax: `export TORCHDYNAMO_DISABLE=1`

## 🔬 Technical Details

### Model Information
- **Name**: google/gemma-3n-e2b-it
- **Type**: Instruction-tuned multimodal transformer
- **Size**: ~2-5B parameters (varies based on loaded components: text, vision, audio, embeddings)
- **Core Text Parameters**: 1.9B
- **Vision Parameters**: 0.3B
- **Audio Parameters**: 0.6B
- **Per-Layer Embedding**: 2.55B
- **Precision**: BFloat16 (GPU) / Float32 (CPU)
- **Context Length**: 8192 tokens
- **VRAM Requirements**: 8GB+ for smooth operation
- **Languages**: Multilingual support with English preference

### Performance Metrics
- **Text Generation**: 30-60 tokens/second (8GB+ VRAM GPU), 2-5 tokens/second (CPU)
- **Image Analysis**: 1-3 seconds per image (8GB+ VRAM GPU), 15-30 seconds (CPU)
- **Memory Usage**: 8-12GB RAM + 8GB+ VRAM (GPU), 16-24GB RAM (CPU only)
- **Storage**: ~30GB for model files, ~6GB for application and dependencies

### Security Features
- **Local Processing**: All AI inference happens locally
- **No Telemetry**: No data collection or tracking
- **Secure Communication**: WebSocket with localhost binding
- **Model Verification**: SHA256 checksums for downloaded models

## 🛠️ Development

### Project Structure
```
offline-ai-tutor/
├── backend/                    # Python Flask backend
│   ├── app.py                 # Main Flask application with SocketIO
│   ├── ai_tutor.py           # Gemma model interface with token control
│   ├── image_analyzer.py     # Vision capabilities
│   ├── model_manager.py      # Model downloading/caching
│   ├── config.py             # Configuration management
│   └── requirements.txt      # Python dependencies
├── frontend/                  # Electron desktop app
│   ├── main.js               # Electron main process
│   ├── package.json          # Node.js dependencies
│   └── src/                  # Frontend source files
│       ├── index.html        # Main UI layout with token selector
│       ├── renderer.js       # Frontend JavaScript with SocketIO
│       ├── preload.js        # Electron security layer
│       └── styles.css        # Complete styling
├── .env                      # Environment configuration
├── setup.py                  # Automated setup script
└── README.md                 # This file
```

### Building for Distribution
```bash
# Create distributable packages
cd frontend
npm run build

# Platform-specific builds
npm run build:win     # Windows installer
npm run build:mac     # macOS DMG
npm run build:linux   # Linux AppImage
```

> **🔮 Future Plans**: We're developing a comprehensive installer that will bundle Python, Node.js, and all dependencies into a single executable package. Users will only need to download one file, run it, authenticate with Hugging Face through a built-in interface, and start using the AI tutor immediately.

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### API Endpoints
- **GET /health** - Backend health check
- **WebSocket /socket.io/** - Real-time communication
- **Event: ask_ai_tutor** - Text generation requests with token control
- **Event: ask_image_question** - Image analysis requests

## 📚 Educational Use Cases

### For Students
- **Homework Help**: Get explanations for complex topics with adjustable detail levels
- **Language Learning**: Practice in multiple languages
- **Visual Learning**: Analyze diagrams and educational images
- **Exam Preparation**: Custom difficulty levels and response lengths for practice

### For Educators
- **Teaching Aid**: Generate explanations at appropriate levels and lengths
- **Multilingual Support**: Assist non-native speakers
- **Visual Content**: Analyze educational images and diagrams
- **Curriculum Support**: Adapt content to different grade levels and time constraints

### For Researchers
- **Document Analysis**: Analyze research papers and figures
- **Data Visualization**: Interpret charts and graphs
- **Technical Writing**: Get help with complex explanations at various detail levels
- **Literature Review**: Summarize and explain concepts

## 🤝 Support

### Getting Help
- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in GitHub Discussions
- **Email**: Contact maintainers for urgent issues

### Known Limitations
- **Hardware Requirements**: Requires high-end hardware (8GB+ VRAM GPU, 16GB+ RAM recommended)
- **Large Model**: 30GB download and significant computational requirements
- **GPU Dependency**: CPU-only mode is functional but significantly slower
- **Environment Variable**: Must set `TORCHDYNAMO_DISABLE=1` before running backend
- **Authentication**: .env file token method may sometimes fail - use `huggingface-cli login` as fallback
- **Language Quality**: Best performance in English, good in major languages
- **Image Types**: Works best with clear, educational images
- **Internet Required**: Only for initial model download (30GB+)

**Important Note: This project was designed to work with a quantized (4-bit) version of Gemma 3n that would require only 4GB RAM and no GPU. We implemented the full, unquantized model purely for demonstration and availability purposes. In theory, a properly quantized version would make this educational AI accessible on basic institutional PCs worldwide. For more details on the intended vision and global impact, please read our [IMPACT_STATEMENT.md](IMPACT_STATEMENT.md).**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### Third-Party Licenses
- **Gemma Model**: Subject to Google's Gemma license terms
- **Hugging Face**: Apache 2.0 License
- **Electron**: MIT License
- **Flask**: BSD-3-Clause License

## 🙏 Acknowledgments

- **Google**: For the Gemma-3n-e2b-it model
- **Hugging Face**: For the transformers library and model hosting
- **Electron Team**: For the cross-platform desktop framework
- **Flask Team**: For the lightweight web framework

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Initial release with Gemma-3n-e2b-it model
- ✅ Text tutoring with multilingual support
- ✅ **NEW: Customizable response length control (50-2048 tokens)**
- ✅ Image analysis capabilities
- ✅ Electron desktop application with real-time SocketIO communication
- ✅ Automated setup and configuration
- ✅ Complete offline functionality
- ✅ **NEW: Enhanced UI with token selection and custom inputs**

### Planned Features
- 🔄 **Code-Free Installation**: One-click installer packages for Windows, macOS, and Linux (no manual setup required)
- 🔄 **Automated Authentication**: Streamlined Hugging Face login process integrated into the installer
- 🔄 Voice input/output support
- 🔄 PDF document analysis
- 🔄 Enhanced image understanding
- 🔄 Conversation history and bookmarks
- 🔄 Additional model options
- 🔄 Plugin system for extensions
- 🔄 **Simplified Distribution**: Pre-packaged executables with automatic dependency management

---

🎓 **Ready to enhance your learning experience with full control over response detail and length?** Get started with the Offline AI Tutor today!
