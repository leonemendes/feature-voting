FROM node:18

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @anthropic-ai/claude-code

WORKDIR /workspace

COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt || true

COPY frontend/package.json .
RUN npm install

VOLUME ["/workspace"]

CMD [ "bash" ]