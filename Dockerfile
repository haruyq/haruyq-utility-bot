FROM python:3.10-slim

WORKDIR /haruyq-util-bot

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]