# notebook-deployment-monitor
Deploy Jupyter notebooks using FastAPI, Monitoring with Prometheus and CI/CD

# ML Prediction API - MLOps Production System

A production-ready MLOps system that executes Jupyter notebooks via API, provides real-time predictions, monitors data drift, and supports automated model retraining.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Components Explained](#components-explained)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Testing](#testing)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Monitoring](#monitoring)
- [When to Modify Components](#when-to-modify-components)
- [Deployment](#deployment)

## 🏗️ Architecture Overview

┌──────────────┐
│ FastAPI │ ◄── HTTP Requests
│ (api.py) │
└──────┬───────┘
│
▼
┌─────────────────────┐
│ PredictionService │
│ (services/) │
└──────┬──────────────┘
│
▼
┌─────────────────────┐
│ NotebookExecutor │
│ (Papermill) │
└──────┬──────────────┘
│
▼
┌─────────────────────┐
│ Jupyter Notebook │ ◄── Your ML Model
│ (model_pipeline) │
└─────────────────────┘
│
▼
┌─────────────────────┐
│ Predictions │
│ (JSON output) │
└─────────────────────┘

Monitoring: Prometheus ◄──► Drift Monitor (Evidently AI)


## 🔍 Components Explained

### Core Files

| File | Purpose | When to Modify |
|------|---------|----------------|
| **main.py** | Application entry point, starts FastAPI server | Rarely. Only for app-level configs |
| **api.py** | API routes and endpoints | Add new endpoints here |
| **config/settings.py** | All configuration variables | Change paths, timeouts, thresholds |
| **models/schemas.py** | Request/response data models | Modify when API contract changes |

### Service Layer

| Component | Purpose | When to Modify |
|-----------|---------|----------------|
| **services/notebook_executor.py** | Executes notebooks via Papermill | Rarely. Core logic stable |
| **services/prediction_service.py** | Business logic for predictions | Change when prediction workflow changes |
| **services/drift_monitor.py** | Monitors data drift with Evidently | Customize drift thresholds, metrics |

### Monitoring

| Component | Purpose | When to Modify |
|-----------|---------|----------------|
| **monitoring/metrics.py** | Prometheus metrics definitions | Add custom metrics here |

### Your ML Notebook

| File | Purpose | When to Modify |
|------|---------|----------------|
| **notebooks/model_pipeline.ipynb** | **YOUR ML MODEL CODE** | **This is where YOUR model lives!** |

**Key Points:**
- This notebook contains your actual ML model
- Must have a `parameters` cell for Papermill
- Takes input: CSV file path
- Produces output: JSON predictions file

## 📦 Prerequisites

- Python 3.10+
- Conda (recommended) or pip
- Docker (for containerized deployment)
- Git

## 🚀 Installation

### Option 1: Conda (Recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd mlops_project

# Create environment
conda env create -f environment.yml
conda activate mlops_production

# Verify installation
python -c "import fastapi, papermill, evidently; print('All dependencies installed!')"
