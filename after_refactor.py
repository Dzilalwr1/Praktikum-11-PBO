from abc import ABC, abstractmethod

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

# Abstraksi Validator (DIP)
class Validator(ABC):
    @abstractmethod
    def validate(self, student):
        pass

# Implementasi Validator (SRP)
class SKSValidator(Validator):
    def validate(self, student):
        if student["sks"] > 24:
            return False, "SKS melebihi batas"
        return True, "SKS valid"

class PrasyaratValidator(Validator):
    def validate(self, student):
        if not student["prasyarat_lulus"]:
            return False, "Prasyarat belum lulus"
        return True, "Prasyarat valid"

# Service Registrasi (High-Level Module)
class RegistrationService:
    def __init__(self, validators):
        self.validators = validators  # Dependency Injection

    def register(self, student):
        for validator in self.validators:
            print(f"Menjalankan {validator.__class__.__name__}...")
            status, message = validator.validate(student)
            if not status:
                return False, message
        return True, "Registrasi berhasil"

# Chalenge (OCP)
class IPKValidator(Validator):
    def validate(self, student):
        if student["ipk"] < 2.75:
            return False, "IPK tidak mencukupi"
        return True, "IPK valid"


# Main Program
student = {
    "sks": 22,
    "prasyarat_lulus": True,
    "ipk": 3.2
}

validators = [
    SKSValidator(),
    PrasyaratValidator(),
    IPKValidator()
]

service = RegistrationService(validators)
status, message = service.register(student)
print(message)