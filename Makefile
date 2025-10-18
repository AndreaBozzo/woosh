.PHONY: help install dev start clean test lint format

help:  ## Show this help message
	@echo "Woosh - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies
	@echo "Installing dependencies..."
	@python install.py

dev:  ## Start development servers (frontend + backend)
	@echo "Starting development servers..."
	@python start.py

start: dev  ## Alias for dev

clean:  ## Clean build artifacts and caches
	@echo "Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@rm -rf woosh/frontend/.next 2>/dev/null || true
	@rm -rf build dist *.egg-info 2>/dev/null || true
	@echo "Clean complete!"

test:  ## Run tests
	@echo "Running tests..."
	@cd woosh/backend && python -m pytest tests/ -v

lint:  ## Run linters
	@echo "Running linters..."
	@cd woosh/backend && python -m ruff check . || true
	@cd woosh/frontend && npm run lint || true

format:  ## Format code
	@echo "Formatting code..."
	@cd woosh/backend && python -m black . || true
	@cd woosh/backend && python -m isort . || true
	@cd woosh/frontend && npm run format || true

backend:  ## Start only backend
	@echo "Starting backend..."
	@cd woosh/backend && python -m uvicorn app:app --reload --port 8000

frontend:  ## Start only frontend
	@echo "Starting frontend..."
	@cd woosh/frontend && npm run dev

build-frontend:  ## Build frontend for production
	@echo "Building frontend..."
	@cd woosh/frontend && npm run build

install-backend:  ## Install only backend dependencies
	@echo "Installing backend dependencies..."
	@cd woosh/backend && pip install -r requirements.txt

install-frontend:  ## Install only frontend dependencies
	@echo "Installing frontend dependencies..."
	@cd woosh/frontend && npm install
