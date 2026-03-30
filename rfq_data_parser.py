# --- ecommerce-ai-automation-tools/rfq_data_parser.py ---
import re
import json

def extract_technical_data(raw_text):
    """
    Ekstraktor danych technicznych z nieustrukturyzowanego tekstu RFQ.
    Idealny do automatyzacji wprowadzania produktów do PIM/ERP.
    """
    
    # Definiujemy wzorce (regex) dla typowych danych technicznych w branży
    patterns = {
        "material_grade": r"(AISI \d{3}|CW\d{3}N|Grade \d+)",
        "pressure_rating": r"(PN\d{2}|Class \d{3})",
        "size": r"(\d+\"?\s?CAL|\d+\s?mm|DN\d{2})",
        "standard": r"(ANSI|DIN|ISO|EN)\s?\d+",
    }
    
    results = {
        "original_text": raw_text[:50] + "...",
        "extracted_specs": {}
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            results["extracted_specs"][key] = match.group(0)
            
    return results

# --- DEMO ---
# Przykład tekstu, który mógłby przyjść w mailu od klienta lub z zapytania ofertowego
rfq_samples = [
    "Need quote for 50pcs of Ball Valve 1 CAL, Stainless Steel AISI 316, PN16, standard DIN 3202.",
    "Looking for Pressure Sensor 0-10 bar, 4-20mA, thread G1/4, Grade 2 material."
]

print("--- Uruchamianie parsera danych technicznych ---")

for sample in rfq_samples:
    parsed = extract_technical_data(sample)
    print(f"\nAnalizowany tekst: {sample}")
    print(f"Wyciągnięte dane: {json.dumps(parsed['extracted_specs'], indent=4, ensure_ascii=False)}")

# Symulacja zapisu do formatu JSON (gotowego do importu do bazy PIM/Shopera)
with open('parsed_data_output.json', 'w', encoding='utf-8') as f:
    json.dump([extract_technical_data(s) for s in rfq_samples], f, indent=4)
    print("\n[INFO] Wyniki zostały zapisane do pliku parsed_data_output.json")
