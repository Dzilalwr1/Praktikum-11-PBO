# Latihan Refactoring Struktur Kode Menggunakan Prinsip SOLID

## Studi Kasus
Validasi registrasi mahasiswa berdasarkan:
1. Jumlah SKS
2. Status kelulusan prasyarat

---

## Pelanggaran Prinsip SOLID

### 1. Single Responsibility Principle (SRP)
Class ValidatorManager memiliki lebih dari satu tanggung jawab,
yaitu memvalidasi SKS dan memvalidasi prasyarat mahasiswa.
Seharusnya setiap jenis validasi berada pada class terpisah.

### 2. Open/Closed Principle (OCP)
Jika ingin menambahkan validasi baru (misalnya IPK),
maka method validate harus diubah.
Artinya class tidak tertutup terhadap perubahan.

### 3. Dependency Inversion Principle (DIP)
ValidatorManager bergantung langsung pada detail implementasi validasi,
bukan pada abstraksi.
Tidak ada interface atau dependency injection.

---

## Kesimpulan
Kode awal sulit dikembangkan dan tidak fleksibel terhadap perubahan.
Oleh karena itu dilakukan refactoring menggunakan prinsip SOLID.
