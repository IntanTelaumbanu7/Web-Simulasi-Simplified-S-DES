# Web Simulasi S-DES Flask

Project ini adalah aplikasi web simulasi Simplified Data Encryption Standard (S-DES) menggunakan Flask.

## Fitur
- Input plaintext/ciphertext 8-bit.
- Input key 10-bit.
- Mode enkripsi dan dekripsi.
- Output bit dalam kotak visual.
- Solusi penyelesaian step-by-step: P10, LS-1, P8/K1, LS-2, P8/K2, IP, Round 1, Swap, Round 2, IP^-1.
- Tampilan rapi, responsif, dan modern.

## Cara Menjalankan
```bash
pip install -r requirements.txt
python app.py
```
Buka browser:
```text
http://127.0.0.1:5000
```

## Contoh Uji
Enkripsi:
- Plaintext: `00101000`
- Key: `1100011110`
- Ciphertext: `10001010`

Dekripsi:
- Ciphertext: `10001010`
- Key: `1100011110`
- Plaintext: `00101000`
