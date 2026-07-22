FROM python:3.12.7-slim@sha256:1c44018d7eb40488f29e7c6ad4991d3200507e14dca71b94fe61011815e98155

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log
