# =========================
# Base Python Image
# =========================
FROM python:3.10-slim

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# Copy requirements
# =========================
COPY requirements.txt .

# =========================
# Install Python deps
# =========================
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Copy bot files
# =========================
COPY . .

# =========================
# Start bot
# =========================
CMD ["python", "bot.py"]
