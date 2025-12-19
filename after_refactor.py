from abc import ABC, abstractmethod
import logging

# KONFIGURASI LOGGING
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)
# ABSTRAKSI VALIDASI
class IValidationRule(ABC):
    """
    Interface untuk semua aturan validasi registrasi mahasiswa.
    """

    @abstractmethod
    def validate(self, student: dict) -> bool:
        """
        Melakukan validasi terhadap data mahasiswa.

        Args:
            student (dict): Data mahasiswa.

        Returns:
            bool: True jika valid, False jika tidak.
        """
        pass

# IMPLEMENTASI ATURAN VALIDASI
class SksLimitRule(IValidationRule):
    """
    Aturan validasi batas maksimal SKS.
    """

    def validate(self, student: dict) -> bool:
        """
        Mengecek apakah jumlah SKS melebihi batas.

        Args:
            student (dict): Data mahasiswa.

        Returns:
            bool: Hasil validasi SKS.
        """
        if student["sks"] > 24:
            logging.WARNING("Validasi SKS gagal: SKS melebihi batas.")
            return False

        logging.INFO("Validasi SKS berhasil.")
        return True


class PrasyaratRule(IValidationRule):
    """
    Aturan validasi kelulusan prasyarat.
    """

    def validate(self, student: dict) -> bool:
        """
        Mengecek status kelulusan prasyarat.

        Args:
            student (dict): Data mahasiswa.

        Returns:
            bool: Hasil validasi prasyarat.
        """
        if not student["prasyarat_lulus"]:
            logging.WARNING("Validasi prasyarat gagal: Prasyarat belum lulus.")
            return False

        logging.INFO("Validasi prasyarat berhasil.")
        return True

# SERVICE REGISTRASI
class RegistrationService:
    """
    Service untuk mengelola proses registrasi mahasiswa.
    """

    def __init__(self, rules: list[IValidationRule]):
        """
        Inisialisasi service dengan daftar aturan validasi.

        Args:
            rules (list[IValidationRule]): Daftar aturan validasi.
        """
        self.rules = rules

    def register(self, student: dict) -> bool:
        """
        Menjalankan proses registrasi mahasiswa.

        Args:
            student (dict): Data mahasiswa.

        Returns:
            bool: True jika registrasi berhasil, False jika gagal.
        """
        logging.INFO("Memulai proses registrasi mahasiswa.")

        for rule in self.rules:
            if not rule.validate(student):
                logging.WARNING("Registrasi mahasiswa gagal.")
                return False

        logging.INFO("Registrasi mahasiswa berhasil.")
        return True

# PROGRAM UTAMA
if __name__ == "__main__":
    student = {
        "sks": 22,
        "prasyarat_lulus": True
    }

    rules = [
        SksLimitRule(),
        PrasyaratRule()
    ]

    service = RegistrationService(rules)
    service.register(student)