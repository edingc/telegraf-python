FROM telegraf:latest

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 \
  python3-requests \
  python3-urllib3 \
  && rm -rf /var/lib/apt/lists/*
