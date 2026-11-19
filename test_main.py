import pytest
from fastapi.testclient import TestClient

from main import app, buat_pesanan, hitung_harga

client = TestClient(app)


@pytest.mark.parametrize(
    ("mobil", "tipe", "jumlah", "expected"),
    [
        ("Toyota Avanza", "G", 1, {"harga_satuan": 265000000, "diskon": 0, "total": 265000000, "stok_tersisa": 4}),
        ("Honda Brio", "E", 2, {"subtotal": 390000000, "diskon": 0, "total": 390000000}),
        ("Mitsubishi Xpander", "Exceed", 3, {"subtotal": 825000000, "diskon": 41250000, "total": 783750000}),
        ("Mitsubishi Xpander", "Ultimate", 1, {"total": 300000000, "stok_tersisa": 0}),
        (" toyota avanza ", " g ", 1, {"harga_satuan": 265000000, "diskon": 0, "total": 265000000}),
    ],
)
def test_hitung_harga_normal(mobil, tipe, jumlah, expected):
    result = hitung_harga(mobil, tipe, jumlah)
    for key, value in expected.items():
        assert result[key] == value


@pytest.mark.parametrize(
    ("mobil", "tipe", "jumlah"),
    [
        ("Honda Brio", "RS", 1),
        ("Toyota Avanza", "Veloz", 4),
        ("Ferrari", "X", 1),
        ("Toyota Avanza", "Avanza Z", 1),
        ("Toyota Avanza", "G", 0),
        ("Toyota Avanza", "G", -1),
        ("Toyota Avanza", "G", 11),
        ("Toyota Avanza", "G", "abc"),
        ("", "G", 1),
    ],
)
def test_hitung_harga_invalid(mobil, tipe, jumlah):
    with pytest.raises(ValueError):
        hitung_harga(mobil, tipe, jumlah)


def test_katalog_api():
    response = client.get("/api/katalog")
    assert response.status_code == 200
    assert len(response.json()) == 9


@pytest.mark.parametrize(
    ("query", "status"),
    [
        ("mobil=Toyota%20Avanza&tipe=G&jumlah=1", 200),
        ("mobil=Honda%20Brio&tipe=RS&jumlah=1", 400),
        ("mobil=Toyota%20Avanza&tipe=Veloz&jumlah=4", 400),
        ("mobil=Ferrari&tipe=X&jumlah=1", 400),
        ("mobil=Toyota%20Avanza&tipe=G&jumlah=abc", 400),
        ("mobil=&tipe=G&jumlah=1", 400),
    ],
)
def test_harga_api(query, status):
    response = client.get("/api/harga?" + query)
    assert response.status_code == status
    if status == 400:
        assert "detail" in response.json()


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()


def test_buat_pesanan():
    result = buat_pesanan([
        {"mobil": "Toyota Avanza", "tipe": "G", "jumlah": 1},
        {"mobil": "Honda Brio", "tipe": "S", "jumlah": 2},
    ])
    assert result["total_pesanan"] == 615000000


def test_buat_pesanan_duplicate_over_stock():
    with pytest.raises(ValueError):
        buat_pesanan([
            {"mobil": "Toyota Avanza", "tipe": "Veloz", "jumlah": 2},
            {"mobil": "Toyota Avanza", "tipe": "Veloz", "jumlah": 2},
        ])


@pytest.mark.parametrize("items", [[], None, [{}], [{"mobil": "Ferrari", "tipe": "X", "jumlah": 1}]])
def test_buat_pesanan_invalid(items):
    with pytest.raises(ValueError):
        buat_pesanan(items)


def test_pesanan_api():
    response = client.post("/api/pesanan", json={"items": [
        {"mobil": "Toyota Avanza", "tipe": "G", "jumlah": 1},
        {"mobil": "Honda Brio", "tipe": "S", "jumlah": 2},
    ]})
    assert response.status_code == 200
    assert response.json()["total_pesanan"] == 615000000
