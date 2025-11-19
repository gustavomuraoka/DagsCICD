FROM python:3.11-slim

ENV TZ="America/Sao_Paulo"

# System dependencies: Java, procps, build-essential, certs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      openjdk-21-jre-headless \
      procps \
      ca-certificates \
      build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set stable JAVA_HOME symlink
RUN set -eux; \
    JH="$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")"; \
    ln -sf "$JH" /usr/lib/jvm/default-java
ENV JAVA_HOME=/usr/lib/jvm/default-java

WORKDIR /app

# Install Python dependencies
COPY src/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy business logic code into the image
COPY src/ ./src

# Optionally: expose main scripts/entrypoints at root level for easy task calling
COPY dags/ ./dags
