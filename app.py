# app.py

import sys
import os
import csv
# Impor dari paket 'tracker' yang sudah kita buat
from tracker import RekapKelas, build_markdown_report, save_text

# Inisialisasi objek manajer rekap utama
rekap_data = RekapKelas()

# --- MODIFIKASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.csv')
GRADES_FILE = os.path.join(DATA_DIR, 'grades.csv')


# --- FUNGSI INI DIPERBARUI AGAR SESUAI PERMINTAAN ANDA ---
def muat_data_csv():
    """
    Memuat data mahasiswa dan nilai dari file CSV di folder 'data/'.
    (Versi Ringkasan Sederhana)
    """
    print("Memuat data dari CSV... Mohon tunggu...")
    
    # Inisialisasi counter untuk ringkasan
    count_hadir = 0
    count_nilai = 0
    count_peringatan_nilai = 0
    
    try:
        # 1. Muat data mahasiswa dan kehadiran
        with open(ATTENDANCE_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Panggil fungsi "senyap"
                rekap_data.tambah_mahasiswa(row['nim'], row['nama']) 
                rekap_data.set_hadir(row['nim'], float(row['hadir_persen']))
                count_hadir += 1
        
        # 2. Muat data nilai
        with open(GRADES_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nim = row['nim']
                if nim in rekap_data.data_mahasiswa:
                    # Panggil fungsi "senyap"
                    rekap_data.set_penilaian(
                        nim, 
                        float(row['quiz']), 
                        float(row['tugas']), 
                        float(row['uts']), 
                        float(row['uas'])
                    )
                    count_nilai += 1
                else:
                    # Tampilkan peringatan langsung jika ada
                    print(f"Peringatan: NIM {nim} di {os.path.basename(GRADES_FILE)} tidak ada di {os.path.basename(ATTENDANCE_FILE)}.")
                    count_peringatan_nilai += 1
                    
        # --- INI ADALAH OUTPUT YANG ANDA MINTA ---
        print("\nProses Selesai.")
        print(f"Berhasil memuat dan memproses {count_hadir} data kehadiran dari {os.path.basename(ATTENDANCE_FILE)}.")
        print(f"Berhasil memuat dan mengatur {count_nilai} data nilai dari {os.path.basename(GRADES_FILE)}.")
        if count_peringatan_nilai > 0:
             print(f"(Total {count_peringatan_nilai} peringatan ditemukan.)")

    except FileNotFoundError as e:
        print(f"\nError: File tidak ditemukan. Pastikan file berikut ada:")
        print(f"1. {ATTENDANCE_FILE}")
        print(f"2. {GRADES_FILE}")
    except KeyError as e:
        print(f"\nError: Kolom CSV tidak sesuai. Pastikan header file CSV benar (Kolom hilang: {e})")
    except Exception as e:
        print(f"\nTerjadi error saat memuat data: {e}")

# --- FUNGSI MENU LAINNYA DISESUAIKAN UNTUK KEMBALI PRINT ---

def menu_tambah_mahasiswa():
    """Tampilkan menu untuk menambah mahasiswa."""
    print("-- Tambah Mahasiswa --")
    nim = input("Masukkan NIM: ")
    nama = input("Masukkan Nama: ")
    
    # Tambahkan print di sini karena 'tambah_mahasiswa' senyap
    if nim not in rekap_data.data_mahasiswa:
        rekap_data.tambah_mahasiswa(nim, nama)
        print(f"Mahasiswa {nama} (NIM: {nim}) berhasil ditambahkan.")
    else:
        rekap_data.tambah_mahasiswa(nim, nama)
        print(f"Data nama untuk NIM {nim} berhasil diperbarui menjadi {nama}.")

def menu_ubah_presensi():
    """Tampilkan menu untuk mengubah presensi."""
    print("-- Ubah Presensi --")
    nim = input("Masukkan NIM mahasiswa: ")
    try:
        persen = float(input("Masukkan persentase kehadiran (0-100): "))
        
        # Tambahkan print di sini
        if nim in rekap_data.data_mahasiswa:
            rekap_data.set_hadir(nim, persen)
            nama = rekap_data.data_mahasiswa[nim]['mhs'].nama
            print(f"Kehadiran {nama} diubah ke {persen}%.")
        else:
            print(f"Error: NIM {nim} tidak ditemukan.")
            
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
        # Tambahkan print di sini
        nama = rekap_data.data_mahasiswa[nim]['mhs'].nama
        print(f"Nilai untuk {nama} berhasil diubah.")
        
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
        
    print(f"{'NIM':<12} | {'Nama':<10} | {'Hadir (%)':<10} | {'Nilai Akhir':<12} | {'Predikat':<8}")
    print("-" * 68)
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
    path = os.path.join(BASE_DIR, "out", "report.md")
    save_text(path, content)

# --- FUNGSI MENU UTAMA & LOOP (TETAP SAMA) ---
def tampilkan_menu_utama():
    """Menampilkan menu CLI utama."""
    print("\n" + "===" * 10)
    print("   Student Performance Tracker   ")
    print("===" * 10)
    print("1) Muat data dari CSV")
    print("2) Tambah/Ubah mahasiswa")
    print("3) Ubah presensi")
    print("4) Ubah nilai")
    print("5) Lihat rekap (Terminal)")
    print("6) Simpan laporan Markdown")
    print("7) Keluar")
    return input("Pilih menu (1-7): ") 

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
        elif pilihan == '7':
            print("Terima kasih telah menggunakan program ini.")
            sys.exit()
        else:
            print("Pilihan tidak valid. Silakan masukkan angka 1-7.")

if __name__ == "__main__":
    main()