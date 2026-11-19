# PROMPT-GALERI-MOBIL

Demo Vibe Engineering: Galery Mobil (Pembelian Mobil Online)

Aplikasi: web untuk memilih mobil, memilih type, lalu melihat total harga. Fitur 1: Hitung Harga (satu mobil). Fitur 2: Pesanan (beberapa mobil sekaligus, dengan cek stok).

## Babak 1: Vibe coding (±20 menit)

Tool: ANTIGRAVITY

```text
Bikinin galeri mobil berbasis web. Pelanggan memilih nama mobil, memilih
type-nya, dan mengisi jumlah unit. Tampilkan harga satuan, diskon, total
harga, dan sisa stok.
```

## Tahap 0: Scaffold proyek (tanpa CI)

Tool: ANTIGRAVITY

```text
Di folder ini: inisialisasi git dengan branch main, jalankan `uv init
--python 3.12`, tambahkan dependency `fastapi[standard]` serta dev
dependency pytest, pytest-cov, httpx dengan `uv add`. Buat `.gitignore`
untuk Python (.venv, __pycache__, .pytest_cache, .coverage, htmlcov,
.env). JANGAN membuat folder .github atau workflow CI. Commit dengan
pesan "chore: scaffold awal tanpa CI", lalu buat repo GitHub publik
bernama "Galery-Mobil-By-Syyou" dan push branch main ke sana dengan `gh`.
```

## Tahap 1: Memahami masalah

Tool: GEMINI

```text
[P] Persona: Bertindaklah sebagai pembeli yang akan memesan mobil secara online.

[K] Konteks: Kita akan membuat Galery Mobil berbasis web untuk pelanggan
pembeli online. Input: nama mobil yang akan dibeli, type/varian yang
dipilih, dan jumlah unit. Output: harga satuan, diskon, dan total harga
mobil yang dipilih, serta sisa stok. Ada dua fitur: (1) hitung harga satu
mobil, (2) pesanan berisi beberapa mobil sekaligus. Kebenaran hasilnya
harus bisa dinilai guru tanpa membaca kode.

[T] Tugas: Bantu saya mendaftar semua kasus pembelian yang harus ditangani,
baik untuk hitung harga satu mobil maupun pesanan beberapa mobil
(termasuk stok tersedia, stok habis, jumlah melebihi stok, mobil atau type
yang tidak ada, jumlah tidak valid, dan pemesanan mobil yang sama dua kali
dalam satu pesanan). Untuk tiap kasus, tandai apakah jawabannya pasti
(bisa dijadikan test) atau perlu keputusan manusia (misalnya aturan
diskon, batas jumlah per pesanan, dan apakah stok habis ditolak atau
ditawarkan pre-order). JANGAN menulis kode apa pun.

[F] Format: Tabel dengan kolom: kasus, input, hasil yang diharapkan,
dan status (pasti / perlu keputusan).
```

## Tahap 2: Spesifikasi (SPEC.md)

Tool: GEMINI, MANUSIA

```text
[P] Persona: Bertindaklah sebagai dealer mobil yang menjual beberapa mobil
dengan beberapa type masing-masing.

[K] Konteks: Lanjutkan dari daftar kasus pembelian mobil ini.
Aplikasi: Galery Mobil berbasis web, dengan backend Python 3.12 + FastAPI
dan satu halaman HTML. Logika perhitungan berada di `main.py`; test
berada di `test_main.py` (pytest).

[T] Tugas: Tulis dokumen SPEC.md (JANGAN menulis kode aplikasi) yang
memuat keputusan berikut:

1. Katalog (data tetap di `main.py`, harga dalam Rupiah bilangan bulat,
   sudah termasuk pajak):

   | Mobil          | Type     | Harga (Rp)  | Stok |
   |----------------|----------|-------------|------|
   | Toyota Avanza  | E        | 245.000.000 | 5    |
   | Toyota Avanza  | G        | 265.000.000 | 5    |
   | Toyota Avanza  | Veloz    | 285.000.000 | 3    |
   | Honda Brio     | S        | 175.000.000 | 6    |
   | Honda Brio     | E        | 195.000.000 | 4    |
   | Honda Brio     | RS       | 215.000.000 | 0    |
   | Mitsubishi Xpander | GLS      | 255.000.000 | 4 |
   | Mitsubishi Xpander | Exceed   | 275.000.000 | 4 |
   | Mitsubishi Xpander | Ultimate | 300.000.000 | 1 |

2. `hitung_harga(mobil: str, tipe: str, jumlah: int) -> dict` dengan
   kunci: mobil, tipe, harga_satuan, jumlah, subtotal, diskon, total,
   stok_tersisa.
   - Nama mobil dan type dicocokkan tanpa membedakan huruf besar/kecil;
     spasi di awal dan akhir diabaikan.
   - Jumlah valid: bilangan bulat 1-10.
   - subtotal = harga_satuan x jumlah.
   - Diskon armada: 5% dari subtotal bila jumlah >= 3, selain itu 0.
     Hitung dengan bilangan bulat: diskon = subtotal * 5 // 100.
   - total = subtotal - diskon.
   - stok_tersisa = stok - jumlah.
   - Raise ValueError bila: mobil atau type tidak ada di katalog, jumlah
     bukan bilangan bulat 1-10, stok habis, atau jumlah melebihi stok.
3. `buat_pesanan(items: list[dict]) -> dict`
   - Tiap item berisi: mobil, tipe, jumlah.
   - Pesanan diproses berurutan; tiap item dihitung dengan aturan
     `hitung_harga`. Bila mobil dan type yang sama muncul lebih dari
     sekali, jumlahnya DIAKUMULASI terhadap stok (misalnya dua item
     Avanza Veloz x2 berarti butuh 4 unit).
   - Hasil: {"items": [hasil hitung_harga tiap item], "total_pesanan":
     jumlah semua total}.
   - Raise ValueError bila: daftar item kosong, ada item yang tidak
     valid, atau stok tidak cukup untuk keseluruhan pesanan.
4. Endpoint: GET /api/katalog (daftar mobil, type, harga, stok),
   GET /api/harga?mobil=&tipe=&jumlah=, POST /api/pesanan (body JSON:
   items), dan GET / untuk halaman index.html. Kesalahan input
   menghasilkan HTTP 400 dengan field "detail".
5. Halaman web: satu halaman dengan dua mode (Hitung Harga dan Pesanan),
   pilihan mobil dan type berupa dropdown dari katalog, harga tampil
   dalam format Rupiah, menampilkan hasil dan pesan error yang jelas.
6. Tabel test case lengkap, memakai tabel dasar berikut:
   - Toyota Avanza G x1 -> harga satuan 265.000.000, diskon 0,
     total 265.000.000, stok tersisa 4
   - Honda Brio E x2 -> subtotal 390.000.000, diskon 0,
     total 390.000.000
   - Mitsubishi Xpander Exceed x3 -> subtotal 825.000.000,
     diskon 41.250.000, total 783.750.000
   - Mitsubishi Xpander Ultimate x1 -> total 300.000.000,
     stok tersisa 0
   - "toyota avanza" "g" x1 (huruf kecil) -> diterima, sama dengan
     Avanza G
   - Honda Brio RS x1 -> ditolak (stok habis)
   - Toyota Avanza Veloz x4 -> ditolak (melebihi stok 3)
   - Mobil "Ferrari", type tidak ada ("Avanza Z"), jumlah 0, jumlah -1,
     jumlah 11, jumlah "abc", mobil kosong -> ditolak
   - Pesanan [Avanza G x1, Brio S x2] -> total_pesanan 615.000.000
   - Pesanan [Avanza Veloz x2, Avanza Veloz x2] -> ditolak (akumulasi 4
     melebihi stok 3)
   - Pesanan kosong -> ditolak

[F] Format: Markdown yang siap saya simpan sebagai SPEC.md, dengan
bagian: Tujuan, Katalog, Aturan Validasi, Kontrak Fungsi, Kontrak API,
Halaman Web, Tabel Test Case, Di Luar Cakupan (pembayaran, kredit/cicilan,
login, dan pre-order).
```

## Tahap 3: Desain UI

Tool: STITCH

```text
[Persona] You are a UI designer for e-commerce and car showroom websites.

[Context] A web page for buying cars online ("Galery Mobil"), used by
customers who browse a small catalog. Style: clean, minimalist, light
mode, Google-like (white background, soft gray text, blue accent,
rounded cards). Prices are shown in Indonesian Rupiah (Rp 265.000.000).

[Task] Design one responsive page with two tabs: "Hitung Harga" and
"Pesanan". Hitung Harga tab: a car dropdown, a type dropdown (filtered
by the selected car), a quantity field (1-10), a "Hitung" button, and a
result card listing unit price, quantity, subtotal, discount, total
price, and remaining stock. Pesanan tab: a list of order items (car,
type, quantity) the user can add or remove, a "Buat Pesanan" button, and
a result table with a grand total. Include three states: empty, success,
and error (clear error message under the field, e.g. "Stok habis").

[Format] Desktop and mobile layouts. Export-ready HTML/CSS.
```

## Tahap 2b: Issue dan branch

Tool: ANTIGRAVITY

```text
Baca SPEC.md. Buat dokumen `issues/1-issue_hitung_harga.md` berisi:
Deskripsi, Tugas, Kriteria Penerimaan (merujuk tabel test di SPEC.md),
dan Alur Kerja (issue -> branch -> test dulu -> implementasi -> commit ->
pull request -> CI -> merge). Lalu buat GitHub Issue dari dokumen itu
dengan `gh issue create --title "[Feature] Hitung Harga Mobil" --body-file
issues/1-issue_hitung_harga.md --label feature` (buat label jika
belum ada). Catat nomor issue-nya, lalu buat branch dari main dengan
nama `feature/issue-<nomor>-hitung-harga`. Commit SPEC.md,
index.html, DESIGN.md, dan folder issues/ sebagai satu commit dengan
pesan "docs: spesifikasi dan desain UI".
```

## Tahap 4: Test dulu (fase merah)

Tool: ANTIGRAVITY

```text
Baca SPEC.md. Tulis test lebih dulu, JANGAN implementasi:

1. Buat `test_main.py` dengan pytest dan `pytest.mark.parametrize`,
   mencakup semua kasus hitung harga dan API di tabel test SPEC.md
   (kasus normal, diskon armada, stok tersisa, huruf kecil, stok habis,
   melebihi stok, input tidak valid, GET /api/katalog dan
   GET /api/harga sukses, GET /api/harga mengembalikan 400 untuk input
   tidak valid, dan GET / mengembalikan 200). Kasus pesanan belum dibuat
   sekarang.
2. Ganti isi `main.py` dengan kerangka saja: `app = FastAPI()`, data
   katalog sesuai SPEC.md, dan fungsi `hitung_harga` yang hanya
   `raise NotImplementedError`.
3. Jalankan `uv run pytest` dan tunjukkan bahwa test GAGAL (merah).
4. JANGAN membuat folder .github atau workflow CI.
5. Commit dengan pesan "test: tulis test hitung harga lebih dulu".
```

## Tahap 5: Implementasi

Tool: ANTIGRAVITY

```text
Implementasikan `hitung_harga` dan endpoint di `main.py` sesuai
SPEC.md, hubungkan `index.html` ke endpoint API (isi dropdown dari
/api/katalog, tampilkan hasil dan pesan error dari field `detail`),
lalu jalankan `uv run pytest` sampai SEMUA test lulus.

Aturan:
- DILARANG mengubah `test_main.py` agar test lulus. Bila menurut Anda
  sebuah test salah, berhenti dan jelaskan alasannya kepada saya.
- Hitung semua uang dengan bilangan bulat (int), jangan float. Diskon
  dihitung dengan `subtotal * 5 // 100`.
- Setelah selesai, jalankan server (`uv run fastapi dev main.py`) dan
  pastikan halaman tampil dan terhubung ke API.
- Commit dengan pesan "feat: implementasi hitung_harga dan API".
```

## Tahap 6: Review dan verifikasi

Tool: ANTIGRAVITY, MANUSIA

```text
Jelaskan fungsi `hitung_harga` baris per baris untuk guru: tunjukkan
bagian yang mencari mobil dan type di katalog, bagian validasi jumlah dan
stok, bagian yang menghitung subtotal, bagian yang menghitung diskon
armada, dan bagian yang menghitung total serta sisa stok. Hubungkan
dengan contoh nyata (misalnya Xpander Exceed x3 menjadi Rp 783.750.000).
Sebutkan juga bila ada asumsi atau keputusan yang tidak ada di SPEC.md.
Jangan mengubah kode.
```

## Tahap 7: Git, CI, dan Pull Request

Tool: ANTIGRAVITY

```text
Buat file `.github/workflows/ci.yml` dengan isi PERSIS seperti berikut:

name: SQA Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run Unit Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v7

      - name: Install uv
        uses: astral-sh/setup-uv@v10.3.3
        with:
          enable-cache: true

      - name: Install Dependencies
        run: uv sync --dev

      - name: Run Tests with Coverage
        run: uv run pytest test_main.py -v --cov=main --cov-report=term-missing

Lalu: commit dengan pesan "ci: tambah pipeline setelah test ada", push branch ini, buka Pull Request ke main (deskripsi memuat "Closes #<nomor issue>"), pantau CI dengan `gh pr checks --watch` sampai hijau, lalu merge Pull Request tersebut. Jangan mengubah test agar CI hijau.
```

## Tahap 8: Fitur Pesanan (beberapa mobil)

Tool: ANTIGRAVITY

```text
Kerjakan fitur Pesanan sesuai SPEC.md dengan alur lengkap yang sama:
1. Buat `issues/2-issue_pesanan.md` dari SPEC.md, buat GitHub Issue-nya
   (label feature), lalu buat branch `feature/issue-<nomor>-pesanan` dari
   main terbaru.
2. Tulis test pesanan LEBIH DULU di `test_main.py` (tambahkan ke file yang
   ada), buat kerangka `buat_pesanan` dan endpoint POST /api/pesanan yang
   belum diimplementasikan, jalankan pytest dan tunjukkan test merah,
   lalu commit.
3. Implementasikan sampai semua test lulus (DILARANG mengubah test
   agar lulus), hubungkan tab Pesanan di index.html, lalu commit.
4. Push, buka Pull Request ke main ("Closes #<nomor>"), pantau CI sampai
   hijau, lalu merge.
```

## Tahap 9: Docker (membungkus aplikasi menjadi container)

Tool: ANTIGRAVITY, DOCKER

```text
Kemas aplikasi ini dengan Docker. Kerjakan berurutan:
1. Jalankan `docker version`. Bila bagian Server tidak muncul atau ada error
   koneksi, berhenti dan minta saya menyalakan Docker Desktop. Jangan
   mencoba memasang Docker sendiri.
2. Pastikan di `main` terbaru dan bersih (git switch main, git pull,
   git status), lalu buat branch `chore/docker`.
3. Buat `Dockerfile` di root dengan isi PERSIS seperti berikut:

    # Image dasar: Python 3.12 versi ramping
    FROM python:3.12-slim

    # Salin program uv dari image resminya (versi dikunci agar hasil build selalu sama)
    COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

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

4. Buat `.dockerignore` dengan isi PERSIS:

    .venv/
    .git/
    .github/
    __pycache__/
    .pytest_cache/
    .coverage
    htmlcov/
    .env

5. Buat `scripts/smoke_test.py` dengan isi PERSIS seperti di bawah
   (jangan diubah):

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
                # server belum siap: koneksi ditolak, terputus, atau habis waktu
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
        base = sys.argv[1]
        gagal = 0
        for nama, fungsi in PEMERIKSAAN:
            try:
                fungsi(base)
                print(f"[LULUS] {nama}")
            except Exception as e:  # noqa: BLE001
                gagal += 1
                print(f"[GAGAL] {nama}: {e}")
        print(f"Ringkasan: {len(PEMERIKSAAN) - gagal} lulus, {gagal} gagal")
        return 1 if gagal else 0


    if __name__ == "__main__":
        sys.exit(main())

6. Build dan jalankan: `docker build -t galery-mobil .`, lalu
   `docker run -d --name galery-app -p 8000:8000 galery-mobil`
   (bila port 8000 masih dipakai server lama, hentikan dulu memakai
   PID-nya), `docker ps`, lalu smoke test
   `uv run python scripts/smoke_test.py http://127.0.0.1:8000`
   (semua harus lulus). Setelah itu `docker rm -f galery-app`.
7. Ganti isi `.github/workflows/ci.yml` dengan isi PERSIS berikut
   (job baru `docker` berjalan setelah job `test` hijau):

    name: SQA Pipeline

    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]

    jobs:
      test:
        name: Run Unit Tests
        runs-on: ubuntu-latest

        steps:
          - name: Checkout Code
            uses: actions/checkout@v7

          - name: Install uv
            uses: astral-sh/setup-uv@v10.3.3
            with:
              enable-cache: true

          - name: Install Dependencies
            run: uv sync --dev

          - name: Run Tests with Coverage
            run: uv run pytest test_main.py -v --cov=main --cov-report=term-missing

      docker:
        name: Build and Smoke Test Container
        runs-on: ubuntu-latest
        needs: test

        steps:
          - name: Checkout Code
            uses: actions/checkout@v7

          - name: Build Image
            run: docker build -t galery-mobil .

          - name: Run Container
            run: docker run -d --name galery-app -p 8000:8000 galery-mobil

          - name: Smoke Test Container
            env:
              SMOKE_PERCOBAAN: "10"
              SMOKE_JEDA: "3"
            run: python3 scripts/smoke_test.py http://127.0.0.1:8000

          - name: Show Container Logs on Failure
            if: failure()
            run: docker logs galery-app

8. Tambahkan bagian `## Docker` ke README.md: perintah build, perintah
   run, dan cara menjalankan smoke test ke container lokal.
9. Pastikan pytest masih hijau, commit "build: kemas aplikasi dengan
   Docker dan smoke test container", push, buka Pull Request ke main
   (tanpa "Closes"), pantau CI sampai KEDUA job hijau, lalu merge.
   Jangan mengubah test maupun skrip smoke test.
```

## Tahap 10: Deploy ke Vercel dan smoke test

Tool: MANUSIA, VERCEL, ANTIGRAVITY

### 10a. Periksa kesiapan

Tool: ANTIGRAVITY

```text
Siapkan deploy ke Vercel. Pastikan di `main` terbaru dan bersih, lalu periksa
dan laporkan satu per satu:
- `main.py` ada di root dan memuat variabel `app`.
- `.python-version` berisi 3.12, dan `uv.lock` sudah di-commit.
- `index.html` dan `scripts/smoke_test.py` ada di `main`.
- Tidak ada rahasia (token, kunci, .env) di repo.
- Run CI terakhir di main hijau untuk job `test` dan `docker`
  (`gh run list --branch main --limit 1`).

Lalu berhenti dan tunggu saya. Saya akan mengimpor repo di Vercel dan memberi
Anda URL produksi. JANGAN membuat akun atau login ke Vercel.
```

### 10c. Smoke test di URL produksi

Tool: ANTIGRAVITY

```text
Berikut URL produksi: <URL>. Jalankan
`uv run python scripts/smoke_test.py <URL>` dan tunggu sampai selesai.

- Bila ada [GAGAL]: analisis akar masalah dulu dan tunjukkan analisisnya.
  Bila perlu log, minta saya menempelkan Build Logs atau Runtime Logs dari
  dashboard Vercel. Perbaiki KODE APLIKASI saja, jangan ubah test maupun
  skrip smoke test, lewat branch dan Pull Request baru. Setelah merge Vercel
  men-deploy ulang; jalankan smoke test lagi.
- Bila semua [LULUS]: tambahkan bagian `## Deploy` di README.md (URL dan cara
  smoke test) lewat branch `docs/url-produksi` dan Pull Request kecil, tunggu CI
  hijau, lalu merge.
- Tunjukkan keluaran smoke test dan URL produksi di akhir.
```
