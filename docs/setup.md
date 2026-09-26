# Setup & Installation Guide

## Prerequisites
- Python 3.11+
- Node.js v18+ and npm
- SWI-Prolog (optional for Phase 1 pure engine, required for Phase 2 SWI backend)
- Git

## Installation

### 1. Backend Setup
```bash
# Clone the repository
git clone <repo-url>
cd Neuro_project

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and set your credentials:
```bash
cp .env.example .env
```
Default local settings use `LLM_PROVIDER=mock` which allows full local testing without requiring external API keys.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Running Backend
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Running Tests
```bash
pytest
```
