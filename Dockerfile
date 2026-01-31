FROM python:3.10-slim

WORKDIR /app

# System deps
RUN apt update && apt install -y \
    ffmpeg \
    git \
    curl \
    nodejs \
    npm

# Node 18 (required by pytgcalls)
RUN npm install -g n && n 18

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
