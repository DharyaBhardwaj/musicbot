FROM python:3.10-slim

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---- install nodejs (REQUIRED FOR pytgcalls) ----
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# ---- workdir ----
WORKDIR /app

# ---- python deps ----
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- copy code ----
COPY . .

# ---- run ----
CMD ["python", "bot.py"]
