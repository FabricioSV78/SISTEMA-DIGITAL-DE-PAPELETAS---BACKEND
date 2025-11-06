#!/usr/bin/env bash
# Start script para Render

echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT