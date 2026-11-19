# Galery Mobil

Aplikasi web jual beli mobil berbasis FastAPI dan halaman HTML responsif.

## Menjalankan Lokal

```bash
uv sync
uv run fastapi dev main.py
```

Buka `http://127.0.0.1:8000`.

## Docker

Build image:

```bash
docker build -t galery-mobil .
```

Jalankan container:

```bash
docker run -d --name galery-app -p 8000:8000 galery-mobil
```

Jalankan smoke test:

```bash
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```