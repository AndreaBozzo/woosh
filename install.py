#!/usr/bin/env python3
"""
Woosh - Unified installation script
"""
import subprocess
import sys
import os
from pathlib import Path

# Colors for output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}")
    print("  WOOSH - Installation")
    print(f"{'='*50}{Colors.END}\n")

def check_python():
    """Check Python version"""
    print(f"{Colors.YELLOW}Checking Python version...{Colors.END}")
    version = sys.version_info

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"{Colors.RED}❌ Python 3.8+ required (found {version.major}.{version.minor}){Colors.END}")
        return False

    print(f"{Colors.GREEN}✓ Python {version.major}.{version.minor}.{version.micro}{Colors.END}")
    return True

def check_node():
    """Check Node.js and npm"""
    print(f"{Colors.YELLOW}Checking Node.js and npm...{Colors.END}")

    # Determine npm command for Windows
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
    node_cmd = "node.exe" if os.name == 'nt' else "node"

    try:
        # Check Node.js
        node_result = subprocess.run(
            [node_cmd, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        node_version = node_result.stdout.strip()

        # Check npm
        npm_result = subprocess.run(
            [npm_cmd, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        npm_version = npm_result.stdout.strip()

        print(f"{Colors.GREEN}✓ Node.js {node_version}{Colors.END}")
        print(f"{Colors.GREEN}✓ npm {npm_version}{Colors.END}")
        return True

    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}❌ Node.js and npm are required{Colors.END}")
        print(f"{Colors.YELLOW}Download from: https://nodejs.org/{Colors.END}")
        return False

def install_backend():
    """Install backend dependencies"""
    print(f"\n{Colors.BLUE}[Backend]{Colors.END} Installing Python dependencies...")

    backend_dir = Path(__file__).parent / "woosh" / "backend"
    requirements = backend_dir / "requirements.txt"

    if not requirements.exists():
        print(f"{Colors.RED}❌ requirements.txt not found{Colors.END}")
        return False

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
            check=True,
            cwd=backend_dir
        )
        print(f"{Colors.GREEN}✓ Backend dependencies installed{Colors.END}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error installing backend dependencies{Colors.END}")
        return False

def install_frontend():
    """Install frontend dependencies"""
    print(f"\n{Colors.BLUE}[Frontend]{Colors.END} Installing Node.js dependencies...")

    frontend_dir = Path(__file__).parent / "woosh" / "frontend"
    package_json = frontend_dir / "package.json"

    if not package_json.exists():
        print(f"{Colors.RED}❌ package.json not found{Colors.END}")
        return False

    # Determine npm command for Windows
    npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"

    try:
        subprocess.run(
            [npm_cmd, "install"],
            check=True,
            cwd=frontend_dir
        )
        print(f"{Colors.GREEN}✓ Frontend dependencies installed{Colors.END}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error installing frontend dependencies{Colors.END}")
        return False

def main():
    print_header()

    # Check prerequisites
    if not check_python():
        return 1

    if not check_node():
        return 1

    print()  # Blank line

    # Install backend
    if not install_backend():
        print(f"\n{Colors.RED}Installation failed{Colors.END}\n")
        return 1

    # Install frontend
    if not install_frontend():
        print(f"\n{Colors.RED}Installation failed{Colors.END}\n")
        return 1

    # Success
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Installation completed successfully!{Colors.END}\n")
    print(f"  Run the application with: {Colors.BOLD}python start.py{Colors.END}\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
