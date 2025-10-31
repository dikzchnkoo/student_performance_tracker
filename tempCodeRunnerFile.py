# app.py

import sys
import os
import csv
# Impor dari paket 'tracker' yang sudah kita buat
from tracker import RekapKelas, build_markdown_report, save_text

# Inisialisasi objek manajer rekap utama
rekap_data = RekapKelas()

# --- MODIFIKASI PATH ---
# Dapatkan path absolut dari folder tempat app.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tentukan path ke file data menggunakan path absolut
DATA_DIR = os.path.join(BASE_DIR, 'data')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.csv')
GRADES_FILE = os.path.join(DATA_DIR, 'grades.csv')


def muat_data_csv():
    """
    Memuat data mahasiswa dan nilai dari file CSV di folder 'data/'.
    """
    print("Memuat data dari CSV...")
    # Kosongkan data lama sebelum memuat yang baru
    # rekap_data.data_mahasiswa.clear()
    # print("Data lama (jika ada) telah dibersihkan.")
    
    try:
        # 1. Muat data mahasiswa dan kehadiran
        with open(ATTENDANCE_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nim = row['nim']
                nama = row['nama']
                hadir = float(row['hadir_persen'])
                
                rekap_data.tambah_mahasiswa(nim, nama)
                rekap_data.set_hadir(nim, hadir)
        
        print(f"Berhasil memuat data kehadiran dari {ATTENDANCE_FILE}")

        # 2. Muat data nilai
        with open(GRADES_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nim = row['nim']
                quiz = float(row['quiz'])
                tugas = float(row['tugas'])
                uts = float(row['uts'])
                uas = float(row['uas'])
                
                if nim in rekap_data.data_mahasiswa:
                    rekap_data.set_penilaian(nim, quiz, tugas, uts, uas)
                else:
                    print(f"Peringatan: NIM {nim} di file nilai tidak ada di file kehadiran.")
                    
        print(f"Berhasil memuat data nilai dari {GRADES_FILE}")
        print("Data CSV berhasil dimuat.")

    except FileNotFoundError as e:
        print(f"Error: File tidak ditemukan. Pastikan file berikut ada:")
        print(f"1. {ATTENDANCE_FILE}")
        print(f"2. {GRADES_FILE}")
    except KeyError as e:
        print(f"Error: Kolom CSV tidak sesuai. Pastikan header file CSV benar (Kolom hilang: {e})")
    except Exception as e:
        print(f"Terjadi error saat memuat data: {e}")

# --- FUNGSI BARU (Menu 7) ---

def menu_tambah_mahasiswa():
    """Tampilkan menu untuk menambah mahasiswa."""
    print("-- Tambah Mahasiswa --")
    nim = input("Masukkan NIM: ")
    nama = input("Masukkan Nama: ")
    rekap_data.tambah_mahasiswa(nim, nama)

def menu_ubah_presensi():
    """Tampilkan menu untuk mengubah presensi."""
    print("-- Ubah Presensi --")
    nim = input("Masukkan NIM mahasiswa: ")
    try:
        persen = float(input("Masukkan persentase kehadiran (0-100): "))
        rekap_data.set_hadir(nim, persen)
    except ValueError:
        print("Input tidak valid, masukkan angka.")
    except Exception as e:
        print(f"Terjadi error: {e}")

def menu_ubah_nilai():
    """Tampilkan menu untuk mengubah nilai."""
    print("-- Ubah Nilai --")
    nim = input("Masukkan NIM mahasiswa: ")
    if nim not in rekap_data.data_mahasiswa:
        print(f"Error: NIM {nim} tidak ditemukan.")
        return
        
    try:
        quiz = float(input("Masukkan nilai Quiz (0-100): "))
        tugas = float(input("Masukkan nilai Tugas (0-100): "))
        uts = float(input("Masukkan nilai UTS (0-100): "))
        uas = float(input("Masukkan nilai UAS (0-100): "))
        rekap_data.set_penilaian(nim, quiz, tugas, uts, uas)
    except ValueError:
        print("Input tidak valid, masukkan angka.")
    except Exception as e:
        print(f"Terjadi error: {e}")

def menu_lihat_rekap():
    """Tampilkan rekap dalam bentuk tabel sederhana di terminal."""
    print("-- Lihat Rekap Terminal --")
    records = rekap_data.rekap()
    if not records:
        print("Belum ada data mahasiswa.")
        return
        
    # Header
    print(f"{'NIM':<12} | {'Nama':<10} | {'Hadir (%)':<10} | {'Nilai Akhir':<12} | {'Predikat':<8}")
    print("-" * 68)
    # Data
    for r in records:
        print(f"{r['nim']:<12} | {r['nama']:<10} | {r['hadir']:<10.1f} | {r['nilai_akhir']:<12.2f} | {r['predikat']:<8}")

def menu_simpan_laporan():
    """Hasilkan dan simpan laporan ke out/report.md."""
    print("-- Simpan Laporan Markdown --")
    records = rekap_data.rekap()
    if not records:
        print("Belum ada data untuk dilaporkan.")
        return
        
    content = build_markdown_report(records)
    path = os.path.join(BASE_DIR, "out", "report.md")  # Menggunakan path absolut
    save_text(path, content)

# --- FUNGSI DIPERBARUI (Menu) ---
def tampilkan_menu_utama():
    """Menampilkan menu CLI utama."""
    print("\n" + "===" * 10)
    print("   Student Performance Tracker   ")
    print("===" * 10)
    print("1) Muat data dari CSV (File .txt)")
    print("2) Tambah mahasiswa")
    print("3) Ubah presensi")
    print("4) Ubah nilai")
    print("5) Lihat rekap (Terminal)")
    print("6) Simpan laporan Markdown")
    print("7) Keluar")             # <-- DIPINDAH
    return input("Pilih menu (1-8): ") # <-- DIPERBARUI

# --- FUNGSI DIPERBARUI (Loop Utama) ---
def main():
    """Loop utama program CLI."""
    while True:
        pilihan = tampilkan_menu_utama()
        
        if pilihan == '1':
            muat_data_csv() 
        elif pilihan == '2':
            menu_tambah_mahasiswa()
        elif pilihan == '3':
            menu_ubah_presensi()
        elif pilihan == '4':
            menu_ubah_nilai()
        elif pilihan == '5':
            menu_lihat_rekap()
        elif pilihan == '6':
            menu_simpan_laporan()
        elif pilihan == '7':            # <-- DIPINDAH
            print("Terima kasih telah menggunakan program ini.")
            sys.exit()
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1-8.") # <-- DIPERBARUI

if __name__ == "__main__":
    main()