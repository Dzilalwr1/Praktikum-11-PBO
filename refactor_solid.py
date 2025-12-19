from abc import ABC, abstractmethod
from dataclasses import dataclass

# Model Sederhana
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# === KODE BURUK (SEBELUM REFACTORING) ===
class OrderManager: # Melanggar SRP, OCP, DIP [cite: 717]
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}...")

        # LOGIKA PEMBAYARAN (Pelanggaran OCP/DIP) [cite: 754]
        if payment_method == "credit_card":
            # Logika detail implementasi hardcore di sini
            print("Processing Credit Card...")
        elif payment_method == "bank_transfer":
            # Logika detail implementasi hardcore di sini
            print("Processing Bank Transfer...")
        else:
            print("Metode tidak valid.")
            return False

        # LOGIKA NOTIFIKASI (Pelanggaran SRP) [cite: 763]
        print(f"Mengirim notifikasi ke {order.customer_name}...")
        order.status = "paid"
        return True
    
# --- ABSTRAKSI (Kontrak untuk OCP/DIP) ---
class IPaymentProcessor(ABC): # [cite: 776]
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC): # [cite: 780]
    @abstractmethod
    def send(self, order: Order):
        pass

# --- IMPLEMENTASI KONKRIT (Plug-in) ---
class CreditCardProcessor(IPaymentProcessor): # [cite: 785]
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService): # [cite: 788]
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# --- KELAS KOORDINATOR (SRP & DIP) ---
class CheckoutService: # Tanggung jawab tunggal: Mengkoordinasi Checkout [cite: 791]
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        # Dependency Injection: Bergantung pada Abstraksi, bukan Konkrit [cite: 820]
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        payment_success = self.payment_processor.process(order) # Delegasi 1 [cite: 824]

        if payment_success:
            order.status = "paid"
            self.notifier.send(order) # Delegasi 2 [cite: 827]
            print("Checkout Sukses.")
            return True
        return False
    
# === PROGRAM UTAMA ===
# 1. Setup Data dan Dependencies
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# 2. Skenario 1: Menggunakan Credit Card
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service) # [cite: 851]
print("--- Skenario 1: Credit Card ---")
checkout_cc.run_checkout(andi_order)

# 3. Skenario 2: Pembuktian OCP (Menambah QRIS tanpa mengubah kode utama)
class QrisProcessor(IPaymentProcessor): # [cite: 853]
    def process(self, order: Order) -> bool:
        print("Payment: Memproses QRIS.")
        return True

budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service) # [cite: 869]
print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
checkout_qris.run_checkout(budi_order)