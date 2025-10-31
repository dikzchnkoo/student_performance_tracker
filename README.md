# Student Performance Tracker (Rekap Nilai Mahasiswa)

Student Performance Tracker adalah sebuah aplikasi CLI (Command-Line Interface) sederhana yang dibangun dengan Python. Program ini berfungsi untuk memuat, mengelola, dan merekapitulasi data kehadiran serta nilai akademik mahasiswa dari beberapa file CSV.

Ini adalah proyek tugas untuk membangun aplikasi mini berbasis Object-Oriented Programming (OOP) yang kemudian disusun ulang menjadi paket modular.

## Fitur Utama

Program ini memiliki antarmuka berbasis menu yang memungkinkan pengguna untuk:

* **1. Muat Data dari CSV**: Mengimpor data secara massal dari `data/attendance.csv` (untuk kehadiran) dan `data/grades.csv` (untuk nilai).
* **2. Tambah/Ubah Mahasiswa**: Menambahkan data mahasiswa baru atau memperbarui nama mahasiswa yang sudah ada.
* **3. Ubah Presensi**: Mengubah data persentase kehadiran untuk mahasiswa tertentu berdasarkan NIM.
* **4. Ubah Nilai**: Mengubah rincian nilai (Quiz, Tugas, UTS, UAS) untuk mahasiswa tertentu.
* **5. Lihat Rekap (Terminal)**: Menampilkan tabel rekapitulasi performa semua mahasiswa (NIM, Nama, Hadir, Nilai Akhir, Predikat) langsung di terminal.
* **6. Simpan Laporan Markdown**: Mengekspor tabel rekapitulasi ke dalam sebuah file bernama `out/report.md`.
* **7. Keluar**: Menghentikan aplikasi.