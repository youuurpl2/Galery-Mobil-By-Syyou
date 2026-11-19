# SPEC - Galery Mobil

## Tujuan
Aplikasi web untuk memilih mobil, memilih type, menghitung harga, diskon, total, dan stok. Mendukung perhitungan satu mobil serta pesanan beberapa mobil.

## Katalog
Data tetap disimpan di `main.py`. Semua harga Rupiah bilangan bulat dan sudah termasuk pajak.

| Mobil | Type | Harga (Rp) | Stok |
|---|---|---:|---:|
| Toyota Avanza | E | 245.000.000 | 5 |
| Toyota Avanza | G | 265.000.000 | 5 |
| Toyota Avanza | Veloz | 285.000.000 | 3 |
| Honda Brio | S | 175.000.000 | 6 |
| Honda Brio | E | 195.000.000 | 4 |
| Honda Brio | RS | 215.000.000 | 0 |
| Mitsubishi Xpander | GLS | 255.000.000 | 4 |
| Mitsubishi Xpander | Exceed | 275.000.000 | 4 |
| Mitsubishi Xpander | Ultimate | 300.000.000 | 1 |

## Aturan Validasi
- Nama mobil dan type dicocokkan case-insensitive dan spasi tepi diabaikan.
- Jumlah harus integer 1-10.
- Diskon armada 5% bila jumlah >= 3.
- Diskon dihitung `subtotal * 5 // 100`.
- Pesanan diproses berurutan.
- Item dengan mobil dan type sama dijumlahkan untuk validasi stok keseluruhan.
- Stok habis atau pesanan melebihi stok ditolak.
- Daftar pesanan kosong atau item tidak valid ditolak.

## Kontrak Fungsi
### `hitung_harga(mobil: str, tipe: str, jumlah: int) -> dict`
Mengembalikan kunci `mobil`, `tipe`, `harga_satuan`, `jumlah`, `subtotal`, `diskon`, `total`, dan `stok_tersisa`.
Mengembalikan `stok_tersisa = stok - jumlah`.

### `buat_pesanan(items: list[dict]) -> dict`
Mengembalikan `{"items": [...], "total_pesanan": total}`.

## Kontrak API
- `GET /api/katalog`: daftar katalog.
- `GET /api/harga?mobil=&tipe=&jumlah=`: hasil perhitungan.
- `POST /api/pesanan`: body JSON `{"items": [...]}`.
- `GET /`: halaman `index.html`.
- Kesalahan input mengembalikan HTTP 400 dengan field `detail`.

## Halaman Web
Satu halaman dengan tab **Hitung Harga** dan **Pesanan**. Pilihan mobil dan type berasal dari katalog. Harga ditampilkan dalam Rupiah. Terdapat state kosong, sukses, dan error.

## Tabel Test Case
| Kasus | Hasil |
|---|---|
| Toyota Avanza G x1 | satuan 265.000.000, diskon 0, total 265.000.000, stok tersisa 4 |
| Honda Brio E x2 | subtotal 390.000.000, diskon 0, total 390.000.000 |
| Mitsubishi Xpander Exceed x3 | subtotal 825.000.000, diskon 41.250.000, total 783.750.000 |
| Mitsubishi Xpander Ultimate x1 | total 300.000.000, stok tersisa 0 |
| `toyota avanza`, `g`, x1 | diterima sama dengan Avanza G |
| Honda Brio RS x1 | ditolak stok habis |
| Toyota Avanza Veloz x4 | ditolak melebihi stok |
| Ferrari, Avanza Z, jumlah 0/-1/11/abc, mobil kosong | ditolak |
| Pesanan Avanza G x1 + Brio S x2 | total 615.000.000 |
| Dua Avanza Veloz x2 | ditolak akumulasi 4 melebihi stok 3 |
| Pesanan kosong | ditolak |

## Di Luar Cakupan
Pembayaran, kredit/cicilan, login, dan pre-order.
