# Stage 1: Build environment with conda-pack
FROM continuumio/miniconda3:latest as builder

WORKDIR /build

# Install conda-pack
RUN conda install -c conda-forge conda-pack

# Copy environment file
COPY environment.yml .

# Create environment
RUN conda env create -f environment.yml && \
    conda clean -afy

# Pack environment for transfer
RUN conda-pack -n mlops_production -o /tmp/env.tar && \
    mkdir /venv && \
    cd /venv && \
    tar xf /tmp/env.tar && \
    rm /tmp/env.tar

# Fix paths in the packed environment
RUN /venv/bin/conda-unpack

# Stage 2: Lightweight runtime
FROM debian:bullseye-slim

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy packed environment
COPY --from=builder /venv /venv

# Copy application
COPY --chown=appuser:appuser . .

# Create directories
RUN mkdir -p notebooks/executed data/input data/output data/monitoring models/trained && \
    chown -R appuser:appuser notebooks data models

# Set environment
ENV PATH=/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

CMD ["gunicorn", "main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "300", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
