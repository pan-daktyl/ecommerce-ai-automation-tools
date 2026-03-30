# --- ecommerce-ai-automation-tools/erp_store_sync_simulator.py ---
import json
import time

# --- SYMULACJA SYSTEMÓW ---

class ErpSystemSimulator:
    """Symuluje system ERP Subiekt Nexo Pro przez API."""
    def __init__(self):
        # Dane demo: SKU -> {Nazwa, Stan, Cena}
        self._database = {
            "ZKW-MOS-1": {"name": "Zawór Kulowy MOSIĘŻNY 1\" CAL", "stock": 150, "price_net": 35.50},
            "CZU-CIS-10": {"name": "Czujnik Ciśnienia 0-10 bar", "stock": 45, "price_net": 120.00},
            "POM-WOD-25": {"name": "Pompa Wody obiegowa DN25", "stock": 5, "price_net": 450.00}
        }

    def get_stock_and_price_by_sku(self, sku):
        """Pobiera dane produktu z ERP po SKU (REST API style)."""
        print(f"[ERP] Pobieranie danych dla SKU: {sku}...")
        time.sleep(0.5) # Symulacja opóźnienia sieciowego
        product_data = self._database.get(sku)
        if product_data:
            return product_data
        else:
            return {"error": "Produkt nie znaleziony w ERP."}

class StoreSystemSimulator:
    """Symuluje platformę e-commerce Shoper przez API."""
    def __init__(self):
        # Dane demo: ID -> {SKU, Stan}
        self._catalog = {
            "shoper_id_101": {"sku": "ZKW-MOS-1", "stock": 145},
            "shoper_id_102": {"sku": "CZU-CIS-10", "stock": 45},
            "shoper_id_103": {"sku": "POM-WOD-25", "stock": 5}
        }

    def update_stock_by_sku(self, sku, new_stock):
        """Aktualizuje stan magazynowy w Shoper po SKU (REST API style)."""
        print(f"[STORE] Próba aktualizacji stanu dla SKU: {sku} na {new_stock}...")
        time.sleep(0.3)
        for prod_id, prod_data in self._catalog.items():
            if prod_data["sku"] == sku:
                old_stock = prod_data["stock"]
                prod_data["stock"] = new_stock
                return {"status": "success", "id": prod_id, "old_stock": old_stock, "new_stock": new_stock}
        return {"error": f"Produkt ze SKU {sku} nie znaleziony w sklepie."}

# --- DEMO ---
erp = ErpSystemSimulator()
store = StoreSystemSimulator()

# Lista SKU do synchronizacji (np. pobrana z BaseLinkera)
sku_do_synchronizacji = ["ZKW-MOS-1", "POM-WOD-25", "BRAK-PRODUKTU"]

print("-" * 20)
print("Uruchamianie synchronizacji ERP -> SKLEP...")
print("-" * 20)

for sku in sku_do_synchronizacji:
    # 1. Pobierz dane z ERP
    dane_erp = erp.get_stock_and_price_by_sku(sku)
    
    if "error" in dane_erp:
        print(f"BŁĄD ERP: {dane_erp['error']} dla {sku}. Pomijam.")
        continue

    # 2. Zaktualizuj stan w sklepie
    # W prawdziwym systemie porównalibyśmy stany przed aktualizacją
    nowy_stan = dane_erp["stock"]
    wynik_aktualizacji = store.update_stock_by_sku(sku, nowy_stan)

    if "success" in wynik_aktualizacji.get("status", ""):
        print(f"SUKCES: Zaktualizowano {sku}. ID: {wynik_aktualizacji['id']}. Stan: {wynik_aktualizacji['old_stock']} -> {wynik_aktualizacji['new_stock']}")
    else:
        print(f"BŁĄD AKTUALIZACJI: {wynik_aktualizacji['error']} dla {sku}.")

print("-" * 20)
print("Synchronizacja zakończona.")
print("-" * 20)
