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

### 🧠 **Dual AI Capabilities**
- **📚 Text Tutor**: Interactive chat-based learning with streaming responses
- **🖼️ Image Analyzer**: Visual learning assistant for diagrams, charts, scientific images, and educational content
- **🔄 Real-time Processing**: Live response generation with typing indicators
- **💾 Local Processing**: 100% offline operation after initial setup

### 🎨 **Educational Customization**
- **Subject Areas**: 12+ predefined subjects (Computer Science, Mathematics, Physics, Biology, Chemistry, History, Literature, Psychology, Economics, Art, Music) + custom options
- **Languages**: 11+ languages (English, German, Spanish, French, Italian, Portuguese, Dutch, Chinese, Japanese, Korean, Arabic) + custom language input
- **Education Levels**: Elementary (6-11) → Professional + custom levels
- **Smart Context**: Responses automatically adapted to chosen subject, language, and education level

### 🔒 **Privacy & Security**
- **100% Local Processing**: No data sent to external servers during operation
- **Offline Ready**: Complete offline functionality after initial model download
- **Model Caching**: One-time download via Hugging Face Hub, permanent local storage
- **Privacy First**: All conversations, images, and data stay on your device
- **Secure Communication**: WebSocket communication between frontend and backend

### 🚀 **Modern User Experience**
- **Electron Desktop App**: Native desktop experience across platforms
- **Tabbed Interface**: Separate tabs for text tutoring and image analysis
- **Drag & Drop**: Easy image upload with live preview
- **Responsive Design**: Adapts to different screen sizes and resolutions
- **Real-time Feedback**: Connection status, loading indicators, and error handling

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

### Prerequisites
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Python 3.9+** - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)
- **8GB+ RAM** (16GB+ recommended for optimal performance)
- **NVIDIA GPU with 8GB+ VRAM** (required for smooth operation)
- **36GB+ free storage** (50GB+ recommended)
- **Hugging Face Account** with token - [Get yours here](https://huggingface.co/settings/tokens)

### System Requirements
- **Minimum**: 8GB RAM, 36GB free storage, quad-core CPU
- **Recommended**: 16GB+ RAM, 50GB free storage, octa-core CPU, NVIDIA GPU with 8GB+ VRAM
- **GPU Requirements**: 8GB+ VRAM highly recommended for smooth operation
- **Storage Breakdown**: ~30GB for model files + ~6GB for application and dependencies

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/offline-ai-tutor.git
cd offline-ai-tutor
```

2. **Run automated setup**
```bash
python setup.py
```
*This will automatically install all dependencies and check system requirements*

3. **Configure your Hugging Face token**
   - Edit `.env` file in the project root
   - Replace `your_hugging_face_token_here` with your actual token
   - Ensure you have access to the Gemma model: [Accept license here](https://huggingface.co/google/gemma-3n-e2b-it)

4. **Accept Gemma License**
   - Visit: https://huggingface.co/google/gemma-3n-e2b-it
   - Click "Agree and access repository"
   - This is required to download the model

### Manual Setup (Alternative)

<details>
<summary>Click to expand manual installation steps</summary>

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend Setup
```bash
cd frontend
npm install
```

#### Environment Configuration
1. Copy `.env.example` to `.env`
2. Edit `.env` with your Hugging Face token:
```env
HF_TOKEN=your_actual_token_here
HF_MODEL_ID=google/gemma-3n-e2b-it
BACKEND_PORT=5000
FRONTEND_PORT=3000
```

</details>

## 🚀 Running the Application

### Start the Complete Application
```bash
# From project root
cd frontend
npm start
```
*This will automatically start both backend and frontend*

### Development Mode (Separate Processes)

**Terminal 1 - Backend:**
```bash
cd backend

# Windows (PowerShell)
$env:TORCHDYNAMO_DISABLE="1"
python app.py

# Linux/macOS
export TORCHDYNAMO_DISABLE=1
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### First Run
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
4. **Ask Questions**: Type your question and press Enter or click "Ask Tutor"
5. **View Responses**: Real-time streaming responses with educational formatting

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
```env
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

# Restart backend
cd backend && python app.py
```

**Model Download Fails**
- Verify Hugging Face token is correct
- Check internet connection (stable connection required for 30GB download)
- Ensure you've accepted Gemma license
- Verify sufficient storage space (36GB+ free)
- Try clearing cache: `rm -rf ~/.cache/huggingface/`
- Consider downloading during off-peak hours for better speeds

**GPU Out of Memory**
- Ensure you have 8GB+ VRAM available
- Close all other GPU-intensive applications (games, video editing, mining)
- Check GPU memory usage: `nvidia-smi`
- Reduce `max_memory` setting in `ai_tutor.py` if needed
- Consider upgrading to a GPU with more VRAM
- CPU fallback available but significantly slower

**Slow Performance**
- **GPU Required**: Ensure 8GB+ VRAM GPU is being used
- Check GPU utilization: `nvidia-smi`
- Enable GPU acceleration if not already active
- Increase system RAM to 16GB+ for optimal performance
- Close other memory-intensive applications
- Upgrade to faster storage (SSD recommended)
- For CPU-only: Performance will be significantly slower but functional

**Frontend Won't Start**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules && npm install

# Check Node.js version
node --version  # Should be 18+
```

### Windows Specific
- **PowerShell Execution Policy**: Set `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **PyTorch CUDA**: Ensure CUDA toolkit is installed for GPU acceleration
- **Antivirus**: Add project folder to antivirus exclusions

### macOS Specific
- **Permission Issues**: Run `chmod +x setup.py` if needed
- **Xcode Tools**: Install with `xcode-select --install`
- **Homebrew**: Use for Python/Node.js installation

### Linux Specific
- **Dependencies**: Install `build-essential python3-dev`
- **CUDA**: Install NVIDIA CUDA toolkit for GPU support
- **Display**: Ensure X11 forwarding for GUI applications

## 🔬 Technical Details

### Model Information
- **Name**: google/gemma-3n-e2b-it
- **Type**: Instruction-tuned multimodal transformer
- **Size**: ~27B parameters (large model requiring significant resources)
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
│   ├── app.py                 # Main Flask application
│   ├── ai_tutor.py           # Gemma model interface
│   ├── image_analyzer.py     # Vision capabilities
│   ├── model_manager.py      # Model downloading/caching
│   ├── config.py             # Configuration management
│   └── requirements.txt      # Python dependencies
├── frontend/                  # Electron desktop app
│   ├── main.js               # Electron main process
│   ├── package.json          # Node.js dependencies
│   └── src/                  # Frontend source files
│       ├── index.html        # Main UI layout
│       ├── renderer.js       # Frontend JavaScript
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

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### API Endpoints
- `GET /health` - Backend health check
- `WebSocket /socket.io/` - Real-time communication
- `POST ask_ai_tutor` - Text generation requests
- `POST ask_image_question` - Image analysis requests

## 📚 Educational Use Cases

### For Students
- **Homework Help**: Get explanations for complex topics
- **Language Learning**: Practice in multiple languages
- **Visual Learning**: Analyze diagrams and educational images
- **Exam Preparation**: Custom difficulty levels for practice

### For Educators
- **Teaching Aid**: Generate explanations at appropriate levels
- **Multilingual Support**: Assist non-native speakers
- **Visual Content**: Analyze educational images and diagrams
- **Curriculum Support**: Adapt content to different grade levels

### For Researchers
- **Document Analysis**: Analyze research papers and figures
- **Data Visualization**: Interpret charts and graphs
- **Technical Writing**: Get help with complex explanations
- **Literature Review**: Summarize and explain concepts

## 🤝 Support

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/offline-ai-tutor/issues)
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in GitHub Discussions
- **Email**: Contact maintainers for urgent issues

### Known Limitations
- **Hardware Requirements**: Requires high-end hardware (8GB+ VRAM GPU, 16GB+ RAM recommended)
- **Large Model**: 30GB download and significant computational requirements
- **GPU Dependency**: CPU-only mode is functional but significantly slower
- **Language Quality**: Best performance in English, good in major languages
- **Image Types**: Works best with clear, educational images
- **Internet Required**: Only for initial model download (30GB+)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
- **OpenAI**: For inspiration from ChatGPT's educational approach

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Initial release with Gemma-3n-e2b-it model
- ✅ Text tutoring with multilingual support
- ✅ Image analysis capabilities
- ✅ Electron desktop application
- ✅ Automated setup and configuration
- ✅ Complete offline functionality

### Planned Features
- 🔄 Voice input/output support
- 🔄 PDF document analysis
- 🔄 Enhanced image understanding
- 🔄 Conversation history and bookmarks
- 🔄 Additional model options
- 🔄 Plugin system for extensions

---

**🎓 Ready to enhance your learning experience? Get started with the Offline AI Tutor today!**
