# tracker/penilaian.py

class Penilaian:
    """
    Mewakili data penilaian seorang mahasiswa (quiz, tugas, uts, uas).
    """

    def __init__(self, nim):
        """
        Inisialisasi objek Penilaian untuk NIM terkait.
        """
        self.nim = nim
        self._quiz = 0
        self._tugas = 0
        self._uts = 0
        self._uas = 0

    def _validasi_nilai(self, nilai):
        """Helper privat untuk memvalidasi nilai antara 0-100."""
        if 0 <= nilai <= 100:
            return nilai
        else:
            print(f"Error: Nilai ({nilai}) harus antara 0 dan 100. Diatur ke 0.")
            return 0

    # Properti untuk setiap komponen nilai
    @property
    def quiz(self):
        return self._quiz

    @quiz.setter
    def quiz(self, nilai):
        self._quiz = self._validasi_nilai(nilai)

    @property
    def tugas(self):
        return self._tugas

    @tugas.setter
    def tugas(self, nilai):
        self._tugas = self._validasi_nilai(nilai)

    @property
    def uts(self):
        return self._uts

    @uts.setter
    def uts(self, nilai):
        self._uts = self._validasi_nilai(nilai)

    @property
    def uas(self):
        return self._uas

    @uas.setter
    def uas(self, nilai):
        self._uas = self._validasi_nilai(nilai)

    def nilai_akhir(self):
        """
        Menghitung nilai akhir berdasarkan bobot:
        Quiz (15%), Tugas (25%), UTS (25%), UAS (35%)
        """
        return (self._quiz * 0.15) + (self._tugas * 0.25) + (self._uts * 0.25) + (self._uas * 0.35)