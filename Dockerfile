# Image dasar: Python 3.12 versi ramping
FROM python:3.12-slim

LABEL org.opencontainers.image.title="PUNYA SYOU LIAN"

RUN python -m pip install --no-cache-dir uv==0.11.32

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Pasang dependency dulu (lapisan ini di-cache selama uv.lock tidak berubah)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

# Salin kode aplikasi
COPY main.py index.html ./

# Layanan hosting biasanya mengisi variabel PORT; di laptop dipakai 8000
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "/app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
