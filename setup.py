#!/usr/bin/env python3
"""
Setup script for AIS Parquet Query project.
This script creates a virtual environment and installs all required dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, shell=True):
    """Run a command and handle errors."""
    try:
        result = subprocess.run(command, shell=shell, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {command}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")

def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    result = run_command(f"{sys.executable} -m venv venv")
    if result:
        print("✓ Virtual environment created successfully")
        return True
    return False

def get_activation_command():
    """Get the correct activation command based on the operating system."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def get_pip_command():
    """Get the correct pip command for the virtual environment."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip"
    else:
        return "venv/bin/pip"

def get_python_command():
    """Get the correct python command for the virtual environment."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\python"
    else:
        return "venv/bin/python"

def upgrade_pip():
    """Upgrade pip in the virtual environment."""
    print("Upgrading pip...")
    pip_cmd = get_pip_command()
    result = run_command(f"{pip_cmd} install --upgrade pip")
    if result:
        print("✓ Pip upgraded successfully")
        return True
    return False

def install_requirements():
    """Install requirements from requirements.txt."""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("Installing requirements...")
    pip_cmd = get_pip_command()
    result = run_command(f"{pip_cmd} install -r requirements.txt")
    if result:
        print("✓ Requirements installed successfully")
        return True
    return False

def install_jupyter_kernel():
    """Install Jupyter kernel for the virtual environment."""
    print("Installing Jupyter kernel...")
    python_cmd = get_python_command()
    result = run_command(f"{python_cmd} -m ipykernel install --user --name=ais_parquet_query --display-name='AIS Parquet Query'")
    if result:
        print("✓ Jupyter kernel installed successfully")
        return True
    return False

def main():
    """Main setup function."""
    print("🚀 Setting up AIS Parquet Query project...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Upgrade pip
    if not upgrade_pip():
        print("❌ Failed to upgrade pip")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    # Install Jupyter kernel
    install_jupyter_kernel()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    print(f"   {get_activation_command()}")
    print("\n2. Start Jupyter Lab:")
    print("   jupyter lab")
    print("\n3. Open parquet_query.ipynb and start querying!")
    print("\n4. Configure your AWS credentials (see README.md for details)")
    
    if platform.system() != "Windows":
        print(f"\n💡 Quick start command:")
        print(f"   {get_activation_command()} && jupyter lab")

if __name__ == "__main__":
    main()
