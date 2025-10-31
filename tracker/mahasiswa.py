# tracker/mahasiswa.py

class Mahasiswa:
    """
    Mewakili seorang mahasiswa dengan data dasar dan persentase kehadiran.
    """

    def __init__(self, nim, nama):
        """
        Inisialisasi objek Mahasiswa.

        Args:
            nim (str): Nomor Induk Mahasiswa.
            nama (str): Nama lengkap mahasiswa.
        """
        self.nim = nim
        self.nama = nama
        self._hadir_persen = 0  # Atribut privat untuk kehadiran

    @property
    def hadir_persen(self):
        """
        Mendapatkan nilai persentase kehadiran.
        """
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, nilai):
        """
        Mengatur nilai persentase kehadiran dengan validasi 0-100.
        """
        if 0 <= nilai <= 100:
            self._hadir_persen = nilai
        else:
            print(f"Error: Persentase kehadiran ({nilai}) harus antara 0 dan 100.")

    def info(self):
        """
        Menampilkan profil singkat mahasiswa.
        """
        return f"NIM: {self.nim}, Nama: {self.nama}, Kehadiran: {self.hadir_persen}%"