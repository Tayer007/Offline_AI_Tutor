#!/usr/bin/env python3
"""
One-click setup script for Offline AI Tutor using Hugging Face
"""
import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd=cwd,
            capture_output=True,
            text=True
        )
        print(f"✅ Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🎓 Offline AI Tutor Setup Script (Hugging Face Edition)")
    print("=" * 60)
    
    # Get project root
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    frontend_dir = project_root / "frontend"
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {python_version.major}.{python_version.minor}")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        node_version = result.stdout.strip()
        print(f"✅ Node.js {node_version} detected")
        
        # Check if Node.js version is 18+
        major_version = int(node_version.replace('v', '').split('.')[0])
        if major_version < 18:
            print("⚠️ Warning: Node.js 18+ is recommended for best compatibility")
            
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 18+ first.")
        print("📥 Download from: https://nodejs.org/")
        return False
    
    # Check system requirements
    print("\n💾 Checking system requirements...")
    
    # Check available memory
    try:
        if platform.system() == "Linux":
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
                total_memory = int([line for line in meminfo.split('\n') if 'MemTotal' in line][0].split()[1]) // 1024
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True)
            total_memory = int(result.stdout.strip()) // (1024 * 1024)
        elif platform.system() == "Windows":
            import psutil
            total_memory = psutil.virtual_memory().total // (1024 * 1024)
        else:
            total_memory = 8192  # Assume 8GB if can't detect
            
        print(f"💻 System RAM: {total_memory // 1024:.1f}GB")
        
        if total_memory < 4096:
            print("⚠️ Warning: Less than 4GB RAM detected. Model performance may be limited.")
        elif total_memory < 8192:
            print("⚠️ Warning: Less than 8GB RAM detected. Consider upgrading for optimal performance.")
        else:
            print("✅ Sufficient RAM for optimal performance")
            
    except Exception:
        print("⚠️ Could not detect system RAM. Ensure you have at least 8GB for optimal performance.")
    
    # Check GPU availability
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ NVIDIA GPU detected - will enable GPU acceleration")
        else:
            print("ℹ️ No NVIDIA GPU detected - will use CPU inference")
    except FileNotFoundError:
        print("ℹ️ No NVIDIA GPU detected - will use CPU inference")
    
    # Setup backend
    print("\n📦 Setting up Python backend with Hugging Face...")
    print("This will install the following key packages:")
    print("  - transformers==4.53.2")
    print("  - torch (latest)")
    print("  - fastapi + uvicorn")
    print("  - huggingface-hub")
    
    if not run_command("pip install -r requirements.txt", cwd=backend_dir):
        print("❌ Failed to install Python dependencies")
        print("💡 Try updating pip: python -m pip install --upgrade pip")
        return False
    
    # Verify transformers version
    try:
        import transformers
        print(f"✅ Transformers {transformers.__version__} installed")
        if transformers.__version__ != "4.53.2":
            print(f"⚠️ Warning: Expected transformers 4.53.2, but found {transformers.__version__}")
            print("This may cause compatibility issues with Gemma 3n E2B IT model")
    except ImportError:
        print("❌ Failed to import transformers")
        return False
    
    # Verify torch installation
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} installed")
        if torch.cuda.is_available():
            print(f"✅ CUDA {torch.version.cuda} available - GPU acceleration enabled")
        else:
            print("ℹ️ CUDA not available - using CPU inference")
    except ImportError:
        print("❌ Failed to import PyTorch")
        return False
    
    # Setup frontend
    print("\n🎨 Setting up Electron frontend...")
    print("This will install Electron and UI dependencies...")
    
    if not run_command("npm install", cwd=frontend_dir):
        print("❌ Failed to install Node.js dependencies")
        print("💡 Try clearing npm cache: npm cache clean --force")
        return False
    
    # Create .env file if it doesn't exist
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env file...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created from template")
        print("🔑 Please edit .env and add your Hugging Face token")
        print("🌐 Get your token at: https://huggingface.co/settings/tokens")
    elif env_file.exists():
        print("✅ .env file already exists")
    
    # Check Hugging Face token
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "your_hugging_face_token_here" in env_content or not any("HF_TOKEN=" in line and len(line.split("=")[1].strip()) > 10 for line in env_content.split("\n")):
                print("⚠️ Please update your Hugging Face token in .env file before running the app")
            else:
                print("✅ Hugging Face token appears to be configured")
    
    print("\n🎉 Setup completed successfully!")
    print("=" * 60)
    
    print("\n📚 Model Information:")
    print("- Model: google/gemma-3n-e2b-it")
    print("- Source: Hugging Face Hub")
    print("- Requires: Hugging Face token with Gemma access")
    print("- First run will download ~2-3GB model files")
    print("- Cached locally for offline use after download")
    
    print("\n🚀 Next steps:")
    print("1. Edit .env and add your Hugging Face token:")
    print("   HF_TOKEN=your_actual_token_here")
    print("2. Ensure you have accepted Gemma's license on Hugging Face:")
    print("   https://huggingface.co/google/gemma-3n-e2b-it")
    print("3. Start the application:")
    print("   cd frontend && npm start")
    print("4. Wait for model download on first run (one-time only)")
    print("5. Enjoy your Offline AI Tutor!")
    
    print("\n💡 Troubleshooting:")
    print("- If model download fails: Check HF token and model access")
    print("- If out of memory: Reduce batch size or use smaller model")
    print("- If slow performance: Enable GPU acceleration or add more RAM")
    print("- For support: Check README.md or GitHub issues")
    
    print("\n🔧 Development commands:")
    print("- Start backend only: cd backend && python app.py")
    print("- Start frontend only: cd frontend && npm run dev")
    print("- Run tests: python -m pytest backend/tests/")
    print("- Build for distribution: cd frontend && npm run build")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎓 Setup complete! Your Offline AI Tutor is ready to go!")
    else:
        print("\n❌ Setup failed. Please check the errors above and try again.")
    
    sys.exit(0 if success else 1)