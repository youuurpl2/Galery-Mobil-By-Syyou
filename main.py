from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

app = FastAPI(title="Galery Mobil")

KATALOG = [
    {"mobil": "Toyota Avanza", "tipe": "E", "harga": 245000000, "stok": 5},
    {"mobil": "Toyota Avanza", "tipe": "G", "harga": 265000000, "stok": 5},
    {"mobil": "Toyota Avanza", "tipe": "Veloz", "harga": 285000000, "stok": 3},
    {"mobil": "Honda Brio", "tipe": "S", "harga": 175000000, "stok": 6},
    {"mobil": "Honda Brio", "tipe": "E", "harga": 195000000, "stok": 4},
    {"mobil": "Honda Brio", "tipe": "RS", "harga": 215000000, "stok": 0},
    {"mobil": "Mitsubishi Xpander", "tipe": "GLS", "harga": 255000000, "stok": 4},
    {"mobil": "Mitsubishi Xpander", "tipe": "Exceed", "harga": 275000000, "stok": 4},
    {"mobil": "Mitsubishi Xpander", "tipe": "Ultimate", "harga": 300000000, "stok": 1},
]


def _teks(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Mobil atau type tidak valid")
    return value.strip().lower()


def hitung_harga(mobil: str, tipe: str, jumlah: int) -> dict:
    if not isinstance(jumlah, int) or isinstance(jumlah, bool) or not 1 <= jumlah <= 10:
        raise ValueError("Jumlah harus bilangan bulat antara 1 sampai 10")

    cocok = None
    for item in KATALOG:
        if _teks(item["mobil"]) == _teks(mobil) and _teks(item["tipe"]) == _teks(tipe):
            cocok = item
            break

    if cocok is None:
        raise ValueError("Mobil atau type tidak ada di katalog")
    if cocok["stok"] == 0:
        raise ValueError("Stok habis")
    if jumlah > cocok["stok"]:
        raise ValueError("Jumlah melebihi stok tersedia")

    subtotal = cocok["harga"] * jumlah
    diskon = subtotal * 5 // 100 if jumlah >= 3 else 0
    total = subtotal - diskon

    return {
        "mobil": cocok["mobil"],
        "tipe": cocok["tipe"],
        "harga_satuan": cocok["harga"],
        "jumlah": jumlah,
        "subtotal": subtotal,
        "diskon": diskon,
        "total": total,
        "stok_tersisa": cocok["stok"] - jumlah,
    }


def buat_pesanan(items: list[dict]) -> dict:
    if not isinstance(items, list) or not items:
        raise ValueError("Daftar pesanan tidak boleh kosong")

    akumulasi = {}
    for item in items:
        if not isinstance(item, dict) or not {"mobil", "tipe", "jumlah"}.issubset(item):
            raise ValueError("Ada item pesanan yang tidak valid")

        mobil = item["mobil"]
        tipe = item["tipe"]
        jumlah = item["jumlah"]
        if not isinstance(jumlah, int) or isinstance(jumlah, bool):
            raise ValueError("Jumlah harus bilangan bulat antara 1 sampai 10")

        kunci = (_teks(mobil), _teks(tipe))
        akumulasi[kunci] = akumulasi.get(kunci, 0) + jumlah

    for (mobil, tipe), jumlah in akumulasi.items():
        hitung_harga(mobil, tipe, jumlah)

    hasil_items = [hitung_harga(item["mobil"], item["tipe"], item["jumlah"]) for item in items]
    total_pesanan = sum(item["total"] for item in hasil_items)
    return {"items": hasil_items, "total_pesanan": total_pesanan}


@app.get("/api/katalog")
def api_katalog():
    return [
        {"mobil": item["mobil"], "tipe": item["tipe"], "harga": item["harga"], "stok": item["stok"]}
        for item in KATALOG
    ]


@app.get("/api/harga")
def api_harga(
    mobil: str = Query(...),
    tipe: str = Query(...),
    jumlah: str = Query(...),
):
    try:
        jumlah_int = int(jumlah)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="Jumlah harus bilangan bulat antara 1 sampai 10")
    try:
        return hitung_harga(mobil, tipe, jumlah_int)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/api/pesanan")
def api_pesanan(body: dict):
    try:
        items = body.get("items") if isinstance(body, dict) else None
        return buat_pesanan(items)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
def homepage():
    return Path("index.html").read_text(encoding="utf-8")
