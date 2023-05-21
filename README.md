# Substation Planning Service
REST API Service untuk Substation dengan FastAPI. Python dan FastAPI dibutuhkan untuk menjalankan service ini.

## Cara menjalankan
Pada terminal, jalankan:

```
cd src
uvicorn main:app
```

## Milestone API
- [x] available-gardu-induk: menampilkan nama gardu induk existing
- [ ] posisi-gardu-induk-existing: menampilkan posisi gardu induk existing
- [ ] memberi rekomendasi GD baru nyambung ke GI mana
- [ ] kerapatan paling bagus berapa? (terkait dengan kapasitas daya GI)
- [ ] penentuan GI berdasarkan peningkatan GD
  - [ ] lokasi dimana
  - [ ] luas area GI baru
  - [ ] berapa jarak ke GI lama
  - [ ] GD mana nyambung ke GI baru atau lama
  - [ ] GI baru tidak terlalu jauh dari 150 kV line
  - [ ] letak GI berdasarkan cost dan jarak, (perlu disiapkan variable pengali untuk cost)
- [x] Area pelayanan GI (m2)
- [ ] jumlah-gardu-distribusi: Total titik beban pergardu induk
- [ ] Total rekap titik beban (MW/MVA)
- [ ] Kerapatan GI
    - [ ] Beban (MW/MVA)/ m2
    - [ ] Kapasitas Trafo GD (KVA)/ m2
    - [ ] Jumlah Pelanggan / m2
    - [ ] Kapasitas Tersambung Pelanggan (kVA) / m2
