#!/usr/bin/env python3
"""
Woosh - Quick start for frontend and backend
"""
import os
import subprocess
import sys
import time
from pathlib import Path


# Colors for output
class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"


def print_header():
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}")
    print("  WOOSH - Starting Application")
    print(f"{'='*50}{Colors.END}\n")


def check_dependencies():
    """Check if dependencies are installed"""
    print(f"{Colors.YELLOW}Checking dependencies...{Colors.END}")

    # Check backend
    backend_dir = Path(__file__).parent / "woosh" / "backend"
    if not (backend_dir / "requirements.txt").exists():
        print(f"{Colors.RED}❌ requirements.txt not found!{Colors.END}")
        return False

    # Check frontend
    frontend_dir = Path(__file__).parent / "woosh" / "frontend"
    if not (frontend_dir / "package.json").exists():
        print(f"{Colors.RED}❌ package.json not found!{Colors.END}")
        return False

    print(f"{Colors.GREEN}✓ Dependencies verified{Colors.END}\n")
    return True


def start_backend():
    """Start FastAPI backend"""
    print(
        f"{Colors.BLUE}[Backend]{Colors.END} Starting FastAPI server on http://localhost:8000..."
    )

    backend_dir = Path(__file__).parent / "woosh" / "backend"

    try:
        # Start uvicorn
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app:app", "--reload", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for server to be ready
        time.sleep(2)

        if process.poll() is None:  # Process still running
            print(f"{Colors.GREEN}✓ Backend started{Colors.END}")
            return process
        else:
            print(f"{Colors.RED}❌ Error starting backend{Colors.END}")
            return None

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        return None


def start_frontend():
    """Start Next.js frontend"""
    print(
        f"{Colors.BLUE}[Frontend]{Colors.END} Starting Next.js server on http://localhost:3000..."
    )

    frontend_dir = Path(__file__).parent / "woosh" / "frontend"

    try:
        # Determine appropriate npm command for Windows
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"

        # Start Next.js
        process = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for server to be ready
        time.sleep(3)

        if process.poll() is None:  # Process still running
            print(f"{Colors.GREEN}✓ Frontend started{Colors.END}")
            return process
        else:
            print(f"{Colors.RED}❌ Error starting frontend{Colors.END}")
            return None

    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        return None


def main():
    print_header()

    if not check_dependencies():
        print(f"\n{Colors.RED}Cannot start application.{Colors.END}")
        return 1

    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return 1

    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return 1

    # Information
    print(
        f"\n{Colors.GREEN}{Colors.BOLD}✓ Application started successfully!{Colors.END}\n"
    )
    print(f"  {Colors.BOLD}Frontend:{Colors.END} http://localhost:3000")
    print(f"  {Colors.BOLD}Backend API:{Colors.END} http://localhost:8000")
    print(f"  {Colors.BOLD}API Documentation:{Colors.END} http://localhost:8000/docs")
    print(f"\n{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}\n")

    try:
        # Keep processes running
        while True:
            time.sleep(1)

            # Check if processes are still running
            if backend_process.poll() is not None:
                print(f"\n{Colors.RED}Backend stopped unexpectedly{Colors.END}")
                break
            if frontend_process.poll() is not None:
                print(f"\n{Colors.RED}Frontend stopped unexpectedly{Colors.END}")
                break

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Shutting down application...{Colors.END}")

    finally:
        # Terminate processes
        print(f"{Colors.BLUE}Stopping backend...{Colors.END}")
        backend_process.terminate()

        print(f"{Colors.BLUE}Stopping frontend...{Colors.END}")
        frontend_process.terminate()

        # Wait for shutdown
        backend_process.wait(timeout=5)
        frontend_process.wait(timeout=5)

        print(f"{Colors.GREEN}✓ Application stopped{Colors.END}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
