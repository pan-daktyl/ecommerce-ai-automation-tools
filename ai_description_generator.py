# --- ecommerce-ai-automation-tools/ai_description_generator.py ---
import os
import json
from openai import OpenAI
import pandas as pd

# --- KONFIGURACJA ---
# W prawdziwym projekcie użyj zmiennych środowiskowych!
# os.environ["OPENAI_API_KEY"] = "TWOJ_KLUCZ_API"
client = OpenAI()

def generuj_opis_z_parametrów(nazwa_produktu, parametry):
    """Generuje opis produktu w formacie Markdown przy użyciu OpenAI GPT."""
    
    # Tworzymy ustrukturyzowany prompt
    prompt_techniczny = f"""Skonstruuj profesjonalny opis produktu dla platformy Allegro/Shoper.
    Produkt: {nazwa_produktu}
    Parametry techniczne (format JSON):
    {json.dumps(parametry, indent=2)}
    
    Wymagania dla opisu:
    1. Użyj formatowania Markdown (pogrubienia dla kluczowych słów).
    2. Stwórz krótką, chwytliwą sekcję marketingową na początku.
    3. Stwórz sekcję "Dane techniczne" z listą punktowaną.
    4. Unikaj pustosłowia, skup się na konkretnych korzyściach technicznych.
    """
    
    print(f"Generowanie opisu dla: {nazwa_produktu}...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Używamy tańszego modelu do demo
            messages=[
                {"role": "system", "content": "Jesteś ekspertem ds. e-commerce i copywritingu technicznego."},
                {"role": "user", "content": prompt_techniczny}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Błąd API: {e}"

# --- DEMO ---
# Symulacja danych pobranych z PIM lub Excela
dane_demo = [
    {
        "product_name": "Zawór Kulowy MOSIĘŻNY 1\" CAL",
        "specs": {
            "Materiał": "Mosiądz CW617N",
            "Średnica": "1 cal (DN25)",
            "Ciśnienie robocze": "PN25",
            "Temperatura": "od -20°C do +120°C",
            "Zastosowanie": "Woda, Glikol, Powietrze"
        }
    },
    {
        "product_name": "Czujnik Ciśnienia 0-10 bar, 4-20mA",
        "specs": {
            "Zakres pomiarowy": "0-10 bar",
            "Sygnał wyjściowy": "4-20mA",
            "Zasilanie": "12-24V DC",
            "Gwint": "G1/4\"",
            "Dokładność": "±0.5% F.S."
        }
    }
]

# Przetwarzamy demo
for produkt in dane_demo:
    opis = generuj_opis_z_parametrów(produkt["product_name"], produkt["specs"])
    print("-" * 20)
    print(opis)
    print("-" * 20)
