# KODE SEBELUM REFACTORING
class ValidatorManager:  # Melanggar SRP, OCP, DIP
    def validate(self, student):
        # Validasi SKS (digabung dalam satu class)
        if student["sks"] > 24:
            return False, "SKS melebihi batas"

        # Validasi Prasyarat (tanggung jawab ganda)
        elif not student["prasyarat_lulus"]:
            return False, "Prasyarat belum lulus"

        # Semua logika di satu method
        else:
            return True, "Registrasi berhasil"

# PROGRAM UTAMA
student = {
    "sks": 22,
    "prasyarat_lulus": True
}

manager = ValidatorManager()
status, message = manager.validate(student)
print(message)