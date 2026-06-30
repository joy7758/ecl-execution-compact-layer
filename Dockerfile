FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends git make \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python3 -m pip install --no-cache-dir -e .

CMD ["make", "demo"]
