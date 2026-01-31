FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y \
    ffmpeg \
    curl \
    nodejs \
    npm

RUN npm install -g n
RUN n 18

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh
CMD ["bash", "start.sh"]
