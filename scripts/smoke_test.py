"""Smoke test (smoke test) untuk Galery Mobil yang sudah berjalan.

Pemakaian:
    uv run python scripts/smoke_test.py <URL dasar>
Contoh:
    uv run python scripts/smoke_test.py http://127.0.0.1:8000

Keluar dengan kode 0 bila semua pemeriksaan lulus, 1 bila ada yang gagal.
Kesalahan sementara (server belum siap atau cold start) dicoba ulang beberapa kali.
"""

import http.client
import json
import os
import sys
import time
import urllib.error
import urllib.request

PERCOBAAN = int(os.environ.get("SMOKE_PERCOBAAN", "6"))
JEDA_DETIK = int(os.environ.get("SMOKE_JEDA", "15"))


def minta(base, path, metode="GET", isi=None):
    url = base.rstrip("/") + path
    data = None
    header = {}
    if isi is not None:
        data = json.dumps(isi).encode("utf-8")
        header["Content-Type"] = "application/json"
    terakhir = (0, "")
    for percobaan in range(1, PERCOBAAN + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=header, method=metode)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            terakhir = (e.code, e.read().decode("utf-8", "replace"))
            if e.code < 500:
                return terakhir
        except (OSError, http.client.HTTPException) as e:
            terakhir = (0, str(e))
        if percobaan < PERCOBAAN:
            time.sleep(JEDA_DETIK)
    return terakhir


def cek_halaman(base):
    status, teks = minta(base, "/")
    assert status == 200, f"status {status}, seharusnya 200"
    assert "<html" in teks.lower(), "isi bukan halaman HTML"


def cek_harga(base):
    status, teks = minta(base, "/api/harga?mobil=Mitsubishi%20Xpander&tipe=Exceed&jumlah=3")
    assert status == 200, f"status {status}, seharusnya 200"
    hasil = json.loads(teks)
    assert hasil["subtotal"] == 825000000, f"subtotal {hasil['subtotal']}"
    assert hasil["diskon"] == 41250000, f"diskon {hasil['diskon']}"
    assert hasil["total"] == 783750000, f"total {hasil['total']}"


def cek_input_invalid(base):
    status, _ = minta(base, "/api/harga?mobil=Ferrari&tipe=X&jumlah=1")
    assert status == 400, f"status {status}, seharusnya 400"


def cek_pesanan(base):
    isi = {
        "items": [
            {"mobil": "Toyota Avanza", "tipe": "G", "jumlah": 1},
            {"mobil": "Honda Brio", "tipe": "S", "jumlah": 2},
        ]
    }
    status, teks = minta(base, "/api/pesanan", "POST", isi)
    assert status == 200, f"status {status}, seharusnya 200"
    hasil = json.loads(teks)
    assert hasil["total_pesanan"] == 615000000, f"total_pesanan {hasil['total_pesanan']}"


PEMERIKSAAN = [
    ("Halaman utama (GET /)", cek_halaman),
    ("Harga Xpander Exceed x3 (diskon armada)", cek_harga),
    ("Input tidak valid ditolak (400)", cek_input_invalid),
    ("Pesanan Avanza G x1 + Brio S x2", cek_pesanan),
]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    gagal = 0
    for nama, fungsi in PEMERIKSAAN:
        try:
            fungsi(sys.argv[1])
            print(f"[LULUS] {nama}")
        except Exception as e:  # noqa: BLE001
            gagal += 1
            print(f"[GAGAL] {nama}: {e}")
    print(f"Ringkasan: {len(PEMERIKSAAN) - gagal} lulus, {gagal} gagal")
    return 1 if gagal else 0


if __name__ == "__main__":
    sys.exit(main())
