# Telefon_SRB.py
# Aplikacija za upravljanje zalihama - PyDroid3 verzija za ANDROID TELEFON
# POBOLJŠANA VERZIJA: Ispravljeni dugmadi, padajući meniji i razmaci
# MODIFIKOVANO: Dva dugmeta u jednom redu, bez preloma teksta, ispravljene boje
# DODATO: Kompletna višejezična podrška sa prevedenim nazivima proizvoda

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime, timedelta
import sqlite3
import webbrowser
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---------------- PAMĆENJE EMAIL PODATAKA ----------------
def save_email_settings(sender_email, app_password, receiver_email):
    """Čuva email podešavanja u fajl"""
    try:
        with open("email_settings.txt", "w", encoding="utf-8") as f:
            f.write(f"sender_email={sender_email}\n")
            f.write(f"app_password={app_password}\n")
            f.write(f"receiver_email={receiver_email}\n")
        return True
    except Exception as e:
        print(f"Greška pri čuvanju email podešavanja: {e}")
        return False

def load_email_settings():
    """Učitava email podešavanja iz fajla"""
    try:
        if os.path.exists("email_settings.txt"):
            settings = {}
            with open("email_settings.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        settings[key] = value
            return settings
        return {}
    except Exception as e:
        print(f"Greška pri učitavanju email podešavanja: {e}")
        return {}

# ---------------- KONFIGURACIJA ZA ANDROID TELEFON ----------------
ROOT_FULLSCREEN = True
FONT_SIZE = 12 
BUTTON_FONT_SIZE = 10 
FORM_LABEL_FONT_SIZE = 10 
ICON_FOLDER = "/storage/emulated/0/Documents/Ikone"  # ISPRAVLJENA PUTANJA
LANG_ICON_FOLDER = os.path.join(ICON_FOLDER, "jezici")

if not os.path.exists(LANG_ICON_FOLDER):
    print("⚠️ Folder Ikone/jezici ne postoji:", LANG_ICON_FOLDER)
else:
    print("✅ Folder jezika pronađen:", LANG_ICON_FOLDER)

# Proveri da li folder postoji
if not os.path.exists(ICON_FOLDER):
    ICON_FOLDER = os.path.join(os.getcwd(), "Ikone")
    print(f"Ikone folder ne postoji, koristim: {ICON_FOLDER}")
else:
    print(f"Ikone folder pronađen: {ICON_FOLDER}")

# GLOBALNA PROMENLJIVA ZA IKONE JEZIKA - SAMO JEDNOM!
language_icons = {}

# ---------------- UČITAVANJE IKONA JEZIKA ---------------- 
def load_language_icons():
    """Učitava ikone za sve jezike iz folder-a"""
    jezici_folder = os.path.join(ICON_FOLDER, "jezici")
    language_icons_dict = {}
    
    # Definicija jezika i njihovih ikona
    language_files = {
        "srpski": ["srpski.png", "srpski.jpg", "sr.png", "rs.png"],
        "hungary": ["hungary.png", "hungary.jpg", "hu.png", "hungarian.png"],
        "ukrajinski": ["ukrajinski.png", "ukrajinski.jpg", "uk.png", "ua.png"],
        "ruski": ["ruski.png", "ruski.jpg", "ru.png", "russian.png"],
        "english": ["english.png", "english.jpg", "en.png", "gb.png", "us.png"],
        "deutsch": ["deutsch.png", "deutsch.jpg", "de.png", "german.png"],
        "mandarinski": ["mandarinski.png", "mandarinski.jpg", "zh.png", "cn.png"],
        "espanol": ["espanol.png", "espanol.jpg", "es.png", "spain.png"],
		"portugalski": ["portugalski.png", "portugalski.jpg", "pt.png", "portugal.png", "Portugal.png"],
        "francais": ["francais.png", "francais.jpg", "fr.png", "french.png"]
    }
    
    if os.path.exists(jezici_folder):
        print(f"\n=== UČITAVANJE IKONA JEZIKA ===")
        
        for lang_code, filenames in language_files.items():
            icon_found = False
            icon_image = None
            
            for filename in filenames:
                icon_path = os.path.join(jezici_folder, filename)
                if os.path.exists(icon_path):
                    try:
                        icon_image = tk.PhotoImage(file=icon_path)
                        
                        # PRIKAŽI VELIČINU ORIGINALNE IKONE
                        print(f"✓ {lang_code}: {filename} - {icon_image.width()}x{icon_image.height()}px")
                        
                        # BLAGO SMANJI IKONE - SAMO 2 PUTA
                        if icon_image.width() > 120:  # Ako je ikona veća od 120px
                            icon_image = icon_image.subsample(2, 2)  # SAMO 2x SMANJENJE
                            print(f"  → Smanjeno 2x na {icon_image.width()}x{icon_image.height()}px")
                        # Za jako velike ikone (240px+), možda 3x
                        elif icon_image.width() > 200:
                            icon_image = icon_image.subsample(3, 3)  # 3x SMANJENJE
                            print(f"  → Smanjeno 3x na {icon_image.width()}x{icon_image.height()}px")
                        
                        language_icons_dict[lang_code] = icon_image
                        icon_found = True
                        break
                    except Exception as e:
                        print(f"✗ {lang_code}: {filename} - Greška pri učitavanju: {e}")
            
            if not icon_found:
                print(f"✗ {lang_code}: NIJE PRONAĐENA IKONA")
                language_icons_dict[lang_code] = None
    
    else:
        print(f"\n✗ Folder jezici ne postoji: {jezici_folder}")
        for lang_code in language_files.keys():
            language_icons_dict[lang_code] = None
    
    return language_icons_dict

# GLOBALS - ROOT I OSNOVNI JEZIK
root = tk.Tk()
root.title("Zalihe - Upravljanje")

if ROOT_FULLSCREEN:
    root.attributes("-fullscreen", True)
else:
    root.geometry("400x700")

current_language = "srpski"

# ---------------- INICIJALIZACIJA IKONA ---------------- 
print("\n" + "="*50)
print("INICIJALIZACIJA IKONA JEZIKA")
print("="*50)

# Učitaj ikone jezika - OVO MORA BITI POSLE KREIRANJA root!
language_icons = load_language_icons()

# ---------------- MASTER STRINGS ZA SVE JEZIKE ----------------

master_strings = {
    "srpski": {
        "nazad": "Nazad", "stanje": "Zalihe", "izlaz": "Izlaz", "spisak": "Spisak", 
        # ... ostatak vašeg koda ...
        "nazad": "Nazad", "stanje": "Zalihe", "izlaz": "Izlaz", "spisak": "Spisak", 
        "naziv_proizvoda": "Proizvod:", "opis": "Opis:", "komad": "Komad:", 
        "kolicina": "Količina:", "jedinica_mere": "Jed. mere:", "datum_unosa": "Datum unosa:", 
        "rok_trajanja": "Rok (meseci):", "automatski_rok": "Automatski rok:", 
        "mesto_skladistenja": "Skladište:", "unesi": "Unesi", "pretrazi": "Pretraži:",
        "azuriraj": "Ažuriraj", "obrisi": "Obriši", "stampaj": "Štampaj", "posalji": "Pošalji",
        "izbor_jezika": "Izaberite jezik", "pocetak": "Početak", "jezik": "Jezik",
        "glavne_kategorije": "Glavne kategorije:", "podkategorije": "Podkategorije -",
        "delovi_proizvoda": "Delovi proizvoda -", "unos_podataka": "Unos podataka",
        "azuriranje_proizvoda": "Ažuriranje proizvoda", "stanje_zaliha": "Stanje zaliha",
        "spisak_potreba": "Spisak potreba", "posalji_spisak": "Pošalji spisak",
        "oznaci_sve": "Označi sve", "kopiraj": "Kopiraj", "posalji_email": "Pošalji Email",
        "posalji_messenger": "Pošalji Messenger", "pomoc_app_password": "Pomoć - App Password",
        "Ostalo": "Ostalo",
		"azuriraj_proizvod": "Ažuriraj proizvod",
        "snimi_izmene": "Snimi izmene",
        "proizvod_azuriran": "Proizvod je uspešno ažuriran",
        "selektuj_proizvod": "Selektuj proizvod za ažuriranje",
        "trenutne_vrednosti": "Trenutne vrednosti:",
        "nove_vrednosti": "Nove vrednosti:",
        "potvrda_azuriranja": "Potvrda ažuriranja",
        "potvrdi_izmenu": "Potvrdi izmenu?",
        "nema_proizvoda": "Nema proizvoda za prikaz",
        "pogresan_izbor": "Pogrešan izbor",
        "pogresan_unos": "Pogrešan unos",
		"enter_nastavak": "Pritisni Enter za nastavak...",
        "izbor": "Izbor",
        		
		"popunite_polja": "Popunite sva obavezna polja",
        "kolicina_mora_broj": "Količina mora biti broj",
        "pregled_unosa": "Pregled unosa za",
        "zamrzivac_1": "Zamrzivač 1",
        "zamrzivac_2": "Zamrzivač 2",
        "zamrzivac_3": "Zamrzivač 3",
        "frizider": "Frižider",
        "ostava": "Ostava",

        "zaglavlja_zaliha": {
            "naziv": "Proizvod",
            "opis": "Opis",
            "komada": "Kom.",
            "jedinica": "Jed.",
            "kolicina": "Kol.",
            "rok_trajanja": "Rok",
            "mesto_skladistenja": "Sklad."
        },
        "zaglavlja_spisak": {
            "proizvod": "Proizvod",
            "opis": "Opis",
            "datum_unosa": "Datum unosa"
        }
    },

    "hungary": {
        "nazad": "Vissza", "stanje": "Készlet", "izlaz": "Kilépés", "spisak": "Bevásárlólista", 
        "naziv_proizvoda": "Termék:", "opis": "Leírás:", "komad": "Darab:", 
        "kolicina": "Mennyiség:", "jedinica_mere": "Mértékegység:", "datum_unosa": "Beírás dátuma:", 
        "rok_trajanja": "Szavatosság (hónap):", "automatski_rok": "Automatikus lejárat:", 
        "mesto_skladistenja": "Raktár:", "unesi": "Bevitel", "pretrazi": "Keresés:",
        "azuriraj": "Frissítés", "obrisi": "Törlés", "stampaj": "Nyomtatás", "posalji": "Küldés",
        "izbor_jezika": "Válasszon nyelvet", "pocetak": "Kezdés", "jezik": "Nyelv",
        "glavne_kategorije": "Fő kategóriák:", "podkategorije": "Alkategóriák -",
        "delovi_proizvoda": "Termék részei -", "unos_podataka": "Adatbevitel",
        "azuriranje_proizvoda": "Termék frissítése", "stanje_zaliha": "Készlet állapota",
        "spisak_potreba": "Bevásárlólista", "posalji_spisak": "Lista küldése",
        "oznaci_sve": "Összes kijelölése", "kopiraj": "Másolás", "posalji_email": "Email küldése",
        "posalji_messenger": "Messenger küldése", "pomoc_app_password": "Súgó - App Jelszó",
        "Ostalo": "Egyéb", 
		"azuriraj_proizvod": "Termék frissítése",
        "snimi_izmene": "Változtatások mentése",
        "proizvod_azuriran": "Termék sikeresen frissítve",
        "selektuj_proizvod": "Válasszon terméket frissítéshez",
        "trenutne_vrednosti": "Jelenlegi értékek:",
        "nove_vrednosti": "Új értékek:",
        "potvrda_azuriranja": "Frissítés megerősítése",
        "potvrdi_izmenu": "Megerősíti a változtatásokat?",
        "nema_proizvoda": "Nincsenek megjeleníthető termékek",
        "pogresan_izbor": "Hibás választás",
        "pogresan_unos": "Hibás bevitel",
        "enter_nastavak": "Nyomja meg az Entert a folytatáshoz...",
        "izbor": "Választás",		
        
        "popunite_polja": "Töltse ki az összes kötelező mezőt",
        "kolicina_mora_broj": "A mennyiségnek számnak kell lennie",
        "pregled_unosa": "Bevitel áttekintése",
        "zamrzivac_1": "Mélyhűtő 1",
        "zamrzivac_2": "Mélyhűtő 2",
        "zamrzivac_3": "Mélyhűtő 3",
        "frizider": "Hűtőszekrény",
        "ostava": "Spájz",

        "zaglavlja_zaliha": {
            "naziv": "Termék",
            "opis": "Leírás",
            "komada": "Db.",
            "jedinica": "Egys.",
            "kolicina": "Menny.",
            "rok_trajanja": "Lejárat",
            "mesto_skladistenja": "Tárolás"
        },
        "zaglavlja_spisak": {
            "proizvod": "Termék",
            "opis": "Leírás",
            "datum_unosa": "Beviteli dátum"
        }
    },

    "ukrajinski": {
        "nazad": "Назад", "stanje": "Запаси", "izlaz": "Вихід", "spisak": "Список", 
        "naziv_proizvoda": "Продукт:", "opis": "Опис:", "komad": "Штука:", 
        "kolicina": "Кількість:", "jedinica_mere": "Од. виміру:", "datum_unosa": "Дата внесення:", 
        "rok_trajanja": "Термін (місяці):", "automatski_rok": "Авто термін:", 
        "mesto_skladistenja": "Сховище:", "unesi": "Внести", "pretrazi": "Пошук:",
        "azuriraj": "Оновити", "obrisi": "Видалити", "stampaj": "Друк", "posalji": "Надіслати",
        "izbor_jezika": "Виберіть мову", "pocetak": "Початок", "jezik": "Мова",
        "glavne_kategorije": "Основні категорії:", "podkategorije": "Підкатегорії -",
        "delovi_proizvoda": "Частини продукту -", "unos_podataka": "Введення даних",
        "azuriranje_proizvoda": "Оновлення продукту", "stanje_zaliha": "Стан запасів",
        "spisak_potreba": "Список потреб", "posalji_spisak": "Надіслати список",
        "oznaci_sve": "Вибрати все", "kopiraj": "Копіювати", "posalji_email": "Надіслати Email",
        "posalji_messenger": "Надіслати Messenger", "pomoc_app_password": "Допомога - App Пароль",
        "Ostalo": "Інше",
		"azuriraj_proizvod": "Оновити продукт",
        "snimi_izmene": "Зберегти зміни",
        "proizvod_azuriran": "Продукт успішно оновлено",
        "selektuj_proizvod": "Виберіть продукт для оновлення",
        "trenutne_vrednosti": "Поточні значення:",
        "nove_vrednosti": "Нові значення:",
        "potvrda_azuriranja": "Підтвердження оновлення",
        "potvrdi_izmenu": "Підтвердити зміни?",
        "nema_proizvoda": "Немає продуктів для відображення",
        "pogresan_izbor": "Неправильний вибір",
        "pogresan_unos": "Неправильне введення",
        "enter_nastavak": "Натисніть Enter для продовження...",
        "izbor": "Вибір",
		
		"popunite_polja": "Заповніть всі обов'язкові поля",
        "kolicina_mora_broj": "Кількість повинна бути числом",
        "pregled_unosa": "Огляд введення для",
        "zamrzivac_1": "Морозилка 1",
        "zamrzivac_2": "Морозилка 2",
        "zamrzivac_3": "Морозилка 3",
        "frizider": "Холодильник",
        "ostava": "Комора",

        "zaglavlja_zaliha": {
            "naziv": "Продукт",
            "opis": "Опис",
            "komada": "Шт.",
            "jedinica": "Од.",
            "kolicina": "Кільк.",
            "rok_trajanja": "Термін",
            "mesto_skladistenja": "Склад"
        },
        "zaglavlja_spisak": {
            "proizvod": "Продукт",
            "opis": "Опис",
            "datum_unosa": "Дата внесення"
        }
    },

    "ruski": {
        "nazad": "Назад", "stanje": "Запасы", "izlaz": "Выход", "spisak": "Список", 
        "naziv_proizvoda": "Продукт:", "opis": "Описание:", "komad": "Штука:", 
        "kolicina": "Количество:", "jedinica_mere": "Ед. изм.:", "datum_unosa": "Дата внесения:", 
        "rok_trajanja": "Срок (месяцы):", "automatski_rok": "Авто срок:", 
        "mesto_skladistenja": "Склад:", "unesi": "Внести", "pretrazi": "Поиск:",
        "azuriraj": "Обновить", "obrisi": "Удалить", "stampaj": "Печать", "posalji": "Отправить",
        "izbor_jezika": "Выберите язык", "pocetak": "Начало", "jezik": "Язык",
        "glavne_kategorije": "Основные категории:", "podkategorije": "Подкатегории -",
        "delovi_proizvoda": "Части продукта -", "unos_podataka": "Ввод данных",
        "azuriranje_proizvoda": "Обновление продукта", "stanje_zaliha": "Состояние запасов",
        "spisak_potreba": "Список потребностей", "posalji_spisak": "Отправить список",
        "oznaci_sve": "Выбрать все", "kopiraj": "Копировать", "posalji_email": "Отправить Email",
        "posalji_messenger": "Отправить Messenger", "pomoc_app_password": "Помощь - App Пароль",
        "Ostalo": "Другое",
		"azuriraj_proizvod": "Обновить продукт",
        "snimi_izmene": "Сохранить изменения",
        "proizvod_azuriran": "Продукт успешно обновлен",
        "selektuj_proizvod": "Выберите продукт для обновления",
        "trenutne_vrednosti": "Текущие значения:",
        "nove_vrednosti": "Новые значения:",
        "potvrda_azuriranja": "Подтверждение обновления",
        "potvrdi_izmenu": "Подтвердить изменения?",
        "nema_proizvoda": "Нет продуктов для отображения",
        "pogresan_izbor": "Неверный выбор",
        "pogresan_unos": "Неверный ввод",
        "enter_nastavak": "Нажмите Enter для продолжения...",
        "izbor": "Выбор",
		
		"popunite_polja": "Заполните все обязательные поля",
        "kolicina_mora_broj": "Количество должно быть числом",
        "pregled_unosa": "Обзор ввода для",
        "zamrzivac_1": "Морозилка 1",
        "zamrzivac_2": "Морозилка 2",
        "zamrzivac_3": "Морозилка 3",
        "frizider": "Холодильник",
        "ostava": "Кладовая",
		
        "zaglavlja_zaliha": {
            "naziv": "Продукт",
            "opis": "Описание",
            "komada": "Шт.",
            "jedinica": "Ед.",
            "kolicina": "Кол-во",
            "rok_trajanja": "Срок",
            "mesto_skladistenja": "Склад"
        },
        "zaglavlja_spisak": {
            "proizvod": "Продукт",
            "opis": "Описание",
            "datum_unosa": "Дата добавления"
        }
    },

    "english": {
        "nazad": "Back", "stanje": "Inventory", "izlaz": "Exit", "spisak": "Shopping List", 
        "naziv_proizvoda": "Product:", "opis": "Description:", "komad": "Piece:", 
        "kolicina": "Quantity:", "jedinica_mere": "Unit:", "datum_unosa": "Entry Date:", 
        "rok_trajanja": "Shelf Life (months):", "automatski_rok": "Auto Expiry:", 
        "mesto_skladistenja": "Storage:", "unesi": "Enter", "pretrazi": "Search:",
        "azuriraj": "Update", "obrisi": "Delete", "stampaj": "Print", "posalji": "Send",
        "izbor_jezika": "Choose Language", "pocetak": "Start", "jezik": "Language",
        "glavne_kategorije": "Main Categories:", "podkategorije": "Subcategories -",
        "delovi_proizvoda": "Product Parts -", "unos_podataka": "Data Entry",
        "azuriranje_proizvoda": "Update Product", "stanje_zaliha": "Inventory Status",
        "spisak_potreba": "Shopping List", "posalji_spisak": "Send List",
        "oznaci_sve": "Select All", "kopiraj": "Copy", "posalji_email": "Send Email",
        "posalji_messenger": "Send Messenger", "pomoc_app_password": "Help - App Password",
        "Ostalo": "Other",
		"azuriraj_proizvod": "Update product",
        "snimi_izmene": "Save changes", 
        "proizvod_azuriran": "Product successfully updated",
        "selektuj_proizvod": "Select product for update",
        "trenutne_vrednosti": "Current values:",
        "nove_vrednosti": "New values:",
        "potvrda_azuriranja": "Update confirmation",
        "potvrdi_izmenu": "Confirm changes?",
        "nema_proizvoda": "No products to display",
        "pogresan_izbor": "Wrong choice",
        "pogresan_unos": "Wrong input",
        "enter_nastavak": "Press Enter to continue...",
        "izbor": "Choice",
		
		"popunite_polja": "Fill in all required fields",
        "kolicina_mora_broj": "Quantity must be a number",
        "pregled_unosa": "Entry review for",
        "zamrzivac_1": "Freezer 1",
        "zamrzivac_2": "Freezer 2",
        "zamrzivac_3": "Freezer 3",
        "frizider": "Refrigerator",
        "ostava": "Pantry",

        "zaglavlja_zaliha": {
            "naziv": "Product", 
            "opis": "Desc.",
            "komada": "Pcs.",
            "jedinica": "Unit",
            "kolicina": "Qty.",
            "rok_trajanja": "Expiry",
            "mesto_skladistenja": "Storage"
        },
        "zaglavlja_spisak": {
            "proizvod": "Product",
            "opis": "Description",
            "datum_unosa": "Entry Date"
        }
    },

    "deutsch": {
        "nazad": "Zurück", "stanje": "Bestand", "izlaz": "Beenden", "spisak": "Einkaufsliste", 
        "naziv_proizvoda": "Produkt:", "opis": "Beschreibung:", "komad": "Stück:", 
        "kolicina": "Menge:", "jedinica_mere": "Einheit:", "datum_unosa": "Eingangsdatum:", 
        "rok_trajanja": "Haltbarkeit (Monate):", "automatski_rok": "Auto Ablauf:", 
        "mesto_skladistenja": "Lager:", "unesi": "Eingeben", "pretrazi": "Suchen:",
        "azuriraj": "Aktualisieren", "obrisi": "Löschen", "stampaj": "Drucken", "posalji": "Senden",
        "izbor_jezika": "Sprache auswählen", "pocetak": "Start", "jezik": "Sprache",
        "glavne_kategorije": "Hauptkategorien:", "podkategorije": "Unterkategorien -",
        "delovi_proizvoda": "Produktteile -", "unos_podataka": "Dateneingabe",
        "azuriranje_proizvoda": "Produkt aktualisieren", "stanje_zaliha": "Bestandsstatus",
        "spisak_potreba": "Einkaufsliste", "posalji_spisak": "Liste senden",
        "oznaci_sve": "Alle auswählen", "kopiraj": "Kopieren", "posalji_email": "Email senden",
        "posalji_messenger": "Messenger senden", "pomoc_app_password": "Hilfe - App Passwort",
        "Ostalo": "Andere",
		"azuriraj_proizvod": "Produkt aktualisieren",
        "snimi_izmene": "Änderungen speichern",
        "proizvod_azuriran": "Produkt erfolgreich aktualisiert",
        "selektuj_proizvod": "Produkt zur Aktualisierung auswählen",
        "trenutne_vrednosti": "Aktuelle Werte:",
        "nove_vrednosti": "Neue Werte:",
        "potvrda_azuriranja": "Aktualisierungsbestätigung",
        "potvrdi_izmenu": "Änderungen bestätigen?",
        "nema_proizvoda": "Keine Produkte zum Anzeigen",
        "pogresan_izbor": "Falsche Auswahl",
        "pogresan_unos": "Falsche Eingabe",
        "enter_nastavak": "Enter drücken zum Fortsetzen...",
        "izbor": "Auswahl",
		
		"popunite_polja": "Füllen Sie alle Pflichtfelder aus",
        "kolicina_mora_broj": "Menge muss eine Zahl sein",
        "pregled_unosa": "Eingabeübersicht für",
        "zamrzivac_1": "Gefrierschrank 1",
        "zamrzivac_2": "Gefrierschrank 2",
        "zamrzivac_3": "Gefrierschrank 3",
        "frizider": "Kühlschrank",
        "ostava": "Vorratskammer",
		
        "zaglavlja_zaliha": {
            "naziv": "Produkt",  
            "opis": "Beschr.",
            "komada": "Stk.",
            "jedinica": "Einheit",
            "kolicina": "Menge",
            "rok_trajanja": "Ablauf",
            "mesto_skladistenja": "Lager" 
        },
        "zaglavlja_spisak": {
            "proizvod": "Produkt",
            "opis": "Beschreibung",
            "datum_unosa": "Eintragsdatum"
        }
    },

    "mandarinski": {
        "nazad": "返回", "stanje": "库存", "izlaz": "退出", "spisak": "购物清单", 
        "naziv_proizvoda": "产品:", "opis": "描述:", "komad": "件:", 
        "kolicina": "数量:", "jedinica_mere": "单位:", "datum_unosa": "录入日期:", 
        "rok_trajanja": "保质期(月):", "automatski_rok": "自动到期:", 
        "mesto_skladistenja": "存储:", "unesi": "输入", "pretrazi": "搜索:",
        "azuriraj": "更新", "obrisi": "删除", "stampaj": "打印", "posalji": "发送",
        "izbor_jezika": "选择语言", "pocetak": "开始", "jezik": "语言",
        "glavne_kategorije": "主要类别:", "podkategorije": "子类别 -",
        "delovi_proizvoda": "产品部件 -", "unos_podataka": "数据输入",
        "azuriranje_proizvoda": "更新产品", "stanje_zaliha": "库存状态",
        "spisak_potreba": "购物清单", "posalji_spisak": "发送列表",
        "oznaci_sve": "全选", "kopiraj": "复制", "posalji_email": "发送邮件",
        "posalji_messenger": "发送Messenger", "pomoc_app_password": "帮助 - 应用密码",
        "Ostalo": "其他",
		"azuriraj_proizvod": "更新产品",
        "snimi_izmene": "保存更改",
        "proizvod_azuriran": "产品更新成功",
        "selektuj_proizvod": "选择要更新的产品",
        "trenutne_vrednosti": "当前值:",
        "nove_vrednosti": "新值:",
        "potvrda_azuriranja": "更新确认",
        "potvrdi_izmenu": "确认更改?",
        "nema_proizvoda": "没有产品可显示",
        "pogresan_izbor": "选择错误",
        "pogresan_unos": "输入错误",
        "enter_nastavak": "按Enter键继续...",
        "izbor": "选择",
		
		"popunite_polja": "请填写所有必填字段",
        "kolicina_mora_broj": "数量必须是数字",
        "pregled_unosa": "输入记录查看",
        "zamrzivac_1": "冷冻柜 1",
        "zamrzivac_2": "冷冻柜 2",
        "zamrzivac_3": "冷冻柜 3",
        "frizider": "冰箱",
        "ostava": "储藏室",

        "zaglavlja_zaliha": {
            "naziv": "产品",
            "opis": "描述",
            "komada": "件",
            "jedinica": "单位",
            "kolicina": "数量",
            "rok_trajanja": "有效期",
            "mesto_skladistenja": "存储"
        },
        "zaglavlja_spisak": {
            "proizvod": "产品",
            "opis": "描述",
            "datum_unosa": "录入日期"
        }
    },

    "espanol": {
        "nazad": "Atrás", "stanje": "Inventario", "izlaz": "Salir", "spisak": "Lista de Compras", 
        "naziv_proizvoda": "Producto:", "opis": "Descripción:", "komad": "Pieza:", 
        "kolicina": "Cantidad:", "jedinica_mere": "Unidad:", "datum_unosa": "Fecha de Entrada:", 
        "rok_trajanja": "Caducidad (meses):", "automatski_rok": "Vencimiento Auto:", 
        "mesto_skladistenja": "Almacenamiento:", "unesi": "Ingresar", "pretrazi": "Buscar:",
        "azuriraj": "Actualizar", "obrisi": "Eliminar", "stampaj": "Imprimir", "posalji": "Enviar",
        "izbor_jezika": "Elija idioma", "pocetak": "Inicio", "jezik": "Idioma",
        "glavne_kategorije": "Categorías Principales:", "podkategorije": "Subcategorías -",
        "delovi_proizvoda": "Partes del Producto -", "unos_podataka": "Entrada de Datos",
        "azuriranje_proizvoda": "Actualizar Producto", "stanje_zaliha": "Estado del Inventario",
        "spisak_potreba": "Lista de Compras", "posalji_spisak": "Enviar Lista",
        "oznaci_sve": "Seleccionar Todo", "kopiraj": "Copiar", "posalji_email": "Enviar Email",
        "posalji_messenger": "Enviar Messenger", "pomoc_app_password": "Ayuda - Contraseña App",
        "Ostalo": "Otro",
		"azuriraj_proizvod": "Actualizar producto",
        "snimi_izmene": "Guardar cambios",
        "proizvod_azuriran": "Producto actualizado con éxito",
        "selektuj_proizvod": "Seleccione producto para actualizar",
        "trenutne_vrednosti": "Valores actuales:",
        "nove_vrednosti": "Nuevos valores:",
        "potvrda_azuriranja": "Confirmación de actualización",
        "potvrdi_izmenu": "¿Confirmar cambios?",
        "nema_proizvoda": "No hay productos para mostrar",
        "pogresan_izbor": "Elección incorrecta",
        "pogresan_unos": "Entrada incorrecta",
        "enter_nastavak": "Presione Enter para continuar...",
        "izbor": "Elección",
		
		"popunite_polja": "Complete todos los campos obligatorios",
        "kolicina_mora_broj": "La cantidad debe ser un número",
        "pregled_unosa": "Revisión de entrada para",
        "zamrzivac_1": "Congelador 1",
        "zamrzivac_2": "Congelador 2",
        "zamrzivac_3": "Congelador 3",
        "frizider": "Refrigerador",
        "ostava": "Despensa",

        "zaglavlja_zaliha": {
            "naziv": "Producto",
            "opis": "Descripción",
            "komada": "Unid.",
            "jedinica": "Unidad",
            "kolicina": "Cant.",
            "rok_trajanja": "Vencimiento",
            "mesto_skladistenja": "Almacén"
        },
        "zaglavlja_spisak": {
            "proizvod": "Producto",
            "opis": "Descripción",
            "datum_unosa": "Fecha de ingreso"
        }
    },

    # dodajte ovo u dictionary master_strings, posle "francais" bloka:

	"portugalski": {
		"nazad": "Voltar", "stanje": "Estoque", "izlaz": "Sair", "spisak": "Lista de Compras", 
		"naziv_proizvoda": "Produto:", "opis": "Descrição:", "komad": "Peça:", 
		"kolicina": "Quantidade:", "jedinica_mere": "Unidade:", "datum_unosa": "Data de Entrada:", 
		"rok_trajanja": "Validade (meses):", "automatski_rok": "Validade Auto:", 
		"mesto_skladistenja": "Armazenamento:", "unesi": "Inserir", "pretrazi": "Pesquisar:",
		"azuriraj": "Atualizar", "obrisi": "Excluir", "stampaj": "Imprimir", "posalji": "Enviar",
		"izbor_jezika": "Escolha o idioma", "pocetak": "Início", "jezik": "Idioma",
		"glavne_kategorije": "Categorias Principais:", "podkategorije": "Subcategorias -",
		"delovi_proizvoda": "Partes do Produto -", "unos_podataka": "Entrada de Dados",
		"azuriranje_proizvoda": "Atualizar Produto", "stanje_zaliha": "Status do Estoque",
		"spisak_potreba": "Lista de Compras", "posalji_spisak": "Enviar Lista",
		"oznaci_sve": "Selecionar Tudo", "kopiraj": "Copiar", "posalji_email": "Enviar Email",
		"posalji_messenger": "Enviar Messenger", "pomoc_app_password": "Ajuda - Senha App",
		"Ostalo": "Outro",
		"azuriraj_proizvod": "Atualizar produto",
		"snimi_izmene": "Salvar alterações",
		"proizvod_azuriran": "Produto atualizado com sucesso",
		"selektuj_proizvod": "Selecione produto para atualizar",
		"trenutne_vrednosti": "Valores atuais:",
		"nove_vrednosti": "Novos valores:",
		"potvrda_azuriranja": "Confirmação de atualização",
		"potvrdi_izmenu": "Confirmar alterações?",
		"nema_proizvoda": "Nenhum produto para exibir",
		"pogresan_izbor": "Escolha incorreta",
		"pogresan_unos": "Entrada incorreta",
		"enter_nastavak": "Pressione Enter para continuar...",
		"izbor": "Escolha",
		"popunite_polja": "Preencha todos os campos obrigatórios",
		"kolicina_mora_broj": "A quantidade deve ser um número",
		"pregled_unosa": "Revisão de entrada para",
		"zamrzivac_1": "Congelador 1",
		"zamrzivac_2": "Congelador 2",
		"zamrzivac_3": "Congelador 3",
		"frizider": "Geladeira",
		"ostava": "Despensa",
    
		"zaglavlja_zaliha": {
			"naziv": "Produto",
			"opis": "Descrição",
			"komada": "Pçs.",
			"jedinica": "Unid.",
			"kolicina": "Qtd.",
			"rok_trajanja": "Validade",
			"mesto_skladistenja": "Armaz."
		},
		"zaglavlja_spisak": {
			"proizvod": "Produto",
			"opis": "Descrição",
			"datum_unosa": "Data de entrada"
		}
	},
	"francais": {
        "nazad": "Retour", "stanje": "Stock", "izlaz": "Quitter", "spisak": "Liste de Courses", 
        "naziv_proizvoda": "Produit:", "opis": "Description:", "komad": "Pièce:", 
        "kolicina": "Quantité:", "jedinica_mere": "Unité:", "datum_unosa": "Date d'entrée:", 
        "rok_trajanja": "Durée (mois):", "automatski_rok": "Expiration Auto:", 
        "mesto_skladistenja": "Stockage:", "unesi": "Entrer", "pretrazi": "Rechercher:",
        "azuriraj": "Mettre à jour", "obrisi": "Supprimer", "stampaj": "Imprimer", "posalji": "Envoyer",
        "izbor_jezika": "Choisir la langue", "pocetak": "Début", "jezik": "Langue",
        "glavne_kategorije": "Catégories Principales:", "podkategorije": "Sous-catégories -",
        "delovi_proizvoda": "Pièces du Produit -", "unos_podataka": "Saisie de Données",
        "azuriranje_proizvoda": "Mettre à jour Produit", "stanje_zалиha": "État du Stock",
        "spisak_potreba": "Liste de Courses", "posalji_spisak": "Envoyer Liste",
        "oznaci_sve": "Tout sélectionner", "kopiraj": "Copier", "posalji_email": "Envoyer Email",
        "posalji_messenger": "Envoyer Messenger", "pomoc_app_password": "Aide - Mot de passe App",
        "Ostalo": "Autre",
		"azuriraj_proizvod": "Mettre à jour le produit",
        "snimi_izmene": "Enregistrer les modifications",
        "proizvod_azuriran": "Produit mis à jour avec succès",
        "selektuj_proizvod": "Sélectionnez un produit à mettre à jour",
        "trenutne_vrednosti": "Valeurs actuelles:",
        "nove_vrednosti": "Nouvelles valeurs:",
        "potvrda_azuriranja": "Confirmation de mise à jour",
        "potvrdi_izmenu": "Confirmer les modifications?",
        "nema_proizvoda": "Aucun produit à afficher",
        "pogresan_izbor": "Choix incorrect",
        "pogresan_unos": "Entrée incorrecte",
        "enter_nastavak": "Appuyez sur Entrée pour continuer...",
        "izbor": "Choix",
		
		"popunite_polja": "Remplissez tous les champs obligatoires",
        "kolicina_mora_broj": "La quantité doit être un nombre",
        "pregled_unosa": "Aperçu des saisies pour",
        "zamrzivac_1": "Congélateur 1",
        "zamrzivac_2": "Congélateur 2",
        "zamrzivac_3": "Congélateur 3",
        "frizider": "Réfrigérateur",
        "ostava": "Garde-manger",

        "zaglavlja_zaliha": {
            "naziv": "Produit",
            "opis": "Description",
            "komada": "Pièce",
            "jedinica": "Unité",
            "kolicina": "Qté",
            "rok_trajanja": "Expiration",
            "mesto_skladistenja": "Stockage"
        },
        "zaglavlja_spisak": {
            "proizvod": "Produit",
            "opis": "Description",
            "datum_unosa": "Date d’entrée"
        }
    }
}

# ---------------- STRUKTURA PROIZVODA, BOJE I DELOVI ----------------
# GLAVNE KATEGORIJE NA SVIM JEZICIMA
main_categories_translations = {
    "srpski": [
        "Belo meso", "Crveno meso", "Sitna divljač", "Krupna divljač",
        "Riba", "Mlečni proizvodi", "Povrće", "Zimnica i kompoti",
        "Testo i Slatkiši", "Pića", "Hemija i higijena", "Ostalo"
    ],
    "hungary": [
        "Fehér hús", "Vörös hús", "Apróvad", "Nagyvad",
        "Hal", "Tejtermékek", "Zöldség", "Befőttek és kompótok",
        "Tészta és Édességek", "Italok", "Kémia és higiénia", "Egyéb"
    ],
    "ukrajinski": [
        "Біле м'ясо", "Червоне м'ясо", "Дрібна дичина", "Велика дичина",
        "Риба", "Молочні продукти", "Овочі", "Консервація та компоти",
        "Тісто та Солодощі", "Напої", "Хімія та гігієна", "Інше"
    ],
    "ruski": [
        "Белое мясо", "Красное мясо", "Мелкая дичь", "Крупная дичь",
        "Рыба", "Молочные продукты", "Овощи", "Консервация и компоты",
        "Тесто и Сладости", "Напитки", "Химия и гигиена", "Другое"
    ],
    "english": [
        "White meat", "Red meat", "Small game", "Big game",
        "Fish", "Dairy products", "Vegetables", "Preserves and compotes",
        "Dough and Sweets", "Beverages", "Chemicals and hygiene", "Other"
    ],
    "deutsch": [
        "Weißes Fleisch", "Rotes Fleisch", "Kleinwild", "Großwild",
        "Fisch", "Milchprodukte", "Gemüse", "Konserven und Kompotte",
        "Teig und Süßigkeiten", "Getränke", "Chemie und Hygiene", "Andere"
    ],
    "mandarinski": [
        "白肉", "红肉", "小型野味", "大型野味",
        "鱼", "乳制品", "蔬菜", "蜜饯和蜜饯",
        "面团和糖果", "饮料", "化学品和卫生", "其他"
    ],
    "espanol": [
        "Carne blanca", "Carne roja", "Caza menor", "Caza mayor",
        "Pescado", "Productos lácteos", "Verduras", "Conservas y compotas",
        "Masa y Dulces", "Bebidas", "Química e higiene", "Otro"
	],
	"portugalski": [
		"Carne branca", "Carne vermelha", "Caça pequena", "Caça grossa",
		"Peixe", "Laticínios", "Vegetais", "Conservas e compotas",
		"Massa e Doces", "Bebidas", "Química e higiene", "Outro"
	],
    "francais": [
        "Viande blanche", "Viande rouge", "Petit gibier", "Gros gibier",
        "Poisson", "Produits laitiers", "Légumes", "Conserves et compotes",
        "Pâte et Sucreries", "Boissons", "Chimie et hygiène", "Autre"
    ]
}

# PODKATEGORIJE NA SVIM JEZICIMA
subcategories_translations = {
    "srpski": {
        "Belo meso": ["Pileće", "Ćureće", "Guska", "Patka", "Ostalo"],
        "Crveno meso": ["Svinjsko", "Jagnjeće", "Ovčije", "Juneće", "Govedina", "Od bika", "Konjsko", "Zečije", "Ostalo"],
        "Sitna divljač": ["Prepelica", "Fazan", "Jarebica", "Divlja patka", "Divlja guska", "Divlji zec", "Golub", "Ostalo"],
        "Krupna divljač": ["Jelen", "Srna", "Divokoza", "Los", "Irvas", "Divlja svinja", "Bizon", "Kamila", "Lama", "Alpaka", "Kengur", "Krokodil/Aligator", "Gušter", "Zmija", "Ostalo"],
        "Riba": ["Morska", "Slatkovodna", "Plodovi mora", "Ostalo"],
        "Mlečni proizvodi": ["Mleko", "Mlečne prerađevine", "Ostalo"],
        "Povrće": ["Sveže", "Termički obrađeno", "Zamrznuto", "Ostalo"],
        "Zimnica i kompoti": ["Voće", "Povrće", "Ostalo"],
        "Testo i Slatkiši": ["Testo", "Slatkiši", "Ostalo"],
        "Pića": ["Voda", "Vino", "Sok", "Žestoka pića", "Pivo", "Ostalo"],
        "Hemija i higijena": ["Sanitar", "Lična higijena", "Pribor", "Ostalo"],
        "Ostalo": ["Ostalo"]
    },
    "hungary": {
        "Fehér hús": ["Csirke", "Pulyka", "Libacomb", "Kacsa", "Egyéb"],
        "Vörös hús": ["Sertéshús", "Bárányhús", "Juhhús", "Borjúhús", "Marhahús", "Bikahús", "Lóhús", "Nyúlhús", "Egyéb"],
        "Apróvad": ["Fürj", "Fácán", "Fogoly", "Vadkacsa", "Vadliba", "Vadnyúl", "Galamb", "Egyéb"],
        "Nagyvad": ["Szarvac", "Őz", "Vadkecske", "Jávorszarvas", "Rénszarvas", "Vadkan", "Bölény", "Teve", "Láma", "Alpaka", "Kenguru", "Krokodil/Alligátor", "Gyík", "Kígyó", "Egyéb"],
        "Hal": ["Tengeri", "Édesvízi", "Tenger gyümölcsei", "Egyéb"],
        "Tejtermékek": ["Tej", "Tejfeldolgozások", "Egyéb"],
        "Zöldség": ["Friss", "Hőkezelt", "Fagyasztott", "Egyéb"],
        "Befőttek és kompótok": ["Gyümölcs", "Zöldség", "Egyéb"],
        "Tészta és Édességek": ["Tészta", "Édességek", "Egyéb"],
        "Italok": ["Víz", "Bor", "Lé", "Tömény italok", "Sör", "Egyéb"],
        "Kémia és higiénia": ["WC", "Személyes higiénia", "Felszerelés", "Egyéb"],
        "Egyéb": ["Egyéb"]
    },
    "ukrajinski": {
        "Біле м'ясо": ["Курятина", "Індичка", "Гуска", "Качка", "Інше"],
        "Червоне м'ясо": ["Свинина", "Ягнятина", "Баранина", "Телятина", "Яловичина", "Бичатина", "Конина", "Кролик", "Інше"],
        "Дрібна дичина": ["Перепілка", "Фазан", "Куріпка", "Дика качка", "Дика гуска", "Заєць", "Голуб", "Інше"],
        "Велика дичина": ["Олень", "Косуля", "Козуль", "Лось", "Північний олень", "Дикий кабан", "Бізон", "Верблюд", "Лама", "Альпака", "Кенгуру", "Крокодил/Алігатор", "Ящірка", "Змія", "Інше"],
        "Риба": ["Морська", "Прісноводна", "Морепродукти", "Інше"],
        "Молочні продукти": ["Молоко", "Молочні переробки", "Інше"],
        "Овочі": ["Свіжі", "Термічно оброблені", "Заморожені", "Інше"],
        "Консервація та компоти": ["Фрукти", "Овочі", "Інше"],
        "Тісто та Солодощі": ["Тісто", "Солодощі", "Інше"],
        "Напої": ["Вода", "Вино", "Сік", "Міцні напої", "Пиво", "Інше"],
        "Хімія та гігієна": ["Санітарія", "Особиста гігієна", "Приладдя", "Інше"],
        "Інше": ["Інше"]
    },
    "ruski": {
        "Белое мясо": ["Курица", "Индейка", "Гусь", "Утка", "Другое"],
        "Красное мясо": ["Свинина", "Баранина", "Овца", "Телятина", "Говядина", "Бык", "Конина", "Кролик", "Другое"],
        "Мелкая дичь": ["Перепел", "Фазан", "Куропатка", "Дикая утка", "Дикий гусь", "Заяц", "Голубь", "Другое"],
        "Крупная дичь": ["Олень", "Косуля", "Дикая коза", "Лось", "Северный олень", "Кабан", "Бизон", "Верблюд", "Лама", "Альпака", "Кенгуру", "Крокодил/Аллигатор", "Ящерица", "Змея", "Другое"],
        "Рыба": ["Морская", "Пресноводная", "Морепродукты", "Другое"],
        "Молочные продукты": ["Молоко", "Молочные переработки", "Другое"],
        "Овощи": ["Свежие", "Термически обработанные", "Замороженные", "Другое"],
        "Консервация и компоты": ["Фрукты", "Овощи", "Другое"],
        "Тесто и Сладости": ["Тесто", "Сладости", "Другое"],
        "Напитки": ["Вода", "Вино", "Сок", "Крепкие напитки", "Пиво", "Другое"],
        "Химия и гигиена": ["Сантехника", "Личная гигиена", "Оборудование", "Другое"],
        "Другое": ["Другое"]
    },
    "english": {
        "White meat": ["Chicken", "Turkey", "Goose", "Duck", "Other"],
        "Red meat": ["Pork", "Lamb", "Sheep", "Veal", "Beef", "Bull", "Horse", "Rabbit", "Other"],
        "Small game": ["Quail", "Pheasant", "Partridge", "Wild duck", "Wild goose", "Hare", "Pigeon", "Other"],
        "Big game": ["Deer", "Roe deer", "Wild goat", "Moose", "Reindeer", "Wild boar", "Bison", "Camel", "Llama", "Alpaca", "Kangaroo", "Crocodile/Alligator", "Lizard", "Snake", "Other"],
        "Fish": ["Sea", "Freshwater", "Seafood", "Other"],
        "Dairy products": ["Milk", "Dairy processing", "Other"],
        "Vegetables": ["Fresh", "Heat treated", "Frozen", "Other"],
        "Preserves and compotes": ["Fruits", "Vegetables", "Other"],
        "Dough and Sweets": ["Dough", "Sweets", "Other"],
        "Beverages": ["Water", "Wine", "Juice", "Spirits", "Beer", "Other"],
        "Chemicals and hygiene": ["Sanitary", "Personal hygiene", "Equipment", "Other"],
        "Other": ["Other"]
    },
    "deutsch": {
        "Weißes Fleisch": ["Huhn", "Truthahn", "Gans", "Ente", "Andere"],
        "Rotes Fleisch": ["Schwein", "Lamm", "Schaf", "Kalb", "Rind", "Bulle", "Pferd", "Kaninchen", "Andere"],
        "Kleinwild": ["Wachtel", "Fasan", "Rebhuhn", "Wildente", "Wildgans", "Hase", "Taube", "Andere"],
        "Großwild": ["Hirsch", "Reh", "Wildziege", "Elch", "Rentier", "Wildschwein", "Bison", "Kamel", "Lama", "Alpaka", "Känguru", "Krokodil/Alligator", "Eidechse", "Schlange", "Andere"],
        "Fisch": ["Meer", "Süßwasser", "Meeresfrüchte", "Andere"],
        "Milchprodukte": ["Milch", "Milchverarbeitung", "Andere"],
        "Gemüse": ["Frisch", "Wärmebehandelt", "Gefroren", "Andere"],
        "Konserven und Kompotte": ["Früchte", "Gemüse", "Andere"],
        "Teig und Süßigkeiten": ["Teig", "Süßigkeiten", "Andere"],
        "Getränke": ["Wasser", "Wein", "Saft", "Spirituosen", "Bier", "Andere"],
        "Chemie und Hygiene": ["Sanitär", "Persönliche Hygiene", "Ausrüstung", "Andere"],
        "Andere": ["Andere"]
    },
    "mandarinski": {
        "白肉": ["鸡", "火鸡", "鹅", "鸭", "其他"],
        "红肉": ["猪肉", "羊肉", "羊", "小牛肉", "牛肉", "公牛", "马肉", "兔肉", "其他"],
        "小型野味": ["鹌鹑", "野鸡", "鹧鸪", "野鸭", "野鹅", "野兔", "鸽子", "其他"],
        "大型野味": ["鹿", "狍子", "野山羊", "驼鹿", "驯鹿", "野猪", "野牛", "骆驼", "羊驼", "袋鼠", "鳄鱼", "蜥蜴", "蛇", "其他"],
        "鱼": ["海鱼", "淡水鱼", "海鲜", "其他"],
        "乳制品": ["牛奶", "乳制品加工", "其他"],
        "蔬菜": ["新鲜", "热处理", "冷冻", "其他"],
        "蜜饯和蜜饯": ["水果", "蔬菜", "其他"],
        "面团和糖果": ["面团", "糖果", "其他"],
        "饮料": ["水", "葡萄酒", "果汁", "烈酒", "啤酒", "其他"],
        "化学品和卫生": ["卫生", "个人卫生", "设备", "其他"],
        "其他": ["其他"]
    },
    "espanol": {
        "Carne blanca": ["Pollo", "Pavo", "Ganso", "Pato", "Otro"],
        "Carne roja": ["Cerdo", "Cordero", "Oveja", "Ternera", "Res", "Toro", "Caballo", "Conejo", "Otro"],
        "Caza menor": ["Codorniz", "Faisán", "Perdiz", "Pato salvaje", "Ganso salvaje", "Liebre", "Paloma", "Otro"],
        "Caza mayor": ["Ciervo", "Corzo", "Cabra salvaje", "Alce", "Reno", "Jabalí", "Bisonte", "Camello", "Llama", "Alpaca", "Canguro", "Cocodrilo/Caimán", "Lagarto", "Serpiente", "Otro"],
        "Pescado": ["Mar", "Agua dulce", "Mariscos", "Otro"],
        "Productos lácteos": ["Leche", "Procesamiento lácteo", "Otro"],
        "Verduras": ["Frescas", "Tratadas térmicamente", "Congeladas", "Otro"],
        "Conservas y compotas": ["Frutas", "Verduras", "Otro"],
        "Masa y Dulces": ["Masa", "Dulces", "Otro"],
        "Bebidas": ["Agua", "Vino", "Jugo", "Licores", "Cerveza", "Otro"],
        "Química e higiene": ["Sanitario", "Higiene personal", "Equipo", "Otro"],
        "Otro": ["Otro"]
	},
	"portugalski": {
		"Carne branca": ["Frango", "Peru", "Ganso", "Pato", "Outro"],
		"Carne vermelha": ["Porco", "Cordeiro", "Ovelha", "Vitela", "Boi", "Touro", "Cavalo", "Coelho", "Outro"],
		"Caça pequena": ["Codorna", "Faisão", "Perdiz", "Pato selvagem", "Ganso selvagem", "Lebre", "Pombo", "Outro"],
		"Caça grossa": ["Cervo", "Corça", "Cabra selvagem", "Alce", "Rena", "Javali", "Bisão", "Camelo", "Lhama", "Alpaca", "Canguru", "Crocodilo/Jacaré", "Lagarto", "Cobra", "Outro"],
		"Peixe": ["Mar", "Água doce", "Frutos do mar", "Outro"],
		"Laticínios": ["Leite", "Processamento de leite", "Outro"],
		"Vegetais": ["Fresco", "Tratado termicamente", "Congelado", "Outro"],
		"Conservas e compotas": ["Frutas", "Vegetais", "Outro"],
		"Massa e Doces": ["Massa", "Doces", "Outro"],
		"Bebidas": ["Água", "Vinho", "Suco", "Bebidas destiladas", "Cerveja", "Outro"],
		"Química e higiene": ["Sanitário", "Higiene pessoal", "Equipamento", "Outro"],
		"Outro": ["Outro"]
	},
    "francais": {
        "Viande blanche": ["Poulet", "Dinde", "Oie", "Canard", "Autre"],
        "Viande rouge": ["Porc", "Agneau", "Mouton", "Veau", "Bœuf", "Taureau", "Cheval", "Lapin", "Autre"],
        "Petit gibier": ["Caille", "Faisan", "Perdrix", "Canard sauvage", "Oie sauvage", "Lièvre", "Pigeon", "Autre"],
        "Gros gibier": ["Cerf", "Chevreuil", "Chèvre sauvage", "Élan", "Renne", "Sanglier", "Bison", "Chameau", "Lama", "Alpaga", "Kangourou", "Crocodile/Alligator", "Lézard", "Serpent", "Autre"],
        "Poisson": ["Mer", "Eau douce", "Fruits de mer", "Autre"],
        "Produits laitiers": ["Lait", "Transformation laitière", "Autre"],
        "Légumes": ["Frais", "Traité thermiquement", "Congelé", "Autre"],
        "Conserves et compotes": ["Fruits", "Légumes", "Autre"],
        "Pâte et Sucreries": ["Pâte", "Sucreries", "Autre"],
        "Boissons": ["Eau", "Vin", "Jus", "Spiritueux", "Bière", "Autre"],
        "Chimie et hygiène": ["Sanitaire", "Hygiène personnelle", "Équipement", "Autre"],
        "Autre": ["Autre"]
    }
}

# DELOVI PROIZVODA NA SVIM JEZICIMA
product_parts_translations = {
    "srpski": {
        # --- Belo meso ---
        "Pileće": ["Gril pile", "Pile celo", "Ceo batak", "Karabatak", "Donji batak", "Belo (grudi)", "File", "Leđa", "Krilca", "Medaljoni", "Nugati", "Panirani odrezak", "Mleveno", "Za supu", "Ostalo"],
        "Ćureće": ["Ceo batak", "Karabatak", "Donji batak", "Rolovani batak", "Odresci od bataka", "Belo (grudi)", "Krilca", "Leđa", "Krila", "Za supu", "Mleveno", "Ostalo"],
        "Guska": ["Belo (grudi)", "Ceo batak", "Karabatak", "Donji batak", "Krilca", "Leđa", "Vrat", "Jetra (foie gras)", "Gušćja mast", "Mleveno", "Za supu", "Ostalo"],
        "Patka": ["Belo (grudi)", "Ceo batak", "Karabatak", "Donji batak", "Krilca", "Leđa", "Vrat", "Pačija mast", "Mleveno", "Jetra", "Za supu", "Ostalo"],

        # --- Crveno meso ---
        "Svinjsko": ["Šnicla", "Karmenadla", "Vrat", "But", "Kare", "Rebra", "Grudi", "Plećka", "Podplećka", "Kolenica", "Mleveno", "Usitnjen", "Za supu", "Ostalo"],
        "Jagnjeće": ["Glava", "Vrat", "Plećka", "Slabine", "Grudi", "Bubrežnjak", "But", "Kolenica", "Ostalo"],
        "Ovčije": ["Glava", "Vrat", "Plećka", "Slabine", "Grudi", "Bubrežnjak", "But", "Kolenica", "Ostalo"],
        "Juneće": ["Biftek", "Vrat - zaplecak", "Prsa", "Lopatica", "Kolenica", "Rebra", "Potrbušina", "T-bone steak", "Ramstek", "Rib-Eye", "Rep", "Ostalo"],
        "Govedina": ["Karmedla", "Biftek", "Vrat", "Podplećka", "Grudi", "Kolenica", "Rebra", "Slabine", "Leđa", "Trbušina", "But", "Ostalo"],
        "Od bika": ["But", "Plećka", "Kare (leđa)", "Prsa i rebra", "Lopatica", "Vrat", "Slabina", "Rep", "Ostalo"],
        "Konjsko": ["But", "Plećka", "Kare (leđa)", "Vrat", "Prsa i rebra", "Biftek", "Ramstek", "Mleveno meso", "Ostalo"],
        "Zečije": ["Zadnji but", "Prednji but", "File (leđa)", "Rebra", "Ostalo"],

        # --- Sitna divljač ---
        "Prepelica": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Fazan": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Jarebica": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Golub": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Divlji zec": ["Zadnji but", "Prednji but", "File (leđa)", "Rebra", "Ostalo"],
        "Divlja patka": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],
        "Divlja guska": ["Celo meso", "Grudi (fileti)", "Bataci", "Jetra", "Ostalo"],

        # --- Krupna divljač ---
        "Jelen": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Srna": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Divokoza": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Irvas": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Los": ["But", "File (leđa)", "Biftek", "Rebra", "Grudi", "Plećka", "Kolenica", "Usitnjeno", "Ostalo"],
        "Divlja svinja": ["But", "Plećka", "Rebra", "Slanina", "Kolenica", "Vrat", "Glava", "Ostalo"],
        "Bizon": ["But", "Plećka", "Biftek", "Ramstek", "Rebra", "Slabina", "Vrat", "Kolenica", "Ostalo"],
        "Kamila": ["But", "Plećka", "File (slabine)", "File (leđa)", "Rebra", "Grudi", "Vrat", "Grba", "Ostalo"],
        "Lama": ["But", "Plećka", "File (leđa i slabine)", "Rebra", "Vrat", "Ostalo"],
        "Alpaka": ["But", "Plećka", "File (leđa i slabine)", "Rebra", "Vrat", "Ostalo"],
        "Kengur": ["But", "Plećka", "File (leđa i slabine)", "Rebra", "Rep", "Ostalo"],
        "Krokodil/Aligator": ["Rep", "File (leđa)", "Butine", "Ostalo"],
        "Zmija": ["Trup (prstenovi)", "Ostalo"],
        "Gušter": ["Rep", "Leđa", "Butine", "Ostalo"],

        # --- Riba ---
        "Morska": ["Losos", "Tuna", "Sardina", "Bakalar", "Oslić", "Skuša", "Brancin", "Orada", "Halibut", "Haringa", "Inćuni", "Kirnja", "Ostalo"],
        "Slatkovodna": ["Šaran", "Pastrmka", "Som", "Grgeč", "Smuđ", "Tilapija", "Pangasijus", "Jesetra", "Štuka", "Beli amur", "Pirarukus", "Ostalo"],
        "Plodovi mora": ["Škampi", "Sipa", "Jakobove kapice", "Venerina školjka", "Dagnje", "Kamenice", "Školjke", "Rak", "Hobotnica", "Lignja", "Morski ježevi", "Morski krastavci", "Abalone", "Ostalo"],

        # --- Mlečni proizvodi ---
        "Mleko": ["Mleko", "Kefir", "Kisela pavlaka", "Slatka pavlaka", "Pavlaka za kuvanje", "Ostalo"],
        "Mlečne prerađevine": ["Urda", "Mladi sir", "Krem sir", "Gouda", "Edamer", "Trapist", "Kačkavalj", "Parmezan", "Gorgonzola", "Rokfor", "Halloumi", "Ostalo"],

        # --- Povrće ---
        "Sveže": ["Grašak", "Boranija", "Karfiol", "Brokoli", "Bundeva", "Paradajz", "Krastavac", "Paprika", "Ostalo"],
        "Termički obrađeno": ["Grašak", "Boranija", "Kukuruz", "Karfiol", "Brokoli", "Paprika", "Tikvice", "Spanać", "Ostalo"],
        "Zamrznuto": ["Grašak", "Boranija", "Kukuruz", "Karfiol", "Brokoli", "Paprika", "Tikvice", "Spanać", "Ostalo"],

        # --- Zimnica i kompoti ---
        "Voće": ["Kajsija", "Kruška", "Višnja", "Pekmez od jagoda", "Šljivov pekmez", "Trešnja", "Pekmez od malina", "Dunja", "Ananas", "Pekmez od manga", "Ostalo"],
        "Povrće": ["Kiseli krastavci", "Kisela paprika", "Paradajz pire", "Cvekla", "Ajvar", "Turšija", "Kiseli kupus", "Ostalo"],

        # --- Testo i Slatkiši ---
        "Testo": ["Hleb", "Raženi hleb", "Čabata", "Kukuruzni hleb", "Baguette", "Pšenično brašno", "Integralno brašno", "Heljdino brašno", "Pirinčano brašno", "Začini", "Ostalo"],
        "Slatkiši": ["Kolači", "Torte", "Peciva", "Sladoled", "Čokolada", "Bombone", "Ostalo"],

        # --- Pića ---
        "Voda": ["Mineralna", "Negazirana", "Gazirana", "Ostalo"],
        "Vino": ["Crno", "Belo", "Roze", "Ostalo"],
        "Sok": ["Voćni", "Povrtni", "Ostalo"],
        "Žestoka pića": ["Rakija", "Votka", "Viski", "Ostalo"],
        "Pivo": ["Tamno", "Svetlo", "Ostalo"],

        # --- Hemija i higijena ---
        "Sanitar": ["Pranje prozora", "Pranje posuđa", "Pranje podova", "Sredstvo za kupatilo", "Ostalo"],
        "Lična higijena": ["Dezodorans", "Brijač", "Šminka", "Sapun", "Šampon", "Krema", "Ostalo"],
        "Pribor": ["Kantica", "Kofa", "Krpa za prašinu", "Metla", "Ostalo"],
        
        # --- Ostalo ---
        "Ostalo": ["Napomena: Unesite naziv proizvoda"]
    },
    "hungary": {
        # --- Fehér hús ---
        "Csirke": ["Grillcsirke", "Egész csirke", "Egész comb", "Comb filé", "Alsó comb", "Fehér hús (mell)", "Filé", "Hát", "Szárny", "Medál", "Nugget", "Rántott szelet", "Darált", "Leveshez", "Egyéb"],
        "Pulyka": ["Egész comb", "Comb filé", "Alsó comb", "Tekercs comb", "Comb szeletek", "Fehér hús (mell)", "Szárny", "Hát", "Szárnyak", "Leveshez", "Darált", "Egyéb"],
        "Libacomb": ["Fehér hús (mell)", "Egész comb", "Comb filé", "Alsó comb", "Szárny", "Hát", "Nyak", "Májas pástétom", "Libazsír", "Darált", "Leveshez", "Egyéb"],
        "Kacsa": ["Fehér hús (mell)", "Egész comb", "Comb filé", "Alsó comb", "Szárny", "Hát", "Nyak", "Kacsazsír", "Darált", "Máj", "Leveshez", "Egyéb"],

        # --- Vörös hús ---
        "Sertéshús": ["Szelet", "Karfiol", "Nyak", "Comb", "Szűzérme", "Borda", "Mell", "Lapocka", "Karakas", "Csülök", "Darált", "Apróra vágott", "Leveshez", "Egyéb"],
        "Bárányhús": ["Fej", "Nyak", "Lapocka", "Gerinc", "Mell", "Vese", "Comb", "Csülök", "Egyéb"],
        "Juhhús": ["Fej", "Nyak", "Lapocka", "Gerinc", "Mell", "Vese", "Comb", "Csülök", "Egyéb"],
        "Borjúhús": ["Bifsztek", "Nyak - tarja", "Mell", "Lapocka", "Csülök", "Borda", "Has", "T-bone steak", "Rump steak", "Rib-Eye", "Farok", "Egyéb"],
        "Marhahús": ["Roston sült", "Bifsztek", "Nyak", "Karakas", "Mell", "Csülök", "Borda", "Gerinc", "Hát", "Has", "Comb", "Egyéb"],
        "Bikahús": ["Comb", "Lapocka", "Szűzérme (hát)", "Mell és borda", "Lapocka", "Nyak", "Ágyék", "Farok", "Egyéb"],
        "Lóhús": ["Comb", "Lapocka", "Szűzérme (hát)", "Nyak", "Mell és borda", "Bifsztek", "Rump steak", "Darált hús", "Egyéb"],
        "Nyúlhús": ["Hátsó comb", "Elülső comb", "Filé (hát)", "Borda", "Egyéb"],

        # --- Apróvad ---
        "Fürj": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Fácán": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Fogoly": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Galamb": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Vadnyúl": ["Hátsó comb", "Elülső comb", "Filé (hát)", "Borda", "Egyéb"],
        "Vadkacsa": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],
        "Vadliba": ["Egész hús", "Mell (filék)", "Combok", "Máj", "Egyéb"],

        # --- Nagy vad ---
        "Szarvac": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Őz": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Vadkecske": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Jávorszarvas": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Rénszarvas": ["Comb", "Filé (hát)", "Bifsztek", "Borda", "Mell", "Lapocka", "Csülök", "Apróra vágott", "Egyéb"],
        "Vadkan": ["Comb", "Lapocka", "Borda", "Szalonna", "Csülök", "Nyak", "Fej", "Egyéb"],
        "Bölény": ["Comb", "Lapocka", "Bifsztek", "Rump steak", "Borda", "Ágyék", "Nyak", "Csülök", "Egyéb"],
        "Teve": ["Comb", "Lapocka", "Filé (ágyék)", "Filé (hát)", "Borda", "Mell", "Nyak", "Púp", "Egyéb"],
        "Láma": ["Comb", "Lapocka", "Filé (hát és ágyék)", "Borda", "Nyak", "Egyéb"],
        "Alpaka": ["Comb", "Lapocka", "Filé (hát és ágyék)", "Borda", "Nyak", "Egyéb"],
        "Kenguru": ["Comb", "Lapocka", "Filé (hát és ágyék)", "Borda", "Farok", "Egyéb"],
        "Krokodil/Alligátor": ["Farok", "Filé (hát)", "Combok", "Egyéb"],
        "Gyík": ["Farok", "Hát", "Combok", "Egyéb"],
        "Kígyó": ["Törzs (gyűrűk)", "Egyéb"],

        # --- Hal ---
        "Tengeri": ["Lazac", "Tonhal", "Szardínia", "Tőkehal", "Tőkehal", "Makréla", "Fogas", "Aranysügér", "Laposhal", "Herring", "Szardella", "Tőkehal", "Egyéb"],
        "Édesvízi": ["Ponty", "Pisztráng", "Harcsa", "Kárász", "Sügér", "Tilápia", "Pangász", "Tok", "Csuka", "Fehér amur", "Arapaima", "Egyéb"],
        "Tenger gyümölcsei": ["Garnéla", "Tintahal", "Kagyló", "Kagyló", "Kagyló", "Kagyló", "Kagyló", "Rák", "Polip", "Lília", "Tengeri sün", "Tengeri uborka", "Abalone", "Egyéb"],

        # --- Tejtermékek ---
        "Tej": ["Tej", "Kefir", "Tejföl", "Tejszín", "Főzőtejszín", "Egyéb"],
        "Tejfeldolgozások": ["Túró", "Friss sajt", "Krémsajt", "Gouda", "Edami", "Trappista", "Kaskavál", "Parmezán", "Gorgonzola", "Roquefort", "Halloumi", "Egyéb"],

        # --- Zöldség ---
        "Friss": ["Borsó", "Zöldbab", "Karfiol", "Brokkoli", "Tök", "Paradicsom", "Uborka", "Paprika", "Egyéb"],
        "Hőkezelt": ["Borsó", "Zöldbab", "Kukorica", "Karfiol", "Brokkoli", "Paprika", "Cukkini", "Spenót", "Egyéb"],
        "Fagyasztott": ["Borsó", "Zöldbab", "Kukorica", "Karfiol", "Brokkoli", "Paprika", "Cukkini", "Spenót", "Egyéb"],

        # --- Befőttek és kompótok ---
        "Gyümölcs": ["Sárgabarack", "Körte", "Cseresznye", "Epres lekvár", "Szilvalekvár", "Cseresznye", "Málnalekvár", "Birsalma", "Ananász", "Mangó lekvár", "Egyéb"],
        "Zöldség": ["Savanyú uborka", "Savanyú paprika", "Paradicsompüré", "Cékla", "Ajvár", "Savanyúság", "Savanyú káposzta", "Egyéb"],

        # --- Tészta és Édességek ---
        "Tészta": ["Kenyér", "Rozskenyér", "Ciabatta", "Kukoricalepény", "Baguette", "Búzaliszt", "Teljes kiőrlésű liszt", "Hajdinaliszt", "Rizsliszt", "Fűszerek", "Egyéb"],
        "Édességek": ["Sütemények", "Torták", "Pékáru", "Fagylalt", "Csokoládé", "Cukorkák", "Egyéb"],

        # --- Italok ---
        "Víz": ["Ásványvíz", "Szénsavmentes", "Szénsavas", "Egyéb"],
        "Bor": ["Vörös", "Fehér", "Rozé", "Egyéb"],
        "Lé": ["Gyümölcslé", "Zöldséglé", "Egyéb"],
        "Tömény italok": ["Pálinka", "Vodka", "Whisky", "Egyéb"],
        "Sör": ["Barna", "Világos", "Egyéb"],

        # --- Kémia és higiénia ---
        "WC": ["Ablaktisztító", "Mosogatószer", "Padlótisztító", "Fürdőszobai tisztítószer", "Egyéb"],
        "Személyes higiénia": ["Dezodor", "Borotva", "Smink", "Szappan", "Sampon", "Krém", "Egyéb"],
        "Felszerelés": ["Vödör", "Vödör", "Poroló", "Seprű", "Egyéb"],

        # --- Egyéb ---
        "Egyéb": ["Megjegyzés: Írja be a termék nevét"]
    },
    "ukrajinski": {
        # --- Біле м'ясо ---
        "Курятина": ["Ціла курка", "Грудка", "Стегно", "Гомілка", "Крило", "Філе", "Спина", "Медальйони", "Нагетси", "Панірований шніцель", "Фарш", "Для супу", "Інше"],
        "Індичка": ["Ціла індичка", "Грудка", "Стегно", "Крило", "Філе", "Спина", "Медальйони", "Для супу", "Фарш", "Інше"],
        "Гуска": ["Ціла гуска", "Грудка", "Стегно", "Крило", "Спина", "Шия", "Печінка", "Гусячий жир", "Фарш", "Для супу", "Інше"],
        "Качка": ["Ціла качка", "Грудка", "Стегно", "Крило", "Спина", "Шия", "Качиний жир", "Печінка", "Фарш", "Для супу", "Інше"],
        
        # --- Червоне м'ясо ---
        "Свинина": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Шинка", "Фарш", "Для супу", "Інше"],
        "Ягнятина": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Яловичина": ["Філей", "Стейк", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Телятина": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Кролик": ["Задні лапи", "Передні лапи", "Спинка", "Ребра", "Для супу", "Інше"],
        
        # --- Дрібна дичина ---
        "Перепілка": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Фазан": ["Цілий", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Куріпка": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Голуб": ["Цілий", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Заєць": ["Задні лапи", "Передні лапи", "Спинка", "Ребра", "Інше"],
        "Дика качка": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        "Дика гуска": ["Ціла", "Грудка", "Гомілки", "Крила", "Печінка", "Інше"],
        
        # --- Велика дичина ---
        "Олень": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Косуля": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Дикий кабан": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Лось": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Північний олень": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Бізон": ["Філе", "Стейк", "Окост", "Шия", "Лопатка", "Грудинка", "Ребра", "Голяшка", "Фарш", "Для супу", "Інше"],
        "Верблюд": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Горб", "Ребра", "Фарш", "Для супу", "Інше"],
        "Лама": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Ребра", "Фарш", "Для супу", "Інше"],
        "Альпака": ["Філе", "Котлета", "Окост", "Шия", "Лопатка", "Ребра", "Фарш", "Для супу", "Інше"],
        "Кенгуру": ["Філе", "Стейк", "Окост", "Шия", "Лопатка", "Хвіст", "Фарш", "Для супу", "Інше"],
        "Крокодил/Алігатор": ["Хвіст", "Філе", "Гомілки", "Інше"],
        "Ящірка": ["Хвіст", "Спина", "Гомілки", "Інше"],
        "Змія": ["Кільця", "Інше"],
        
        # --- Риба ---
        "Морська": ["Філе", "Стейк", "Ціла риба", "Філе зі шкірою", "Філе без шкіри", "Шматки", "Для супу", "Інше"],
        "Прісноводна": ["Філе", "Стейк", "Ціла риба", "Філе зі шкірою", "Філе без шкіри", "Шматки", "Для супу", "Інше"],
        "Морепродукти": ["Креветки", "Кальмар", "Мідії", "Устриці", "Гребінці", "Краби", "Восьминіг", "Каракатиця", "Інше"],
        
        # --- Молочні продукти ---
        "Молоко": ["Цільне", "Знежирене", "Пастеризоване", "Стерилізоване", "Кип'ячене", "Згущене", "Сухе", "Інше"],
        "Молочні переробки": ["Сир", "Сир домашній", "Сметана", "Йогурт", "Кефір", "Масло", "Сирний крем", "Інше"],
        
        # --- Овочі ---
        "Свіжі": ["Цілі", "Нарізані", "Виміті", "Очищені", "Терті", "Інше"],
        "Термічно оброблені": ["Варені", "Тушковані", "Смажені", "Запечені", "Приготовані на пару", "Інше"],
        "Заморожені": ["Цілі", "Нарізані", "Суміш", "Пюре", "Інше"],
        
        # --- Фрукти ---
        "Фрукти": ["Цілі", "Нарізані", "Очищені", "Без кісточок", "Консервовані", "Сушені", "Інше"],
        
        # --- Тісто та Солодощі ---
        "Тісто": ["Дріжджове", "Пісочне", "Листкове", "Для млинців", "Для піци", "Для макарон", "Інше"],
        "Солодощі": ["Шоколад", "Цукерки", "Печиво", "Торти", "Випічка", "Морозиво", "Вафлі", "Інше"],
        
        # --- Напої ---
        "Вода": ["Газована", "Негазована", "Мінеральна", "Ароматизована", "Інше"],
        "Вино": ["Червоне", "Біле", "Рожеве", "Ігристe", "Солодке", "Сухе", "Напівсухе", "Інше"],
        "Сік": ["Яблучний", "Апельсиновий", "Виноградний", "Томатний", "Мультифрукт", "З м'якоттю", "Без м'якоті", "Інше"],
        "Міцні напої": ["Горілка", "Віскі", "Коньяк", "Ром", "Джин", "Текіла", "Лікер", "Інше"],
        "Пиво": ["Світле", "Темне", "Пшеничне", "Крафтове", "Безалкогольне", "Інше"],
        
        # --- Хімія та гігієна ---
        "Санітарія": ["Для ванної", "Для туалету", "Для умивальника", "Універсальний", "Антибактеріальний", "Інше"],
        "Особиста гігієна": ["Мило", "Шампунь", "Гель для душу", "Дезодорант", "Зубна паста", "Бритва", "Крем", "Інше"],
        "Приладдя": ["Відро", "Швабра", "Ганчірка", "Губка", "Щітка", "Рукавиці", "Інше"],
        
        "Інше": ["Примітка: введіть назву продукту"]
    },

    "ruski": {
        # --- Белое мясо ---
        "Курица": ["Целая курица", "Грудка", "Бедро", "Голень", "Крыло", "Филе", "Спина", "Медальоны", "Наггетсы", "Панированное", "Фарш", "Для супа", "Другое"],
        "Индейка": ["Целая индейка", "Грудка", "Бедро", "Голень", "Крыло", "Филе", "Спина", "Медальоны", "Для супа", "Фарш", "Другое"],
        "Гусь": ["Целая гусь", "Грудка", "Бедро", "Голень", "Крыло", "Спина", "Шея", "Печень", "Гусиный жир", "Фарш", "Для супа", "Другое"],
        "Утка": ["Целая утка", "Грудка", "Бедро", "Голень", "Крыло", "Спина", "Шея", "Утиный жир", "Печень", "Фарш", "Для супа", "Другое"],
        
        # --- Красное мясо ---
        "Свинина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Подплечный край", "Фарш", "Для супа", "Другое"],
        "Баранина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Телятина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Говядина": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Кролик": ["Задние лапы", "Передние лапы", "Спинка", "Ребра", "Для супа", "Другое"],
        
        # --- Мелкая дичь ---
        "Перепел": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Фазан": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Куропатка": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Голубь": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Заяц": ["Задние лапы", "Передние лапы", "Спинка", "Ребра", "Другое"],
        "Дикая утка": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        "Дикий гусь": ["Целая тушка", "Грудка", "Бедра", "Крылья", "Печень", "Другое"],
        
        # --- Крупная дичь ---
        "Олень": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Косуля": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Кабан": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        "Лось": ["Вырезка", "Корейка", "Окорок", "Шея", "Лопатка", "Грудинка", "Ребра", "Рулька", "Фарш", "Для супа", "Другое"],
        
        # --- Рыба ---
        "Морская": ["Филе", "Стейк", "Целая рыба", "Филе с кожей", "Филе без кожи", "Филе на коже", "Куски", "Для супа", "Другое"],
        "Пресноводная": ["Филе", "Стейк", "Целая рыба", "Филе с кожей", "Филе без кожи", "Филе на коже", "Куски", "Для супа", "Другое"],
        "Морепродукты": ["Креветки", "Кальмары", "Мидии", "Устрицы", "Гребешки", "Крабы", "Осьминоги", "Каракатицы", "Другое"],
        
        # --- Молочные продукты ---
        "Молоко": ["Цельное", "Обезжиренное", "Пастеризованное", "Стерилизованное", "Топленое", "Сгущенное", "Сухое", "Другое"],
        "Молочные переработки": ["Сыр", "Творог", "Сметана", "Йогурт", "Кефир", "Ряженка", "Сливочное масло", "Творожный сыр", "Другое"],
        
        # --- Овощи ---
        "Свежие": ["Целые", "Нарезанные", "Вымытые", "Чищенные", "Натертые", "Другое"],
        "Термически обработанные": ["Вареные", "Тушеные", "Жареные", "Запеченные", "Приготовленные на пару", "Другое"],
        "Замороженные": ["Целые", "Нарезанные", "Смесь", "Пюре", "Другое"],
        
        # --- Фрукты ---
        "Фрукты": ["Целые", "Нарезанные", "Очищенные", "Без косточек", "Консервированные", "Сушеные", "Другое"],
        
        # --- Тесто и сладости ---
        "Тесто": ["Дрожжевое", "Песочное", "Слоеное", "Блинное", "Для пиццы", "Для пасты", "Другое"],
        "Сладости": ["Шоколад", "Конфеты", "Печенье", "Торты", "Пирожные", "Мороженое", "Вафли", "Другое"],
        
        # --- Напитки ---
        "Вода": ["Газированная", "Негазированная", "Минеральная", "Ароматизированная", "Другое"],
        "Вино": ["Красное", "Белое", "Розовое", "Игристое", "Сладкое", "Сухое", "Полусухое", "Другое"],
        "Сок": ["Яблочный", "Апельсиновый", "Виноградный", "Томатный", "Мультифрукт", "С мякотью", "Без мякоти", "Другое"],
        "Крепкие напитки": ["Водка", "Виски", "Коньяк", "Ром", "Джин", "Текила", "Ликер", "Другое"],
        "Пиво": ["Светлое", "Темное", "Пшеничное", "Крафтовое", "Безалкогольное", "Другое"],
        
        # --- Химия и гигиена ---
        "Сантехника": ["Для ванной", "Для туалета", "Для раковины", "Универсальное", "Антибактериальное", "Другое"],
        "Личная гигиена": ["Мыло", "Шампунь", "Гель для душа", "Дезодорант", "Зубная паста", "Бритва", "Крем", "Другое"],
        "Оборудование": ["Ведро", "Швабра", "Тряпка", "Губка", "Щетка", "Перчатки", "Другое"],
        
        "Другое": ["Примечание: введите название продукта"]
    },

    "english": {
        # --- White meat ---
        "Chicken": ["Whole chicken", "Breast", "Thigh", "Drumstick", "Wing", "Filet", "Back", "Medallions", "Nuggets", "Breaded cutlet", "Minced meat", "For soup", "Other"],
        "Turkey": ["Whole turkey", "Breast", "Thigh", "Wing", "Filet", "Back", "Medallions", "For soup", "Minced meat", "Other"],
        "Goose": ["Whole goose", "Breast", "Thigh", "Wing", "Back", "Neck", "Liver", "Goose fat", "Minced meat", "For soup", "Other"],
        "Duck": ["Whole duck", "Breast", "Thigh", "Wing", "Back", "Neck", "Duck fat", "Liver", "Minced meat", "For soup", "Other"],
        
        # --- Red meat ---
        "Pork": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Ham", "Minced meat", "For soup", "Other"],
        "Lamb": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Minced meat", "For soup", "Other"],
        "Beef": ["Sirloin", "Steak", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Veal": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Minced meat", "For soup", "Other"],
        "Rabbit": ["Hind legs", "Front legs", "Saddle", "Ribs", "For soup", "Other"],
        
        # --- Small game ---
        "Quail": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Pheasant": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Partridge": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Pigeon": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Hare": ["Hind legs", "Front legs", "Saddle", "Ribs", "Other"],
        "Wild duck": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        "Wild goose": ["Whole", "Breast", "Legs", "Wings", "Liver", "Other"],
        
        # --- Big game ---
        "Deer": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Roe deer": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Wild boar": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Belly", "Ribs", "Hock", "Minced meat", "For soup", "Other"],
        "Moose": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Reindeer": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Bison": ["Loin", "Steak", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Shank", "Minced meat", "For soup", "Other"],
        "Camel": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Hump", "Minced meat", "For soup", "Other"],
        "Llama": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Minced meat", "For soup", "Other"],
        "Alpaca": ["Loin", "Chop", "Leg", "Neck", "Shoulder", "Brisket", "Ribs", "Minced meat", "For soup", "Other"],
        "Kangaroo": ["Loin", "Steak", "Leg", "Neck", "Shoulder", "Tail", "Minced meat", "For soup", "Other"],
        "Crocodile/Alligator": ["Tail", "Filet", "Legs", "Other"],
        "Lizard": ["Tail", "Back", "Legs", "Other"],
        "Snake": ["Body rings", "Other"],
        
        # --- Fish ---
        "Sea": ["Fillet", "Steak", "Whole fish", "Skin-on fillet", "Skinless fillet", "Pieces", "For soup", "Other"],
        "Freshwater": ["Fillet", "Steak", "Whole fish", "Skin-on fillet", "Skinless fillet", "Pieces", "For soup", "Other"],
        "Seafood": ["Shrimp", "Squid", "Mussels", "Oysters", "Scallops", "Crabs", "Octopus", "Cuttlefish", "Other"],
        
        # --- Dairy products ---
        "Milk": ["Whole", "Skimmed", "Pasteurized", "Sterilized", "Boiled", "Condensed", "Powder", "Other"],
        "Dairy processing": ["Cheese", "Cottage cheese", "Sour cream", "Yogurt", "Kefir", "Butter", "Cream cheese", "Other"],
        
        # --- Vegetables ---
        "Fresh": ["Whole", "Chopped", "Washed", "Peeled", "Grated", "Other"],
        "Heat treated": ["Boiled", "Stewed", "Fried", "Baked", "Steamed", "Other"],
        "Frozen": ["Whole", "Chopped", "Mixed", "Puree", "Other"],
        
        # --- Fruits ---
        "Fruits": ["Whole", "Sliced", "Peeled", "Seedless", "Canned", "Dried", "Other"],
        
        # --- Dough and Sweets ---
        "Dough": ["Yeast dough", "Shortcrust", "Puff pastry", "Pancake batter", "Pizza dough", "Pasta dough", "Other"],
        "Sweets": ["Chocolate", "Candy", "Cookies", "Cakes", "Pastries", "Ice cream", "Wafers", "Other"],
        
        # --- Beverages ---
        "Water": ["Sparkling", "Still", "Mineral", "Flavored", "Other"],
        "Wine": ["Red", "White", "Rosé", "Sparkling", "Sweet", "Dry", "Semi-dry", "Other"],
        "Juice": ["Apple", "Orange", "Grape", "Tomato", "Multifruit", "With pulp", "Without pulp", "Other"],
        "Spirits": ["Vodka", "Whisky", "Cognac", "Rum", "Gin", "Tequila", "Liqueur", "Other"],
        "Beer": ["Light", "Dark", "Wheat", "Craft", "Non-alcoholic", "Other"],
        
        # --- Chemicals and hygiene ---
        "Sanitary": ["For bathroom", "For toilet", "For sink", "Universal", "Antibacterial", "Other"],
        "Personal hygiene": ["Soap", "Shampoo", "Shower gel", "Deodorant", "Toothpaste", "Razor", "Cream", "Other"],
        "Equipment": ["Bucket", "Mop", "Cloth", "Sponge", "Brush", "Gloves", "Other"],
        
        "Other": ["Note: Enter product name"]
    },

    "deutsch": {
        # --- Weißes Fleisch ---
        "Huhn": ["Ganzes Huhn", "Brust", "Keule", "Flügel", "Filet", "Rücken", "Medaillons", "Nuggets", "Panierte Schnitzel", "Hackfleisch", "Für Suppe", "Andere"],
        "Truthahn": ["Ganzes Truthahn", "Brust", "Keule", "Flügel", "Filet", "Rücken", "Medaillons", "Für Suppe", "Hackfleisch", "Andere"],
        "Gans": ["Ganze Gans", "Brust", "Keule", "Flügel", "Rücken", "Hals", "Leber", "Gänseschmalz", "Hackfleisch", "Für Suppe", "Andere"],
        "Ente": ["Ganze Ente", "Brust", "Keule", "Flügel", "Rücken", "Hals", "Entenschmalz", "Leber", "Hackfleisch", "Für Suppe", "Andere"],
        
        # --- Rotes Fleisch ---
        "Schwein": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Schinken", "Hackfleisch", "Für Suppe", "Andere"],
        "Lamm": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Rind": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Kalbfleisch": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Kaninchen": ["Hinterläufe", "Vorderläufe", "Rücken", "Rippen", "Für Suppe", "Andere"],
        
        # --- Kleinwild ---
        "Wachtel": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Fasan": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Rebhuhn": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Taube": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Hase": ["Hinterläufe", "Vorderläufe", "Rücken", "Rippen", "Andere"],
        "Wildente": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        "Wildgans": ["Ganzes Tier", "Brust", "Keulen", "Flügel", "Leber", "Andere"],
        
        # --- Großwild ---
        "Hirsch": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Reh": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Wildschwein": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        "Elch": ["Filet", "Kotelett", "Keule", "Hals", "Schulter", "Brust", "Rippen", "Haxe", "Hackfleisch", "Für Suppe", "Andere"],
        
        # --- Fisch ---
        "Meer": ["Filet", "Steak", "Ganzer Fisch", "Filet mit Haut", "Filet ohne Haut", "Stücke", "Für Suppe", "Andere"],
        "Süßwasser": ["Filet", "Steak", "Ganzer Fisch", "Filet mit Haut", "Filet ohne Haut", "Stücke", "Für Suppe", "Andere"],
        "Meeresfrüchte": ["Garnelen", "Tintenfisch", "Muscheln", "Austern", "Jakobsmuscheln", "Krabben", "Tintenfisch", "Sepia", "Andere"],
        
        # --- Milchprodukte ---
        "Milch": ["Vollmilch", "Fettarme", "Pasteurisiert", "Sterilisiert", "Gekocht", "Kondensmilch", "Pulver", "Andere"],
        "Milchverarbeitung": ["Käse", "Hüttenkäse", "Sauerrahm", "Joghurt", "Kefir", "Butter", "Frischkäse", "Andere"],
        
        # --- Gemüse ---
        "Frisch": ["Ganz", "Geschnitten", "Gewaschen", "Geschält", "Geraspelt", "Andere"],
        "Erhitzt": ["Gekocht", "Gedünstet", "Gebraten", "Gebacken", "Gedämpft", "Andere"],
        "Gefroren": ["Ganz", "Geschnitten", "Mischung", "Püree", "Andere"],
        
        # --- Obst ---
        "Früchte": ["Ganz", "Geschnitten", "Geschält", "Kernlos", "Konserviert", "Getrocknet", "Andere"],
        
        # --- Teig und Süßigkeiten ---
        "Teig": ["Hefeteig", "Mürbeteig", "Blätterteig", "Pfannkuchenteig", "Pizzateig", "Pastateig", "Andere"],
        "Süßigkeiten": ["Schokolade", "Bonbons", "Kekse", "Kuchen", "Torten", "Eis", "Waffeln", "Andere"],
        
        # --- Getränke ---
        "Wasser": ["Sprudel", "Still", "Mineral", "Aromatisiert", "Andere"],
        "Wein": ["Rot", "Weiß", "Rosé", "Sekt", "Süß", "Trocken", "Halbtrocken", "Andere"],
        "Saft": ["Apfel", "Orange", "Traube", "Tomate", "Multifrucht", "Mit Fruchtfleisch", "Ohne Fruchtfleisch", "Andere"],
        "Spirituosen": ["Wodka", "Whisky", "Cognac", "Rum", "Gin", "Tequila", "Likör", "Andere"],
        "Bier": ["Hell", "Dunkel", "Weizen", "Craft", "Alkoholfrei", "Andere"],
        
        # --- Chemie und Hygiene ---
        "Sanitär": ["Für Bad", "Für Toilette", "Für Waschbecken", "Universal", "Antibakteriell", "Andere"],
        "Persönliche Hygiene": ["Seife", "Shampoo", "Duschgel", "Deodorant", "Zahnpasta", "Rasierer", "Creme", "Andere"],
        "Ausrüstung": ["Eimer", "Mop", "Tuch", "Schwamm", "Bürste", "Handschuhe", "Andere"],
        
        "Andere": ["Hinweis: Produktname eingeben"]
    },

    "mandarinski": {
        # --- 白肉 ---
        "鸡": ["整鸡", "鸡胸", "鸡腿", "鸡翅", "鸡柳", "鸡背", "鸡块", "鸡米花", "炸鸡排", "鸡绞肉", "汤用", "其他"],
        "火鸡": ["整火鸡", "火鸡胸", "火鸡腿", "火鸡翅", "火鸡柳", "火鸡背", "火鸡块", "汤用", "火鸡绞肉", "其他"],
        "鹅": ["整鹅", "鹅胸", "鹅腿", "鹅翅", "鹅背", "鹅颈", "鹅肝", "鹅油", "鹅绞肉", "汤用", "其他"],
        "鸭": ["整鸭", "鸭胸", "鸭腿", "鸭翅", "鸭背", "鸭颈", "鸭油", "鸭肝", "鸭绞肉", "汤用", "其他"],
        
        # --- 红肉 ---
        "猪肉": ["里脊", "排骨", "猪腿", "猪颈", "猪肩", "猪胸", "猪肋", "猪蹄", "猪绞肉", "汤用", "其他"],
        "羊肉": ["里脊", "排骨", "羊腿", "羊颈", "羊肩", "羊胸", "羊肋", "羊蹄", "羊绞肉", "汤用", "其他"],
        "牛肉": ["里脊", "牛排", "牛腿", "牛颈", "牛肩", "牛胸", "牛肋", "牛蹄", "牛绞肉", "汤用", "其他"],
        "兔肉": ["后腿", "前腿", "兔背", "兔肋", "汤用", "其他"],
        
        # --- 小型野味 ---
        "鹌鹑": ["整只", "鹌鹑胸", "鹌鹑腿", "鹌鹑翅", "鹌鹑肝", "其他"],
        "野鸡": ["整只", "野鸡胸", "野鸡腿", "野鸡翅", "野鸡肝", "其他"],
        "鹧鸪": ["整只", "鹧鸪胸", "鹧鸪腿", "鹧鸪翅", "鹧鸪肝", "其他"],
        "鸽子": ["整只", "鸽子胸", "鸽子腿", "鸽子翅", "鸽子肝", "其他"],
        "野兔": ["后腿", "前腿", "兔背", "兔肋", "其他"],
        "野鸭": ["整只", "野鸭胸", "野鸭腿", "野鸭翅", "野鸭肝", "其他"],
        "野鹅": ["整只", "野鹅胸", "野鹅腿", "野鹅翅", "野鹅肝", "其他"],
        
        # --- 大型野味 ---
        "鹿": ["里脊", "鹿排", "鹿腿", "鹿颈", "鹿肩", "鹿胸", "鹿肋", "鹿蹄", "鹿绞肉", "汤用", "其他"],
        "狍子": ["里脊", "狍子排", "狍子腿", "狍子颈", "狍子肩", "狍子胸", "狍子肋", "狍子蹄", "狍子绞肉", "汤用", "其他"],
        "野猪": ["里脊", "野猪排", "野猪腿", "野猪颈", "野猪肩", "野猪胸", "野猪肋", "野猪蹄", "野猪绞肉", "汤用", "其他"],
        "驼鹿": ["里脊", "驼鹿排", "驼鹿腿", "驼鹿颈", "驼鹿肩", "驼鹿胸", "驼鹿肋", "驼鹿蹄", "驼鹿绞肉", "汤用", "其他"],
        
        # --- 鱼 ---
        "海鱼": ["鱼片", "鱼排", "整鱼", "带皮鱼片", "去皮鱼片", "鱼块", "汤用", "其他"],
        "淡水鱼": ["鱼片", "鱼排", "整鱼", "带皮鱼片", "去皮鱼片", "鱼块", "汤用", "其他"],
        "海鲜": ["虾", "鱿鱼", "蛤蜊", "牡蛎", "扇贝", "螃蟹", "章鱼", "墨鱼", "其他"],
        
        # --- 乳制品 ---
        "牛奶": ["全脂", "脱脂", "巴氏杀菌", "灭菌", "煮沸", "炼乳", "奶粉", "其他"],
        "乳制品加工": ["奶酪", "干酪", "酸奶油", "酸奶", "开菲尔", "黄油", "奶油奶酪", "其他"],
        
        # --- 蔬菜 ---
        "新鲜": ["整颗", "切片", "洗净", "去皮", "擦丝", "其他"],
        "热处理": ["煮熟", "炖煮", "油炸", "烘烤", "蒸煮", "其他"],
        "冷冻": ["整颗", "切片", "混合", "泥状", "其他"],
        
        # --- 水果 ---
        "水果": ["整颗", "切片", "去皮", "去核", "罐头", "干果", "其他"],
        
        # --- 面团和糖果 ---
        "面团": ["酵母面团", "酥皮面团", "千层酥皮", "煎饼面糊", "披萨面团", "意大利面团", "其他"],
        "糖果": ["巧克力", "糖果", "饼干", "蛋糕", "糕点", "冰淇淋", "华夫饼", "其他"],
        
        # --- 饮料 ---
        "水": ["气泡水", "静水", "矿泉水", "调味水", "其他"],
        "酒": ["红酒", "白酒", "桃红", "起泡酒", "甜酒", "干酒", "半干", "其他"],
        "果汁": ["苹果汁", "橙汁", "葡萄汁", "番茄汁", "混合果汁", "带果肉", "无果肉", "其他"],
        "烈酒": ["伏特加", "威士忌", "干邑", "朗姆酒", "金酒", "龙舌兰", "利口酒", "其他"],
        "啤酒": ["淡啤", "黑啤", "小麦啤", "精酿", "无酒精", "其他"],
        
        # --- 化学品和卫生 ---
        "卫生": ["浴室用", "厕所用", "洗手池用", "通用", "抗菌", "其他"],
        "个人卫生": ["肥皂", "洗发水", "沐浴露", "除臭剂", "牙膏", "剃须刀", "面霜", "其他"],
        "设备": ["桶", "拖把", "布", "海绵", "刷子", "手套", "其他"],
        
        "其他": ["注：输入产品名称"]
    },

    "espanol": {
        # --- Carne blanca ---
        "Pollo": ["Pollo entero", "Pechuga", "Muslo", "Ala", "Filete", "Espalda", "Medallones", "Nuggets", "Milanesa", "Carne molida", "Para sopa", "Otro"],
        "Pavo": ["Pavo entero", "Pechuga", "Muslo", "Ala", "Filete", "Espalda", "Medallones", "Para sopa", "Carne molida", "Otro"],
        "Ganso": ["Ganso entero", "Pechuga", "Muslo", "Ala", "Espalda", "Cuello", "Hígado", "Grasa de ganso", "Carne molida", "Para sopa", "Otro"],
        "Pato": ["Pato entero", "Pechuga", "Muslo", "Ala", "Espalda", "Cuello", "Grasa de pato", "Hígado", "Carne molida", "Para sopa", "Otro"],
        
        # --- Carne roja ---
        "Cerdo": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Jamón", "Carne molida", "Para sopa", "Otro"],
        "Cordero": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Res": ["Lomo", "Bistec", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Ternera": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Conejo": ["Patas traseras", "Patas delanteras", "Lomo", "Costillas", "Para sopa", "Otro"],
        
        # --- Caza menor ---
        "Codorniz": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Faisán": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Perdiz": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Paloma": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Liebre": ["Patas traseras", "Patas delanteras", "Lomo", "Costillas", "Otro"],
        "Pato salvaje": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        "Ganso salvaje": ["Entera", "Pechuga", "Muslos", "Alas", "Hígado", "Otro"],
        
        # --- Caza mayor ---
        "Ciervo": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Corzo": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Jabalí": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        "Alce": ["Lomo", "Chuleta", "Pierna", "Cuello", "Paleta", "Pecho", "Costilla", "Codillo", "Carne molida", "Para sopa", "Otro"],
        
        # --- Pescado ---
        "Mar": ["Filete", "Filete con piel", "Filete sin piel", "Entero", "Trozos", "Para sopa", "Otro"],
        "Agua dulce": ["Filete", "Filete con piel", "Filete sin piel", "Entero", "Trozos", "Para sopa", "Otro"],
        "Mariscos": ["Camarones", "Calamar", "Mejillones", "Ostras", "Vieiras", "Cangrejos", "Pulpo", "Sepia", "Otro"],
        
        # --- Productos lácteos ---
        "Leche": ["Entera", "Descremada", "Pasteurizada", "Esterilizada", "Hervida", "Condensada", "En polvo", "Otro"],
        "Procesamiento lácteo": ["Queso", "Requesón", "Crema agria", "Yogur", "Kéfir", "Mantequilla", "Queso crema", "Otro"],
        
        # --- Verduras ---
        "Frescas": ["Enteras", "Cortadas", "Lavadas", "Peladas", "Ralladas", "Otro"],
        "Tratadas térmicamente": ["Cocidas", "Estofadas", "Fritas", "Horneadas", "Al vapor", "Otro"],
        "Congeladas": ["Enteras", "Cortadas", "Mezcla", "Puré", "Otro"],
        
        # --- Frutas ---
        "Frutas": ["Enteras", "Cortadas", "Peladas", "Sin semillas", "Enlatadas", "Secas", "Otro"],
        
        # --- Masa y dulces ---
        "Masa": ["Levadura", "Quebrada", "Hojaldre", "Para panqueques", "Para pizza", "Para pasta", "Otro"],
        "Dulces": ["Chocolate", "Caramelos", "Galletas", "Pasteles", "Tortas", "Helado", "Wafles", "Otro"],
        
        # --- Bebidas ---
        "Agua": ["Con gas", "Sin gas", "Mineral", "Saborizada", "Otro"],
        "Vino": ["Tinto", "Blanco", "Rosado", "Espumoso", "Dulce", "Seco", "Semiseco", "Otro"],
        "Jugo": ["Manzana", "Naranja", "Uva", "Tomate", "Multifruta", "Con pulpa", "Sin pulpa", "Otro"],
        "Licores": ["Vodka", "Whisky", "Coñac", "Ron", "Ginebra", "Tequila", "Licor", "Otro"],
        "Cerveza": ["Clara", "Oscura", "Trigo", "Artesanal", "Sin alcohol", "Otro"],
        
        # --- Química e higiene ---
        "Sanitario": ["Para baño", "Para inodoro", "Para lavabo", "Universal", "Antibacterial", "Otro"],
        "Higiene personal": ["Jabón", "Champú", "Gel de baño", "Desodorante", "Pasta dental", "Maquinilla", "Crema", "Otro"],
        "Equipo": ["Cubo", "Trapeador", "Paño", "Esponja", "Cepillo", "Guantes", "Otro"],
        
        "Otro": ["Nota: Ingrese el nombre del producto"]
    },

	"portugalski": {
		"Frango": ["Frango grelhado", "Frango inteiro", "Coxa inteira", "Sobrecoxa", "Coxinha", "Peito", "Filé", "Costas", "Asas", "Medalhões", "Nuggets", "Bife empanado", "Moído", "Para sopa", "Outro"],
		"Peru": ["Coxa inteira", "Sobrecoxa", "Coxinha", "Coxa enrolada", "Bifes de coxa", "Peito", "Asas", "Costas", "Pontas de asa", "Para sopa", "Moído", "Outro"],
		"Ganso": ["Peito", "Sobrecoxa", "Coxinha", "Asas", "Costas", "Pescoço", "Fígado (foie gras)", "Banha de ganso", "Moído", "Para sopa", "Outro"],
		"Pato": ["Peito", "Sobrecoxa", "Coxinha", "Asas", "Costas", "Pescoço", "Banha de pato", "Moído", "Fígado", "Para sopa", "Outro"],
		"Porco": ["Bife", "Costeleta", "Pescoço", "Pernil", "Lombo", "Costelas", "Barriga", "Paleta", "Espádua", "Jarret", "Moído", "Picado", "Para sopa", "Outro"],
		"Cordeiro": ["Cabeça", "Pescoço", "Paleta", "Lombo", "Peito", "Rim", "Pernil", "Jarret", "Outro"],
		"Boi": ["Bife", "Pescoço", "Peito", "Paleta", "Jarret", "Costelas", "Fralda", "T-bone", "Alcatra", "Rib-eye", "Rabo", "Outro"],
		"Coelho": ["Perna traseira", "Perna dianteira", "Filé do lombo", "Costelas", "Outro"],
		# --- Sitna divljač ---
		"Codorna": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Faisão": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Perdiz": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Pato selvagem": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Ganso selvagem": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		"Lebre": ["Perna traseira", "Perna dianteira", "Filé do lombo", "Costelas", "Outro"],
		"Pombo": ["Carne inteira", "Peito (filés)", "Coxas", "Fígado", "Outro"],
		# --- Krupna divljač ---
		"Cervo": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Corça": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Cabra selvagem": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Alce": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Rena": ["Perna", "Filé (lombo)", "Bife", "Costelas", "Peito", "Paleta", "Jarrete", "Picado", "Outro"],
		"Javali": ["Perna", "Paleta", "Costelas", "Bacon", "Jarrete", "Pescoço", "Cabeça", "Outro"],
		"Bisão": ["Perna", "Paleta", "Bife", "Alcatra", "Costelas", "Lombo", "Pescoço", "Jarrete", "Outro"],
		"Camelo": ["Perna", "Paleta", "Filé (lombo)", "Filé (dorso)", "Costelas", "Peito", "Pescoço", "Corcova", "Outro"],
		"Lhama": ["Perna", "Paleta", "Filé (dorso e lombo)", "Costelas", "Pescoço", "Outro"],
		"Alpaca": ["Perna", "Paleta", "Filé (dorso e lombo)", "Costelas", "Pescoço", "Outro"],
		"Canguru": ["Perna", "Paleta", "Filé (dorso e lombo)", "Costelas", "Rabo", "Outro"],
		"Crocodilo/Jacaré": ["Rabo", "Filé (dorso)", "Coxas", "Outro"],
		"Lagarto": ["Rabo", "Dorso", "Coxas", "Outro"],
		"Cobra": ["Tronco (anéis)", "Outro"],
		"Mar": ["Salmão", "Atum", "Sardinha", "Bacalhau", "Pescada", "Cavala", "Robalo", "Dourada", "Linguado", "Arenque", "Anchova", "Outro"],
		"Água doce": ["Carpa", "Truta", "Bagre", "Percha", "Sander", "Tilápia", "Panga", "Esturjão", "Lúcio", "Carpa capim", "Pirarucu", "Outro"],
		"Frutos do mar": ["Camarão", "Lula", "Vieiras", "Amêijoas", "Mexilhões", "Ostras", "Caranguejo", "Polvo", "Ouriço", "Pepino do mar", "Abalone", "Outro"],
		"Leite": ["Leite", "Kefir", "Creme azedo", "Creme", "Creme de cozinha", "Outro"],
		"Processamento de leite": ["Queijo fresco", "Queijo jovem", "Queijo cremoso", "Gouda", "Edam", "Trappista", "Kashkaval", "Parmesão", "Gorgonzola", "Roquefort", "Halloumi", "Outro"],
		"Fresco": ["Ervilhas", "Feijão verde", "Couve-flor", "Brócolis", "Abóbora", "Tomate", "Pepino", "Pimentão", "Outro"],
		"Tratado termicamente": ["Ervilhas", "Feijão verde", "Milho", "Couve-flor", "Brócolis", "Pimentão", "Abobrinha", "Espinafre", "Outro"],
		"Congelado": ["Ervilhas", "Feijão verde", "Milho", "Couve-flor", "Brócolis", "Pimentão", "Abobrinha", "Espinafre", "Outro"],
		"Frutas": ["Damasco", "Pera", "Cereja", "Geleia de morango", "Geleia de ameixa", "Cereja doce", "Geleia de framboesa", "Marmelo", "Abacaxi", "Geleia de manga", "Outro"],
		"Vegetais": ["Picles", "Pimentão em conserva", "Purê de tomate", "Beterraba", "Ajvar", "Conservas", "Chucrute", "Outro"],
		"Massa": ["Pão", "Pão de centeio", "Ciabatta", "Pão de milho", "Baguete", "Farinha de trigo", "Farinha integral", "Farinha de trigo sarraceno", "Farinha de arroz", "Temperos", "Outro"],
		"Doces": ["Bolos", "Tortas", "Padaria", "Sorvete", "Chocolate", "Doces", "Outro"],
		"Água": ["Mineral", "Sem gás", "Com gás", "Outro"],
		"Vinho": ["Tinto", "Branco", "Rosé", "Outro"],
		"Suco": ["Fruta", "Vegetal", "Outro"],
		"Bebidas destiladas": ["Conhaque", "Vodka", "Uísque", "Outro"],
		"Cerveja": ["Escura", "Clara", "Outro"],
		"Sanitário": ["Limpa-vidros", "Detergente", "Limpa-pisos", "Limpa-banheiro", "Outro"],
		"Higiene pessoal": ["Desodorante", "Lâmina", "Maquiagem", "Sabão", "Xampu", "Creme", "Outro"],
		"Equipamento": ["Balde", "Pano", "Espanador", "Vassoura", "Outro"],
		"Outro": ["Nota: Digite o nome do produto"]
	},

    "francais": {
        # --- Viande blanche ---
        "Poulet": ["Poulet entier", "Poitrine", "Cuisse", "Aile", "Filet", "Dos", "Médaillons", "Nuggets", "Escalope panée", "Viande hachée", "Pour soupe", "Autre"],
        "Dinde": ["Dinde entière", "Poitrine", "Cuisse", "Aile", "Filet", "Dos", "Médaillons", "Pour soupe", "Viande hachée", "Autre"],
        "Oie": ["Oie entière", "Poitrine", "Cuisse", "Aile", "Dos", "Cou", "Foie", "Graisse d'oie", "Viande hachée", "Pour soupe", "Autre"],
        "Canard": ["Canard entier", "Magret", "Cuisse", "Aile", "Dos", "Cou", "Graisse de canard", "Foie", "Viande hachée", "Pour soupe", "Autre"],
        
        # --- Viande rouge ---
        "Porc": ["Filet", "Côtelette", "Jambon", "Échine", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Agneau": ["Filet", "Côtelette", "Gigot", "Collet", "Épaule", "Poitrine", "Côtes", "Souris", "Viande hachée", "Pour soupe", "Autre"],
        "Bœuf": ["Filet", "Entrecôte", "Rumsteck", "Collier", "Paleron", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Veau": ["Filet", "Côtelette", "Rognonnade", "Collet", "Épaule", "Poitrine", "Côtes", "Osso buco", "Viande hachée", "Pour soupe", "Autre"],
        "Lapin": ["Cuisses arrière", "Cuisses avant", "Râble", "Côtes", "Pour soupe", "Autre"],
        
        # --- Petit gibier ---
        "Caille": ["Entière", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Faisan": ["Entier", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Perdrix": ["Entière", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Pigeon": ["Entier", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Lièvre": ["Cuisses arrière", "Cuisses avant", "Râble", "Côtes", "Autre"],
        "Canard sauvage": ["Entier", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        "Oie sauvage": ["Entière", "Poitrine", "Cuisses", "Ailes", "Foie", "Autre"],
        
        # --- Gros gibier ---
        "Cerf": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Chevreuil": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Sanglier": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Élan": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Renne": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Bison": ["Filet", "Entrecôte", "Cuissot", "Collet", "Épaule", "Poitrine", "Côtes", "Jarret", "Viande hachée", "Pour soupe", "Autre"],
        "Chameau": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Bosse", "Côtes", "Viande hachée", "Pour soupe", "Autre"],
        "Lama": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Côtes", "Viande hachée", "Pour soupe", "Autre"],
        "Alpaga": ["Filet", "Côtelette", "Cuissot", "Collet", "Épaule", "Côtes", "Viande hachée", "Pour soupe", "Autre"],
        "Kangourou": ["Filet", "Steak", "Cuissot", "Collet", "Épaule", "Queue", "Viande hachée", "Pour soupe", "Autre"],
        "Crocodile/Alligator": ["Queue", "Filet", "Cuisses", "Autre"],
        "Lézard": ["Queue", "Dos", "Cuisses", "Autre"],
        "Serpent": ["Anneaux", "Autre"],
        
        # --- Poisson ---
        "Mer": ["Filet", "Darnes", "Poisson entier", "Filet avec peau", "Filet sans peau", "Morceaux", "Pour soupe", "Autre"],
        "Eau douce": ["Filet", "Darnes", "Poisson entier", "Filet avec peau", "Filet sans peau", "Morceaux", "Pour soupe", "Autre"],
        "Fruits de mer": ["Crevettes", "Calmar", "Moules", "Huîtres", "Coquilles Saint-Jacques", "Crabes", "Poulpe", "Seiche", "Autre"],
        
        # --- Produits laitiers ---
        "Lait": ["Entier", "Écrémé", "Pasteurisé", "Stérilisé", "Bouilli", "Condensé", "En poudre", "Autre"],
        "Transformation laitière": ["Fromage", "Fromage blanc", "Crème fraîche", "Yaourt", "Kéfir", "Beurre", "Fromage à tartiner", "Autre"],
        
        # --- Légumes ---
        "Frais": ["Entiers", "Coupés", "Lavés", "Pelés", "Râpés", "Autre"],
        "Traité thermiquement": ["Cuits", "Étuvés", "Frits", "Rôtis", "Vapeur", "Autre"],
        "Congelé": ["Entiers", "Coupés", "Mélange", "Purée", "Autre"],
        
        # --- Fruits ---
        "Fruits": ["Entiers", "Tranchés", "Pelés", "Sans pépins", "En conserve", "Séchés", "Autre"],
        
        # --- Pâte et Sucreries ---
        "Pâte": ["Pâte à levure", "Pâte brisée", "Pâte feuilletée", "Pâte à crêpes", "Pâte à pizza", "Pâte à pâtes", "Autre"],
        "Sucreries": ["Chocolat", "Bonbons", "Biscuits", "Gâteaux", "Pâtisseries", "Glace", "Gaufres", "Autre"],
        
        # --- Boissons ---
        "Eau": ["Pétillante", "Plate", "Minérale", "Aromatisée", "Autre"],
        "Vin": ["Rouge", "Blanc", "Rosé", "Mousseux", "Doux", "Sec", "Demi-sec", "Autre"],
        "Jus": ["Pomme", "Orange", "Raisin", "Tomate", "Multifruits", "Avec pulpe", "Sans pulpe", "Autre"],
        "Spiritueux": ["Vodka", "Whisky", "Cognac", "Rhum", "Gin", "Tequila", "Liqueur", "Autre"],
        "Bière": ["Blonde", "Brune", "Blanche", "Artisanale", "Sans alcool", "Autre"],
        
        # --- Chimie et hygiène ---
        "Sanitaire": ["Pour salle de bain", "Pour toilettes", "Pour lavabo", "Universel", "Antibactérien", "Autre"],
        "Hygiène personnelle": ["Savon", "Shampooing", "Gel douche", "Déodorant", "Dentifrice", "Rasoir", "Crème", "Autre"],
        "Équipement": ["Seau", "Balai", "Chiffon", "Éponge", "Brosse", "Gants", "Autre"],
        
        "Autre": ["Note : Saisir le nom du produit"]
    },
}

# ---------------- ISPRAVLJENE POMOĆNE FUNKCIJE ZA PREVOD ----------------

def get_main_categories():
    """Vraća glavne kategorije na trenutnom jeziku"""
    return main_categories_translations.get(current_language, main_categories_translations["srpski"])

def get_subcategories(main_category):
    """Vraća podkategorije na trenutnom jeziku - ISPRAVLJENA VERZIJA"""
    # Direktno uzimamo podkategorije za trenutni jezik
    subcats_dict = subcategories_translations.get(current_language, subcategories_translations["srpski"])
    
    # Proveravamo da li kategorija postoji u rečniku
    if main_category in subcats_dict:
        return subcats_dict[main_category]
    else:
        # Ako ne postoji, pokušavamo da pronađemo odgovarajuću kategoriju
        for lang_categories in subcategories_translations.values():
            if main_category in lang_categories:
                return lang_categories[main_category]
        return ["Ostalo"]

def get_product_parts(subcategory, main_category):
    """Vraća delove proizvoda na trenutnom jeziku"""
    # Fallback: Ako ne postoje delovi proizvoda za ovu podkategoriju, vrati ["Ostalo"]
    parts_dict = product_parts_translations.get(current_language, product_parts_translations["srpski"])
    
    if subcategory not in parts_dict:
        # Pokušaj da pronađeš srpski ekvivalent
        srpski_parts = product_parts_translations["srpski"]
        
        # Pronađi podkategoriju u srpskom rečniku podkategorija
        for srpski_main_cat, srpski_subcats in subcategories_translations["srpski"].items():
            if subcategory in srpski_subcats:
                # Pronađi indeks i vrati odgovarajuće delove
                index = srpski_subcats.index(subcategory)
                if index < len(srpski_subcats):
                    srpski_subcat = srpski_subcats[index]
                    if srpski_subcat in srpski_parts:
                        return srpski_parts[srpski_subcat]
        
        # Ako ništa ne pronađeš, vrati ["Ostalo"]
        return ["Napomena: Unesite naziv proizvoda"]  # ili odgovarajući prevod
    
    return parts_dict[subcategory]
        
# ---------------- BOJE - KAO U WINDOWS VERZIJI ----------------
category_colors = {
    "Belo meso": "#FFE295",
    "Crveno meso": "#F1624B",
    "Sitna divljač": "#F59AA6",
    "Krupna divljač": "#E19E94",
    "Riba": "#00BBF1",
    "Mlečni proizvodi": "#ACE1F9",
    "Povrće": "#8FC74A",
    "Zimnica i kompoti": "#CC98C4",
    "Testo i Slatkiši": "#FFECAB",
    "Pića": "#F8E06D",
    "Hemija i higijena": "#98D6D2",
    "Ostalo": "#F58634"
}

# BOJE ZA PODKATEGORIJE
subcategory_colors = {
    "Belo meso": ["#FFEDB5", "#F2D382"],
    "Crveno meso": ["#FABFA9", "#F9AA75"],
    "Sitna divljač": ["#F6C5A4", "#E8A97B"],
    "Krupna divljač": ["#FBCEC8", "#F6998C"],
    "Riba": ["#91D8F7", "#D5EFFC"],
    "Mlečni proizvodi": ["#ACE1F9", "#D5EFFC"],
    "Povrće": ["#8FC74A", "#A0D29E"],
    "Zimnica i kompoti": ["#F3B6D1", "#E894B0"],
    "Testo i Slatkiši": ["#FEE5CB", "#FFECAB"],
    "Pića": ["#FFD76E", "#EEB832"],
    "Hemija i higijena": ["#AADBD2", "#6FC7B8"],
    "Ostalo": ["#D9D9D9", "#BFBFBF"]
}

# BOJE ZA DELOVE PROIZVODA
product_parts_colors = {
    "Belo meso": ["#FFEDB5", "#F2D382"],
    "Crveno meso": ["#FABFA9", "#F9AA75"],
    "Sitna divljač": ["#F6C5A4", "#E8A97B"],
    "Krupna divljač": ["#FBCEC8", "#F6998C"],
    "Riba": ["#91D8F7", "#D5EFFC"],
    "Mlečni proizvodi": ["#ACE1F9", "#D5EFFC"],
    "Povrće": ["#8FC74A", "#A0D29E"],
    "Zimnica i kompoti": ["#F3B6D1", "#E894B0"],
    "Testo i Slatkiši": ["#FEE5CB", "#FFECAB"],
    "Pića": ["#FFD76E", "#EEB832"],
    "Hemija i higijena": ["#AADBD2", "#6FC7B8"],
    "Ostalo": ["#D9D9D9", "#BFBFBF"]
}

# ---------------- BAZA PODATAKA ----------------
def init_db():
    """Kreira tabele 'products' i 'shopping_list' ako ne postoje."""
    try:
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS products
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      product_name TEXT,
                      description TEXT,
                      piece TEXT,
                      quantity REAL,
                      unit TEXT,
                      entry_date TEXT,
                      shelf_life_months INTEGER,
                      expiry_date TEXT,
                      storage_location TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS shopping_list
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      product_name TEXT,
                      description TEXT,
                      date_added TEXT)''')
                      
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"FATALNA GREŠKA pri inicijalizaciji baze: {e}")

# ---------------- PREVODI I POMOĆNE FUNKCIJE ----------------
def t(key): 
    return master_strings[current_language].get(key, key)

def exit_program():
    root.quit()

def make_fullscreen_toplevel(title="Prozor"):
    top = tk.Toplevel(root)
    top.title(title)
    top.attributes("-fullscreen", True)
    top.transient(root)
    top.grab_set()
    return top
    
def calculate_expiry_date(entry_date, months):
    try:
        entry_dt = datetime.strptime(entry_date, "%Y-%m-%d")
        expiry_dt = entry_dt + timedelta(days=months*30)
        return expiry_dt.strftime("%Y-%m-%d")
    except:
        return ""

# ---------------- FUNKCIJE ZA SPISAK POTREBA ----------------
def add_to_shopping_list(product_name, description=""):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM shopping_list WHERE product_name = ?", (product_name,))
    existing = c.fetchone()
    
    if not existing:
        c.execute('''INSERT INTO shopping_list (product_name, description, date_added)
                    VALUES (?, ?, ?)''',
                 (product_name, description, datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()

def delete_selected_from_list(tree):
    selected = tree.selection()
    if not selected:
        return
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    for item in selected:
        values = tree.item(item)['values']
        if values:
            item_id = values[0]
            c.execute("DELETE FROM shopping_list WHERE id = ?", (item_id,))
    
    conn.commit()
    conn.close()
    
    for item in selected:
        tree.delete(item)

def print_shopping_list():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT product_name, description, date_added FROM shopping_list")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        return
    
    filename = f"spisak_potreba_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Proizvod', 'Opis', 'Datum dodavanja'])
        
        for row in rows:
            writer.writerow(row)

def send_selected_to_messenger(tree):
    selected = tree.selection()
    if not selected:
        return
    
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    message = "SPISAK POTREBA:\n\n"
    
    for i, item in enumerate(selected, 1):
        values = tree.item(item)['values']
        if values and len(values) >= 3:
            product_name = values[1]
            description = values[2] if len(values) > 2 else ""
            message += f"{i}. {product_name}"
            if description:
                message += f" - {description}"
            message += "\n"
    
    message += f"\nDatum: {datetime.now().strftime('%d.%m.%Y.')}"
    
    conn.close()
    
    # Kopiranje u clipboard
    root.clipboard_clear()
    root.clipboard_append(message)
    
    # Otvaranje Messenger-a
    try:
        # Facebook Messenger deeplink
        messenger_url = f"fb-messenger://share?link={message.replace(' ', '%20')}"
        webbrowser.open(messenger_url)
    except Exception as e:
        print(f"Greška pri otvaranju Messenger-a: {e}")
        # Alternativa ako Messenger nije dostupan
        try:
            # SMS fallback
            sms_url = f"sms:?body={message.replace(' ', '%20')}"
            webbrowser.open(sms_url)
        except Exception as e2:
            print(f"Greška pri otvaranju SMS-a: {e2}")

# ---------------- AŽURIRANJE PROIZVODA - CEO EKRAN ----------------
# ---------------- AŽURIRANJE PROIZVODA - KOMPLETNA VERZIJA SA SVIM POLJIMA ----------------
def update_selected_product(tree):
    selected = tree.selection()
    if not selected:
        return
    
    item = tree.item(selected[0])
    values = item['values']
    
    if len(values) < 7:  # Sada imamo 7 kolona
        return
    
    # PRVO: Dobij ID proizvoda iz baze koristeći sve dostupne informacije
    selected_product_name = values[0] if len(values) > 0 else ""
    selected_piece = values[2] if len(values) > 2 else ""
    selected_storage = values[6] if len(values) > 6 else ""
    
    # Preuzmi KOMPLETNE podatke iz baze
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Pokušaj prvo sa tačnim nazivom
    c.execute('''SELECT id, product_name, description, piece, quantity, unit, 
                 entry_date, shelf_life_months, expiry_date, storage_location 
                 FROM products 
                 WHERE product_name = ? OR product_name LIKE ?
                 LIMIT 1''',
             (selected_product_name, f'%{selected_product_name}%'))
    
    result = c.fetchone()
    
    # Ako nije pronađeno, pokušaj sa ostalim kriterijumima
    if not result and selected_piece:
        c.execute('''SELECT id, product_name, description, piece, quantity, unit, 
                     entry_date, shelf_life_months, expiry_date, storage_location 
                     FROM products 
                     WHERE piece = ? 
                     LIMIT 1''',
                 (selected_piece,))
        result = c.fetchone()
    
    conn.close()
    
    if not result:
        print("Nije pronađen proizvod u bazi")
        return
    
    (selected_id, product_name, description, piece, quantity, 
     unit, entry_date, shelf_life_months, expiry_date, storage_location) = result
    
    # NOVI CEO EKRAN ZA AŽURIRANJE SA SVIM POLJIMA
    win = make_fullscreen_toplevel(t("azuriranje_proizvoda"))
    
    # HEADER
    header_frame = tk.Frame(win, bg="lightgray", height=60)
    header_frame.pack(fill="x", padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Button(header_frame, text=t("nazad"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="lightblue", command=win.destroy).pack(side="left", padx=5, pady=5)
    
    # GLAVNI SADRŽAJ
    main_container = tk.Frame(win)
    main_container.pack(fill="both", expand=True, padx=5, pady=5)
    
    canvas = tk.Canvas(main_container)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=win.winfo_screenwidth() - 20)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # SAMO NASLOV - BEZ ID INFORMACIJA
    tk.Label(scrollable_frame, text=t("azuriranje_proizvoda"), 
             font=("Arial", FONT_SIZE + 2, "bold"), fg="darkblue").pack(pady=10)
    
    # FORMA ZA AŽURIRANJE - BEZ IKAKVIH DODATNIH INFO
    form_frame = tk.Frame(scrollable_frame)
    form_frame.pack(padx=5, pady=5, fill="x")
    
    form_frame.columnconfigure(0, weight=0)
    form_frame.columnconfigure(1, weight=1)
    
    row_idx = 0
    
    # 1. NAZIV PROIZVODA (MOŽE DA SE MENJA) - PRVO POLJE POSLE NASLOVA
    tk.Label(form_frame, text=t("naziv_proizvoda"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    name_var = tk.StringVar(value=product_name)
    name_entry = tk.Entry(form_frame, textvariable=name_var, font=("Arial", FONT_SIZE))
    name_entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 2. OPIS (može da se menja)
    tk.Label(form_frame, text=t("opis"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    desc_var = tk.StringVar(value=description)
    desc_entry = tk.Entry(form_frame, textvariable=desc_var, font=("Arial", FONT_SIZE))
    desc_entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 3. KOMAD/DEO (može da se menja)
    tk.Label(form_frame, text=t("komad"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    piece_var = tk.StringVar(value=piece)
    piece_entry = tk.Entry(form_frame, textvariable=piece_var, font=("Arial", FONT_SIZE))
    piece_entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 4. KOLIČINA (može da se menja)
    tk.Label(form_frame, text=t("kolicina"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    qty_var = tk.StringVar(value=str(quantity))
    qty_entry = tk.Entry(form_frame, textvariable=qty_var, font=("Arial", FONT_SIZE))
    qty_entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 5. JEDINICA MERE (padajući meni)
    tk.Label(form_frame, text=t("jedinica_mere"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    unit_options = ["kg", "g", "kom", "l", "ml", "pak", "flaša", "kutija"]
    unit_var = tk.StringVar(value=unit)
    unit_combo = ttk.Combobox(form_frame, textvariable=unit_var, values=unit_options, 
                              font=("Arial", FONT_SIZE), state="readonly")
    unit_combo.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 6. DATUM UNOSA (može da se menja)
    tk.Label(form_frame, text=t("datum_unosa"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    date_var = tk.StringVar(value=entry_date)
    date_entry = tk.Entry(form_frame, textvariable=date_var, font=("Arial", FONT_SIZE))
    date_entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 7. ROK TRAJANJA U MESECIMA (može da se menja)
    tk.Label(form_frame, text=t("rok_trajanja"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    shelf_life_var = tk.StringVar(value=str(shelf_life_months))
    shelf_life_entry = tk.Entry(form_frame, textvariable=shelf_life_var, font=("Arial", FONT_SIZE))
    shelf_life_entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 8. AUTOMATSKI ROK (samo prikaz)
    tk.Label(form_frame, text=t("automatski_rok"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    expiry_date_label = tk.Label(form_frame, text=expiry_date, font=("Arial", FONT_SIZE), bg="lightgray")
    expiry_date_label.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # 9. MESTO SKLADIŠTENJA (padajući meni)
    tk.Label(form_frame, text=t("mesto_skladistenja"), 
             font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    storage_options = [
        t("zamrzivac_1"), 
        t("zamrzivac_2"), 
        t("zamrzivac_3"), 
        t("frizider"), 
        t("ostava"), 
        t("Ostalo")
    ]
    storage_var = tk.StringVar(value=storage_location)
    storage_combo = ttk.Combobox(form_frame, textvariable=storage_var, values=storage_options, 
                                 font=("Arial", FONT_SIZE), state="readonly")
    storage_combo.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    # Funkcija za ažuriranje automatskog roka
    def update_expiry_display(*args):
        try:
            months = int(shelf_life_var.get()) if shelf_life_var.get().isdigit() else 0
        except:
            months = 0
            
        new_expiry = calculate_expiry_date(date_var.get(), months)
        expiry_date_label.config(text=new_expiry)
    
    # Poveži promene
    date_var.trace_add("write", update_expiry_display)
    shelf_life_var.trace_add("write", update_expiry_display)
    
    # FOKUS NA POLJE ZA KOLIČINU
    def focus_on_quantity():
        win.after(100, lambda: qty_entry.focus_set())
        win.after(200, lambda: qty_entry.select_range(0, tk.END))
    
    win.after(300, focus_on_quantity)
    
    # DUGMAD
    button_frame = tk.Frame(scrollable_frame)
    button_frame.pack(pady=20)
    
    def save_changes():
        """Snima sve promene u bazu"""
        # Validacija obaveznih polja
        if not name_var.get().strip():
            messagebox.showerror(t("pogresan_unos"), "Polje 'Proizvod' ne može biti prazno!")
            name_entry.focus_set()
            return
            
        try:
            new_quantity = float(qty_var.get())
            new_shelf_life = int(shelf_life_var.get()) if shelf_life_var.get().isdigit() else 0
        except ValueError:
            messagebox.showerror(t("pogresan_unos"), t("kolicina_mora_broj"))
            qty_entry.focus_set()
            return
        
        # Potvrda ažuriranja
        if not messagebox.askyesno(t("potvrda_azuriranja"), t("potvrdi_izmenu")):
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        
        # Izračunaj novi rok trajanja
        new_expiry_date = calculate_expiry_date(date_var.get(), new_shelf_life)
        
        # Ako je količina 0, dodaj u spisak potreba i obriši iz zaliha
        if new_quantity == 0:
            add_to_shopping_list(name_var.get().strip(), desc_var.get().strip())
            c.execute("DELETE FROM products WHERE id = ?", (selected_id,))
            messagebox.showinfo(t("proizvod_azuriran"), 
                              f"Proizvod '{name_var.get().strip()}' je prebačen u spisak potreba.")
        else:
            # Ažuriraj SVA polja KORISTEĆI ID
            c.execute('''UPDATE products SET 
                        product_name = ?,
                        description = ?, 
                        piece = ?, 
                        quantity = ?, 
                        unit = ?, 
                        entry_date = ?, 
                        shelf_life_months = ?, 
                        expiry_date = ?, 
                        storage_location = ?
                        WHERE id = ?''',
                     (name_var.get().strip(),
                      desc_var.get().strip(), 
                      piece_var.get().strip(),
                      new_quantity,
                      unit_var.get(),
                      date_var.get(),
                      new_shelf_life,
                      new_expiry_date,
                      storage_var.get(),
                      selected_id))
            
            messagebox.showinfo(t("proizvod_azuriran"), 
                              f"Proizvod '{name_var.get().strip()}' je uspešno ažuriran.")
        
        conn.commit()
        conn.close()
        
        # Zatvori sve prozore i vrati se na zalihe
        for widget in root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        show_inventory()
    
    def delete_product():
        """Briše proizvod iz baze"""
        if not messagebox.askyesno("Potvrda brisanja", 
                                  f"Da li ste sigurni da želite da obrišete proizvod '{product_name}'?"):
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id = ?", (selected_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Proizvod obrisan", 
                          f"Proizvod '{product_name}' je obrisan iz zaliha.")
        
        # Zatvori prozor i vrati se na zalihe
        win.destroy()
        show_inventory()
    
    # DUGMAD
    tk.Button(button_frame, text=t("snimi_izmene"), font=("Arial", FONT_SIZE, "bold"),
             bg="lightgreen", command=save_changes, width=18, height=2).pack(side="left", padx=10, pady=5)
    
    tk.Button(button_frame, text=t("obrisi"), font=("Arial", FONT_SIZE, "bold"),
             bg="red", fg="white", command=delete_product, width=12, height=2).pack(side="left", padx=10, pady=5)
    
    tk.Button(button_frame, text=t("nazad"), font=("Arial", FONT_SIZE, "bold"),
             bg="lightcoral", command=win.destroy, width=12, height=2).pack(side="left", padx=10, pady=5)
# ---------------- EKRAN ZA UNOS PODATAKA ----------------
def show_data_entry(product_name="", subcategory_name=""):
    win = make_fullscreen_toplevel(t("unos_podataka"))
    
    create_mobile_header(win, win.destroy, show_inventory, show_shopping_list)

    main_container = tk.Frame(win)
    main_container.pack(fill="both", expand=True, padx=5, pady=5)
    
    canvas = tk.Canvas(main_container)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=win.winfo_screenwidth() - 20)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    form_frame = tk.Frame(scrollable_frame)
    form_frame.pack(padx=5, pady=5, fill="x")
    
    form_frame.columnconfigure(0, weight=0)
    form_frame.columnconfigure(1, weight=1)
    
    row_idx = 0
    
    # Čuvamo reference na polja za unos
    entry_fields = []
    
    def create_form_row(parent_frame, label_text_key, default_value="", is_menu=False, options=None):
        nonlocal row_idx
        
        # KORISTIMO t() FUNKCIJU ZA PREVOD LABELA
        label_text = t(label_text_key) if label_text_key in master_strings[current_language] else label_text_key
        tk.Label(parent_frame, text=label_text, font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
        
        if is_menu:
            var = tk.StringVar(value=default_value)
            combo = ttk.Combobox(parent_frame, textvariable=var, values=options, 
                                font=("Arial", FONT_SIZE), state="readonly")
            combo.set(default_value)
            combo.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
            row_idx += 1
            return var, combo
        else:
            entry = tk.Entry(parent_frame, font=("Arial", FONT_SIZE))
            entry.insert(0, default_value)
            entry.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
            entry_fields.append(entry)  # Dodajemo u listu
            row_idx += 1
            return entry
    
    # KORISTIMO KLJUČEVE IZ MASTER_STRINGS UMESTO FIKSNIH TEKSTOVA
    name_entry = create_form_row(form_frame, "naziv_proizvoda", product_name)
    desc_entry = create_form_row(form_frame, "opis", subcategory_name)
    piece_entry = create_form_row(form_frame, "komad")
    qty_entry = create_form_row(form_frame, "kolicina")
    
    unit_options = ["kg", "g", "kom", "l"]
    unit_var, unit_combo = create_form_row(form_frame, "jedinica_mere", "kg", is_menu=True, options=unit_options)
    
    date_entry = create_form_row(form_frame, "datum_unosa", datetime.now().strftime("%Y-%m-%d"))
    shelf_life_entry = create_form_row(form_frame, "rok_trajanja", "12")
    
    # TAKOĐE PREVODIMO OPCIJE ZA SKLADIŠTE
    storage_options_translated = [
		t("zamrzivac_1"), 
		t("zamrzivac_2"), 
		t("zamrzivac_3"), 
		t("frizider"), 
		t("ostava"), 
		t("Ostalo")
	]
    storage_var, storage_combo = create_form_row(form_frame, "mesto_skladistenja", t("Ostalo"), is_menu=True, options=storage_options_translated)
    
    # AUTOMATSKI ROK - TAKOĐE PREVEDEN
    auto_rok_label = t("automatski_rok")
    tk.Label(form_frame, text=auto_rok_label, font=("Arial", FORM_LABEL_FONT_SIZE), anchor="w", width=15).grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)
    expiry_date_label = tk.Label(form_frame, text="", font=("Arial", FONT_SIZE), bg="lightgray")
    expiry_date_label.grid(row=row_idx, column=1, sticky="ew", pady=5, padx=5)
    row_idx += 1
    
    def update_expiry_date(*args):
        try:
            months = int(shelf_life_entry.get()) if shelf_life_entry.get().isdigit() else 0
        except:
            months = 0
            
        expiry_date = calculate_expiry_date(date_entry.get(), months)
        expiry_date_label.config(text=expiry_date)
    
    date_entry.bind("<KeyRelease>", update_expiry_date)
    shelf_life_entry.bind("<KeyRelease>", update_expiry_date)
    update_expiry_date()
    
    # VAŽNO: Fokusiraj se na prvo polje kada se prozor pojavi
    def focus_first_entry():
        win.after(100, lambda: name_entry.focus_set())
        win.after(200, lambda: name_entry.select_range(0, tk.END))
    
    # Pokreni fokusiranje nakon što se prozor pojavi
    win.after(300, focus_first_entry)
    
    # Takođe, dodajte handler za kada se prozor aktivira
    def on_window_activate(event):
        if event.widget == win:
            name_entry.focus_set()
    
    win.bind("<FocusIn>", on_window_activate)
    
    button_frame = tk.Frame(scrollable_frame)
    button_frame.pack(pady=10)
    
    history_frame = tk.Frame(scrollable_frame)
    history_frame.pack(pady=10, fill="x", padx=5)
    
    def save_product():
        if not name_entry.get().strip() or not piece_entry.get().strip() or not qty_entry.get().strip():
            print(f"{t('popunite_polja')}")  # Trebalo bi dodati ovaj prevod u master_strings
            return
            
        try:
            quantity = float(qty_entry.get())
        except ValueError:
            print(f"{t('kolicina_mora_broj')}")  # Trebalo bi dodati ovaj prevod
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        
        try:
            months = int(shelf_life_entry.get()) if shelf_life_entry.get().isdigit() else 0
        except:
            months = 0
            
        expiry_date = calculate_expiry_date(date_entry.get(), months)
        
        c.execute('''INSERT INTO products 
                    (product_name, description, piece, quantity, unit, entry_date, shelf_life_months, expiry_date, storage_location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (name_entry.get().strip(), desc_entry.get().strip(), piece_entry.get().strip(), 
                  quantity, unit_var.get(), date_entry.get(), 
                  months, expiry_date, storage_var.get()))
        conn.commit()
        conn.close()
        
        piece_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        shelf_life_entry.delete(0, tk.END)
        shelf_life_entry.insert(0, "12")
        update_expiry_date()
        
        show_product_history()
    
    # DUGME TAKOĐE PREVEDENO
    tk.Button(button_frame, text=t("unesi"), font=("Arial", FONT_SIZE, "bold"), 
              bg="lightgreen", fg="black", command=save_product,
              width=15, height=2).pack(pady=5, padx=10)
    
    def show_product_history():
        for widget in history_frame.winfo_children():
            widget.destroy()
        
        current_product = name_entry.get().strip()
        if not current_product:
            return
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute('''SELECT piece, quantity, unit, expiry_date, storage_location 
                     FROM products WHERE product_name = ? 
                     ORDER BY entry_date DESC LIMIT 5''', (current_product,))
        
        rows = c.fetchall()
        conn.close()
        
        if rows:
            # PREVEDEN NASLOV ZA PREGLED
            history_title = f"{t('pregled_unosa')}: {current_product}"
            tk.Label(history_frame, text=history_title, 
                    font=("Arial", FONT_SIZE, "bold")).pack(anchor="w", pady=5)
            
            table_frame = tk.Frame(history_frame)
            table_frame.pack(fill="x", pady=5)
            
            # PREVEDENI ZAGLAVLJA TABELE
            headers = [t("komad"), t("kolicina"), t("jedinica_mere"), t("rok_trajanja"), t("mesto_skladistenja")]
            # Skratimo za prikaz
            headers = [h.replace(":", "")[:4] for h in headers]
            
            for i in range(len(headers)):
                table_frame.columnconfigure(i, weight=1)
                
            for i, header in enumerate(headers):
                tk.Label(table_frame, text=header, font=("Arial", FONT_SIZE-2, "bold"),
                        bg="lightgray", relief="solid", borderwidth=1).grid(row=0, column=i, sticky="ew", padx=1, pady=1)
            
            for row_idx, row in enumerate(rows, 1):
                display_row = [row[0], f"{row[1]:.2f}", row[2], 
                              row[3].split('-')[1] + '.' + row[3].split('-')[0][-2:] if row[3] else "",
                              row[4].split(' ')[0] if row[4] else ""]
                
                for col_idx, value in enumerate(display_row):
                    bg_color = "white" if row_idx % 2 == 0 else "#f0f0f0"
                    tk.Label(table_frame, text=str(value), font=("Arial", FONT_SIZE-2),
                            bg=bg_color, relief="solid", borderwidth=1).grid(row=row_idx, column=col_idx, sticky="ew", padx=1, pady=1)
    
    def on_name_change(*args):
        show_product_history()
    
    name_entry.bind("<KeyRelease>", on_name_change)
    show_product_history()

# ---------------- STANJE ZALIHA ----------------
def show_inventory():
    win = make_fullscreen_toplevel(t("stanje_zaliha"))
    
    create_mobile_header(win, win.destroy, show_inventory, show_shopping_list)
    
    search_update_frame = tk.Frame(win, bg="#f0f0f0")
    search_update_frame.pack(fill="x", padx=5, pady=5)
    
    search_update_frame.columnconfigure(0, weight=0)
    search_update_frame.columnconfigure(1, weight=1)
    search_update_frame.columnconfigure(2, weight=0)

    tk.Label(search_update_frame, text=t("pretrazi"), font=("Arial", FONT_SIZE-2)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    search_entry = tk.Entry(search_update_frame, font=("Arial", FONT_SIZE-2), width=15)
    search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    tk.Button(search_update_frame, text=t("azuriraj"), font=("Arial", BUTTON_FONT_SIZE-2, "bold"), 
              bg="lightgreen", command=lambda: update_selected_product(tree)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    
    main_frame = tk.Frame(win)
    main_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # KOLONE - BEZ ID
    columns = ("naziv", "opis", "komada", "kolicina", "jedinica", "rok_trajanja", "mesto_skladistenja")
    
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
    
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", FONT_SIZE-2), rowheight=65)
    style.configure("Treeview.Heading", font=("Arial", FONT_SIZE-2, "bold"))
    
    # ŠIRINE KOLONA - OPTIMIZOVANE, BEZ ID
    tree.column("naziv", width=120, minwidth=100, anchor="w")  # PROIZVOD
    tree.column("opis", width=150, minwidth=120, anchor="w")   # OPIS
    tree.column("komada", width=50, minwidth=40, anchor="center")  # KOM.
    tree.column("kolicina", width=50, minwidth=40, anchor="center")  # KOL.
    tree.column("jedinica", width=45, minwidth=35, anchor="center")  # JED.
    tree.column("rok_trajanja", width=60, minwidth=50, anchor="center")  # ROK
    tree.column("mesto_skladistenja", width=70, minwidth=50, anchor="center")  # SKLADIŠTE
    
    # Postavljanje naslova kolona IZ PREVODA
    for col in columns:
        # Uzmi prevedeni naslov iz master_strings za trenutni jezik
        heading_text = master_strings[current_language]["zaglavlja_zaliha"].get(col, col)
        tree.heading(col, text=heading_text, anchor="center")
    
    tree.tag_configure('critical', background='#F9AA65')
    
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def update_display(search_term=""):
        for item in tree.get_children():
            tree.delete(item)
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        
        if search_term:
            c.execute('''SELECT id, product_name, description, piece, quantity, unit, expiry_date, storage_location 
                         FROM products 
                         WHERE product_name LIKE ? OR piece LIKE ? OR storage_location LIKE ?
                         ORDER BY storage_location, expiry_date''', 
                     (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            c.execute('''SELECT id, product_name, description, piece, quantity, unit, expiry_date, storage_location 
                         FROM products ORDER BY storage_location, expiry_date''')
        
        for row in c.fetchall():
            item_id, product_name, description, piece, quantity, unit, expiry_date, storage_location = row
            
            # PRIKAZ SKRAĆENIH VREDNOSTI ZA SKLADIŠTE
            storage_display = ""
            if storage_location:
                try:
                    sl = storage_location.lower()
                except:
                    sl = storage_location
                if any(k in sl for k in ["zamrzivač", "zamrzivac", "freezer", "congelateur", "zamrzivac"]):
                    parts = storage_location.split()
                    if len(parts) > 1 and parts[1].isdigit():
                        # Prevedi "Freezer" ili "Congélateur" u lokalni jezik
                        if current_language == "english":
                            storage_display = "F" + parts[1]
                        elif current_language == "francais":
                            storage_display = "C" + parts[1]
                        else:
                            storage_display = "Z" + parts[1]
                    else:
                        storage_display = storage_location[:3]
                else:
                    storage_display = storage_location[:3]
            else:
                storage_display = ""
            
            # Formatiranje prikaza roka (YYYY-MM-DD → MM.YY)
            expiry_display = ""
            try:
                parts = expiry_date.split('-')
                expiry_display = parts[1] + '.' + parts[0][-2:]  # MM.YY
            except Exception:
                expiry_display = expiry_date or ""
            
            # VREDNOSTI ZA PRIKAZ - KRATKE VREDNOSTI
            display_values = [
                product_name[:20] + "..." if len(product_name) > 20 else product_name,  # PROIZVOD
                description[:25] + "..." if len(description) > 25 else description,  # OPIS
                piece[:12] if piece else "",  # KOM.
                f"{float(quantity):.1f}" if isinstance(quantity, (int, float)) else str(quantity),  # KOL.
                unit[:3] if unit else "",  # JED.
                expiry_display,  # ROK
                storage_display  # SKLADIŠTE
            ]
            
            # LOGIKA ZA KRITIČNE ZALIHE
            is_critical = False
            try:
                unit_lower = str(unit).lower()
                qty_float = float(quantity)
                
                if unit_lower in ['kom', 'pcs', 'stk', 'piece', 'pièce'] and qty_float <= 2:
                    is_critical = True
                elif unit_lower in ['kg'] and qty_float <= 0.5:
                    is_critical = True
                elif unit_lower in ['g'] and qty_float <= 500:
                    is_critical = True
                elif unit_lower in ['l'] and qty_float <= 0.5:
                    is_critical = True
            except Exception:
                is_critical = False
            
            if is_critical:
                tree.insert("", "end", values=display_values, tags=('critical',))
            else:
                tree.insert("", "end", values=display_values)
        
        conn.close()
    
    def on_search(*args):
        update_display(search_entry.get())
    
    search_entry.bind("<KeyRelease>", on_search)
    update_display()

# ---------------- SLANJE EMAIL DIALOG - KOMPLETNA FUNKCIJA ----------------
def show_send_email_dialog():
    """Prikazuje dijalog za slanje spiska preko email-a, Messenger-a ili kopiranje"""
    win = make_fullscreen_toplevel(t("posalji_spisak"))
    
    # HEADER
    header_frame = tk.Frame(win, bg="lightgray", height=60)
    header_frame.pack(fill="x", padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Button(header_frame, text=t("nazad"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="lightblue", command=win.destroy).pack(side="left", padx=5, pady=5)
    
    # GLAVNI SADRŽAJ
    main_container = tk.Frame(win)
    main_container.pack(fill="both", expand=True, padx=5, pady=5)
    
    canvas = tk.Canvas(main_container)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=win.winfo_screenwidth() - 20)
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # NASLOV
    tk.Label(scrollable_frame, text=t("posalji_spisak"), 
             font=("Arial", FONT_SIZE, "bold"), fg="darkblue").pack(pady=10)
    
    # FORMA ZA EMAIL
    form_frame = tk.Frame(scrollable_frame)
    form_frame.pack(padx=10, pady=10, fill="x")
    
    form_frame.columnconfigure(0, weight=0)
    form_frame.columnconfigure(1, weight=1)
    
    # Učitaj postojeća podešavanja
    email_settings = load_email_settings()
    
    # POŠILJALAC
    tk.Label(form_frame, text="Vaš Email:", font=("Arial", FORM_LABEL_FONT_SIZE), 
             anchor="w").grid(row=0, column=0, sticky="w", pady=5, padx=5)
    sender_var = tk.StringVar(value=email_settings.get('sender_email', ''))
    sender_entry = tk.Entry(form_frame, textvariable=sender_var, font=("Arial", FONT_SIZE))
    sender_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
    
    # APP PASSWORD
    tk.Label(form_frame, text="App Password:", font=("Arial", FORM_LABEL_FONT_SIZE), 
             anchor="w").grid(row=1, column=0, sticky="w", pady=5, padx=5)
    password_var = tk.StringVar(value=email_settings.get('app_password', ''))
    password_entry = tk.Entry(form_frame, textvariable=password_var, show="*", font=("Arial", FONT_SIZE))
    password_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
    
    # HELP ZA APP PASSWORD
    tk.Button(form_frame, text="?", font=("Arial", FONT_SIZE-2), 
              bg="lightyellow", command=show_app_password_help,
              width=2, height=1).grid(row=1, column=2, padx=5, pady=5)
    
    # PRIMALAC
    tk.Label(form_frame, text="Email primaoca:", font=("Arial", FORM_LABEL_FONT_SIZE), 
             anchor="w").grid(row=2, column=0, sticky="w", pady=5, padx=5)
    receiver_var = tk.StringVar(value=email_settings.get('receiver_email', ''))
    receiver_entry = tk.Entry(form_frame, textvariable=receiver_var, font=("Arial", FONT_SIZE))
    receiver_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
    
    # STATUS LABELA
    status_label = tk.Label(scrollable_frame, text="", font=("Arial", FONT_SIZE-1), fg="blue")
    status_label.pack(pady=5)
    
    # DUGMAD
    button_frame = tk.Frame(scrollable_frame)
    button_frame.pack(pady=15)
    
    def send_email():
        """Šalje spisak preko email-a"""
        sender_email = sender_var.get().strip()
        app_password = password_var.get().strip()
        receiver_email = receiver_var.get().strip()
        
        if not sender_email or not app_password or not receiver_email:
            status_label.config(text="❌ Popunite sva polja!", fg="red")
            return
        
        # Sačuvaj podešavanja
        save_email_settings(sender_email, app_password, receiver_email)
        
        # Preuzmi spisak iz baze
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT product_name, description FROM shopping_list")
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            status_label.config(text="❌ Spisak je prazan!", fg="red")
            return
        
        # Kreiraj poruku
        message_body = "SPISAK POTREBA:\n\n"
        for i, row in enumerate(rows, 1):
            product_name = row[0]
            description = row[1] if row[1] else ""
            message_body += f"{i}. {product_name}"
            if description:
                message_body += f" - {description}"
            message_body += "\n"
        
        message_body += f"\nDatum: {datetime.now().strftime('%d.%m.%Y.')}"
        message_body += f"\nVreme: {datetime.now().strftime('%H:%M')}"
        
        try:
            # Podešavanje email poruke
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"Spisak potreba - {datetime.now().strftime('%d.%m.%Y.')}"
            
            msg.attach(MIMEText(message_body, 'plain'))
            
            # Slanje email-a preko Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            status_label.config(text="✅ Email uspešno poslat!", fg="green")
            
        except Exception as e:
            status_label.config(text=f"❌ Greška pri slanju: {str(e)}", fg="red")
    
    def send_to_messenger():
        """Šalje spisak preko Messenger-a"""
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT product_name, description FROM shopping_list")
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            status_label.config(text="Spisak je prazan!", fg="red")
            return
        
        message = "📋 SPISAK POTREBA 📋\n\n"
        for i, row in enumerate(rows, 1):
            product_name = row[0]
            description = row[1] if row[1] else ""
            message += f"#{i} {product_name}"
            if description:
                message += f" - {description}"
            message += "\n"
        
        message += f"\n📅 Datum: {datetime.now().strftime('%d.%m.%Y.')}"
        message += f"\n🕒 Vreme: {datetime.now().strftime('%H:%M')}"
        
        # Kopiraj u clipboard
        win.clipboard_clear()
        win.clipboard_append(message)
        
        status_label.config(text=f"✅ {t('kopiraj')}!\nSada otvorite Messenger\n i nalepite poruku", fg="green")
        
        # Pokušaj da otvoriš Messenger
        try:
            # Facebook Messenger deeplink
            messenger_url = "fb-messenger://share"
            webbrowser.open(messenger_url)
        except Exception as e:
            print(f"Greška pri otvaranju Messenger-a: {e}")
            # Pokaži uputstvo
            status_label.config(text="✅ Spisak kopiran!\nOtvorite Messenger ručno\n i nalepite poruku", fg="green")
    
    def copy_to_clipboard():
        """Kopira spisak u clipboard"""
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT product_name, description FROM shopping_list")
        rows = c.fetchall()
        conn.close()
        
        message = "SPISAK POTREBA:\n\n"
        for i, row in enumerate(rows, 1):
            product_name = row[0]
            description = row[1] if row[1] else ""
            message += f"{i}. {product_name}"
            if description:
                message += f" - {description}"
            message += "\n"
        
        message += f"\nDatum: {datetime.now().strftime('%d.%m.%Y.')}"
        
        # Kopiraj u clipboard
        win.clipboard_clear()
        win.clipboard_append(message)
        
        status_label.config(text="✅ Spisak kopiran!\nSada nalepite gde god želite", fg="green")
    
    # SMANJEN FONT I VISINA DUGMADI
    tk.Button(button_frame, text=t("posalji_email"), font=("Arial", FONT_SIZE-2),
             bg="lightgreen", command=send_email, width=8, height=1).pack(side="left", padx=3)
    
    tk.Button(button_frame, text=t("posalji_messenger"), font=("Arial", FONT_SIZE-2),
             bg="#0084FF", fg="white", command=send_to_messenger, width=10, height=1).pack(side="left", padx=3)
    
    tk.Button(button_frame, text=t("kopiraj"), font=("Arial", FONT_SIZE-2),
             bg="lightblue", command=copy_to_clipboard, width=8, height=1).pack(side="left", padx=3)
    
    tk.Button(button_frame, text="ZATVORI", font=("Arial", FONT_SIZE-2),
             bg="lightcoral", command=win.destroy, width=8, height=1).pack(side="left", padx=3)

def show_app_password_help():
    """Prikaže pomoć za App Password u novom prozoru"""
    # NOVI CEO EKRAN ZA POMOĆ
    help_win = make_fullscreen_toplevel(t("pomoc_app_password"))
    
    # HEADER
    header_frame = tk.Frame(help_win, bg="lightgray", height=60)
    header_frame.pack(fill="x", padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    tk.Button(header_frame, text=t("nazad"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="lightblue", command=help_win.destroy).pack(side="left", padx=5, pady=5)
    
    # GLAVNI SADRŽAJ
    main_help_frame = tk.Frame(help_win)
    main_help_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # NASLOV
    tk.Label(main_help_frame, text=t("pomoc_app_password"), 
             font=("Arial", FONT_SIZE, "bold"), fg="darkblue").pack(pady=10)
    
    # TEKST POMOĆI
    help_text = """Kako dobiti App Password:

1. Idite na Google Account
2. Ukljucite 2-step verification  
3. U "Security" pronadjite "App passwords"
4. Generisite password za "Mail"
5. Kopirajte 16-cifreni kod
6. Nalepite ovde (bez razmaka)

Lozinka je bezbednija alternativa
vasoj glavnoj lozinki!"""
    
    help_label = tk.Label(main_help_frame, text=help_text, font=("Arial", FONT_SIZE-1), 
                         justify="left", bg="#E8F4FD", wraplength=600)
    help_label.pack(pady=15, padx=10, fill="both", expand=True)
    
    # DUGME ZA ZATVARANJE
    tk.Button(main_help_frame, text="ZATVORI", font=("Arial", FONT_SIZE-1),
             bg="lightcoral", command=help_win.destroy, width=12, height=1).pack(pady=10)

# ---------------- ZAJEDNIČKI HEADER ----------------
def create_mobile_header(win, back_cmd, inventory_cmd, shopping_cmd):
    """Kreira kompaktni header 2x2 dugmad za mobilni ekran."""
    header_frame = tk.Frame(win, bg="lightgray", height=95)
    header_frame.pack(fill="x", padx=5, pady=5)
    header_frame.pack_propagate(False)
    
    header_frame.columnconfigure(0, weight=1)
    header_frame.columnconfigure(1, weight=1)
    
    button_height = 1
    
    # RED 0: NAZAD i IZLAZ
    tk.Button(header_frame, text=t("nazad"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="lightblue", command=back_cmd, height=button_height).grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    
    tk.Button(header_frame, text=t("izlaz"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="red", fg="white", command=exit_program, height=button_height).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    # RED 1: ZALIHE i SPISAK
    tk.Button(header_frame, text=t("stanje"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="lightgreen", command=inventory_cmd, height=button_height).grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    
    tk.Button(header_frame, text=t("spisak"), font=("Arial", BUTTON_FONT_SIZE, "bold"), 
              bg="lightcoral", command=shopping_cmd, height=button_height).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

# ---------------- SPISAK POTREBA - CEO EKRAN ----------------
def show_shopping_list():
    win = make_fullscreen_toplevel(t("spisak_potreba"))
    
    create_mobile_header(win, win.destroy, show_inventory, show_shopping_list)

    # DUGMAD ISPOD HEADERA
    button_frame = tk.Frame(win)
    button_frame.pack(fill="x", padx=5, pady=5)
    
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

    def select_all_items():
        """Označi sve stavke u listi"""
        items = tree.get_children()
        for item in items:
            tree.selection_add(item)
    def copy_selected_to_clipboard():
        """Kopira označene stavke u clipboard"""
        selected = tree.selection()
        if not selected:
            return
    
        # KORISTIMO PREVEDENE TEKSTOVE
        message = f"📋 {t('spisak_potreba')} 📋\n\n"
    
        for i, item in enumerate(selected, 1):
            values = tree.item(item)['values']
            if values and len(values) >= 3:
                product_name = values[1]
                description = values[2] if len(values) > 2 else ""
                message += f"#{i} {product_name}"
                if description:
                    message += f" - {description}"
                message += "\n"  # OVO JE U VUČENO
    
        message += f"\n📅 {t('datum_unosa').replace(':', '')}: {datetime.now().strftime('%d.%m.%Y.')}"
        message += f"\n🕒 Vreme: {datetime.now().strftime('%H:%M')}"
    
        # Ostatak funkcije (kopiranje u clipboard i prikaz poruke)
        win.clipboard_clear()
        win.clipboard_append(message)
    
        status_text = f"✅ {t('kopiraj')}!"
        status_label = tk.Label(win, text=status_text, 
                               font=("Arial", FONT_SIZE-1), fg="green", bg="lightyellow")
        status_label.place(relx=0.5, rely=0.9, anchor="center")
        win.after(2000, status_label.destroy)
    
    tk.Button(button_frame, text=t("oznaci_sve"), font=("Arial", BUTTON_FONT_SIZE-2, "bold"), 
              bg="lightblue", command=select_all_items).grid(row=0, column=0, padx=2, pady=5, sticky="ew")
    
    tk.Button(button_frame, text=t("obrisi"), font=("Arial", BUTTON_FONT_SIZE-2, "bold"), 
              bg="lightcoral", command=lambda: delete_selected_from_list(tree)).grid(row=0, column=1, padx=2, pady=5, sticky="ew")
    
    tk.Button(button_frame, text=t("kopiraj"), font=("Arial", BUTTON_FONT_SIZE-2, "bold"), 
              bg="lightgreen", command=copy_selected_to_clipboard).grid(row=0, column=2, padx=2, pady=5, sticky="ew")

    main_frame = tk.Frame(win)
    main_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    columns = ("ID", "Proizvod", "Opis", "Datum")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
    
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", FONT_SIZE-2), rowheight=65)
    style.configure("Treeview.Heading", font=("Arial", FONT_SIZE-2, "bold"))
    
    tree.heading("ID", text="ID", anchor="center")
    tree.heading("Proizvod", text=t("naziv_proizvoda").replace(":", ""), anchor="center")
    tree.heading("Opis", text=t("opis").replace(":", ""), anchor="center")
    tree.heading("Datum", text=t("datum_unosa").replace(":", ""), anchor="center")
    
    tree.column("ID", width=40, anchor="center")
    tree.column("Proizvod", width=120, anchor="w")
    tree.column("Opis", width=150, anchor="w")
    tree.column("Datum", width=80, anchor="center")
    
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def refresh_list():
        for item in tree.get_children():
            tree.delete(item)
        
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT id, product_name, description, date_added FROM shopping_list")
        rows = c.fetchall()
        conn.close()
        
        for row in rows:
            date_str = row[3].split('-')
            short_date = f"{date_str[2]}.{date_str[1]}" if len(date_str) == 3 else row[3]
            tree.insert("", "end", values=(row[0], row[1], row[2], short_date))
    
    refresh_list()

# ---------------- DELOVI PROIZVODA - DVA DUGMETA U REDU ----------------
def show_product_parts(subcategory, main_category):
    parts = get_product_parts(subcategory, main_category)
    
        # PROVERA: Ako je parts samo ["Ostalo"] ili sadrži "Napomena:", idi direktno na unos
    if len(parts) == 1 and ("Ostalo" in parts[0] or "Napomena:" in parts[0] or is_other_category(parts[0])):
        # Odmah idi na unos podataka sa praznim poljima
        show_data_entry("", subcategory)  # Prazan naziv proizvoda
        return
    
    # Ako je parts prazna lista, idi direktno na unos
    if not parts:
        show_data_entry(subcategory, subcategory)
        return
    
    # ... ostatak postojeće funkcije ostaje isti ...
    
    # KORISTIMO PREVEDENI NASLOV
    win = make_fullscreen_toplevel(f"{main_category} - {subcategory}")
    
    create_mobile_header(win, win.destroy, show_inventory, show_shopping_list)

    main_frame = tk.Frame(win)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # PREVEDEN NASLOV
    tk.Label(main_frame, text=f"{t('delovi_proizvoda')} {subcategory}:", 
             font=("Arial", FONT_SIZE-2, "bold")).pack(pady=5)
    
    parts_frame = tk.Frame(main_frame)
    parts_frame.pack(expand=True, fill="both")
    
    # Pronađi srpski naziv glavne kategorije za boje
    srpski_categories = main_categories_translations["srpski"]
    current_categories = get_main_categories()
    
    srpski_main_category = main_category
    if main_category in current_categories:
        index = current_categories.index(main_category)
        srpski_main_category = srpski_categories[index]
    
    colors = product_parts_colors.get(srpski_main_category, ["#FFEDB5", "#F2D382"])
    
    # DVA DUGMETA U JEDNOM REDU - SMANJEN FONT
    for i, part in enumerate(parts):
        row = i // 2  # 2 dugmeta po redu
        col = i % 2
        color = colors[i % len(colors)]
        
        # ISPRAVKA OVDE: Koristi lambda sa default argumentima da se pravilno prosledi vrednost
        cmd = lambda p=part, s=subcategory: show_data_entry(p, s)
        
        btn = tk.Button(parts_frame, text=part, font=("Arial", FONT_SIZE-2),
                       bg=color, fg="black", command=cmd,
                       width=18, height=3, wraplength=400)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    # RAVNOMERNA RASPOREDA
    for i in range(2):
        parts_frame.columnconfigure(i, weight=1)
    for i in range((len(parts) + 1) // 2):
        parts_frame.rowconfigure(i, weight=1)
	
# ---------------- PODKATEGORIJE - DVA DUGMETA U REDU ----------------
def get_main_categories():
    """Vraća glavne kategorije na trenutnom jeziku"""
    return main_categories_translations.get(current_language, main_categories_translations["srpski"])

def get_subcategories(main_category):
    """Vraća podkategorije na trenutnom jeziku - ISPRAVLJENA VERZIJA"""
    # Uzmi rečnik podkategorija za trenutni jezik
    subcats_dict = subcategories_translations.get(current_language, subcategories_translations["srpski"])
    
    # Direktno vrati podkategorije za datu glavnu kategoriju
    if main_category in subcats_dict:
        return subcats_dict[main_category]
    else:
        # Ako ne postoji, vrati podkategorije iz srpskog kao fallback
        return subcategories_translations["srpski"].get(main_category, ["Ostalo"])

def get_product_parts(subcategory, main_category):
    """Vraća delove proizvoda na trenutnom jeziku - ISPRAVLJENA VERZIJA"""
    # Uzmi rečnik delova proizvoda za trenutni jezik
    parts_dict = product_parts_translations.get(current_language, product_parts_translations["srpski"])
    
    # Direktno vrati delove proizvoda za datu podkategoriju
    if subcategory in parts_dict:
        return parts_dict[subcategory]
    else:
        # Ako ne postoji, vrati delove iz srpskog kao fallback
        return product_parts_translations["srpski"].get(subcategory, ["Ostalo"])
def is_other_category(category_name):
    """Proverava da li je kategorija 'Ostalo' na bilo kom jeziku"""
    other_names = {
        "srpski": "Ostalo",
        "hungary": "Egyéb", 
        "ukrajinski": "Інше",
        "ruski": "Другое",
        "english": "Other",
        "deutsch": "Andere",
        "mandarinski": "其他",
        "espanol": "Otro",
		"portugalski": "Outro",  # DODATO
        "francais": "Autre"
    }
    
    # Proveri da li se category_name poklapa sa bilo kojim od ovih naziva
    for name in other_names.values():
        if category_name == name:
            return True
    return False
		
def show_subcategories(main_category):
    # Ako je kategorija "Ostalo" na bilo kom jeziku, idi direktno na unos
    if main_category == t("Ostalo") or main_category == "Ostalo":
        show_data_entry(main_category, main_category)
        return
    
    win = make_fullscreen_toplevel(f"{t('podkategorije')} {main_category}")
    
    create_mobile_header(win, win.destroy, show_inventory, show_shopping_list)
    
    main_frame = tk.Frame(win)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    tk.Label(main_frame, text=f"{t('podkategorije')} {main_category}:", 
             font=("Arial", FONT_SIZE-2, "bold")).pack(pady=10)
    
    subcats = get_subcategories(main_category)
    
    # FALLBACK: ako nema podkategorija, idi direktno na unos podataka
    if not subcats or subcats == ["Ostalo"]:
        win.destroy()
        show_data_entry(main_category, main_category)
        return
        
    subcats_frame = tk.Frame(main_frame)
    subcats_frame.pack(expand=True, fill="both")
    
    # Pronađi srpski naziv glavne kategorije za boje
    srpski_categories = main_categories_translations["srpski"]
    current_categories = get_main_categories()
    
    srpski_main_category = main_category
    if main_category in current_categories:
        index = current_categories.index(main_category)
        srpski_main_category = srpski_categories[index]
    
    colors = subcategory_colors.get(srpski_main_category, ["#FFEDB5", "#F2D382"])
    
    # DVA DUGMETA U JEDNOM REDU - SMANJEN FONT
    for i, subcat in enumerate(subcats):
        row = i // 2  # 2 dugmeta po redu
        col = i % 2
        color = colors[i % len(colors)]
        
        cmd = lambda sc=subcat, mc=main_category: show_product_parts(sc, mc)
        
        btn = tk.Button(subcats_frame, text=subcat, font=("Arial", FONT_SIZE-2),
                       bg=color, fg="black", command=cmd,
                       width=18, height=3, wraplength=300)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    # RAVNOMERNA RASPOREDA
    for i in range(2):
        subcats_frame.columnconfigure(i, weight=1)
    for i in range((len(subcats) + 1) // 2):
        subcats_frame.rowconfigure(i, weight=1)
        
# ---------------- GLAVNE KATEGORIJE - DVA DUGMETA U REDU ----------------
def open_category(category):
    # Proveri da li je ovo "Ostalo" kategorija na bilo kom jeziku
    if is_other_category(category):
        show_data_entry(category, category)  # Kategorija kao naziv i opis
        return
    
    # Uzmi podkategorije na trenutnom jeziku
    subcats = get_subcategories(category)
    
    # Proveri da li su podkategorije samo ["Ostalo"]
    if not subcats or (len(subcats) == 1 and is_other_category(subcats[0])):
        show_data_entry(category, category)
    else:
        show_subcategories(category)

def show_subcategories(main_category):
    # Proveri da li je ovo "Ostalo" kategorija na bilo kom jeziku
    if is_other_category(main_category):
        show_data_entry(main_category, main_category)
        return
    
    win = make_fullscreen_toplevel(f"{t('podkategorije')} {main_category}")
    
    create_mobile_header(win, win.destroy, show_inventory, show_shopping_list)
    
    main_frame = tk.Frame(win)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    tk.Label(main_frame, text=f"{t('podkategorije')} {main_category}:", 
             font=("Arial", FONT_SIZE-2, "bold")).pack(pady=10)
    
    subcats = get_subcategories(main_category)
    
    subcats_frame = tk.Frame(main_frame)
    subcats_frame.pack(expand=True, fill="both")
    
    # Pronađi srpski naziv glavne kategorije za boje
    srpski_categories = main_categories_translations["srpski"]
    current_categories = get_main_categories()
    
    srpski_main_category = main_category
    if main_category in current_categories:
        index = current_categories.index(main_category)
        srpski_main_category = srpski_categories[index]
    
    colors = subcategory_colors.get(srpski_main_category, ["#FFEDB5", "#F2D382"])
    
    # DVA DUGMETA U JEDNOM REDU
    for i, subcat in enumerate(subcats):
        row = i // 2  # 2 dugmeta po redu
        col = i % 2
        color = colors[i % len(colors)]
        
        # PROVERA: Ako je podkategorija "Ostalo", odmah idi na unos
        if is_other_category(subcat):
            cmd = lambda sc=subcat, mc=main_category: show_data_entry(sc, sc)
        else:
            cmd = lambda sc=subcat, mc=main_category: show_product_parts(sc, mc)
        
        btn = tk.Button(subcats_frame, text=subcat, font=("Arial", FONT_SIZE-2),
                       bg=color, fg="black", command=cmd,
                       width=18, height=3, wraplength=300)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    # RAVNOMERNA RASPOREDA
    for i in range(2):
        subcats_frame.columnconfigure(i, weight=1)
    for i in range((len(subcats) + 1) // 2):
        subcats_frame.rowconfigure(i, weight=1)

def show_main_categories():
    for widget in root.winfo_children():
        widget.destroy()
    
    create_mobile_header(root, show_language_selection, show_inventory, show_shopping_list)
    
    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # SMANJEN FONT ZA NASLOV
    tk.Label(main_frame, text=t("glavne_kategorije"), font=("Arial", FONT_SIZE + 2, "bold")).pack(pady=10)
    
    # 2 KOLONE (DVA DUGMETA U JEDNOM REDU) - SMANJEN FONT I ŠIRINA
    categories_frame = tk.Frame(main_frame)
    categories_frame.pack(expand=True, fill="both")
    
    categories = get_main_categories()
    
    for i, category in enumerate(categories):
        row = i // 2  # 2 dugmeta po redu
        col = i % 2
        
        # Pronađi srpski naziv kategorije za boje
        srpski_categories = main_categories_translations["srpski"]
        current_categories = get_main_categories()
        
        srpski_category = category
        if category in current_categories:
            index = current_categories.index(category)
            srpski_category = srpski_categories[index]
        
        color = category_colors.get(srpski_category, "#FFFFFF")
        
        # ISPRAVKA OVDE: Uvek pozivaj open_category za sve kategorije
        # open_category će sam proveriti da li je "Ostalo"
        cmd = lambda c=category: open_category(c)
        
        btn = tk.Button(categories_frame, text=category, font=("Arial", FONT_SIZE-1, "bold"),
                       bg=color, fg="black", command=cmd,
                       width=14, height=2, wraplength=400)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    # RAVNOMERNA RASPOREDA
    for i in range(2):
        categories_frame.columnconfigure(i, weight=1)
    for i in range(6):  # 6 redova za 12 kategorija
        categories_frame.rowconfigure(i, weight=1)

def show_language_selection():
    """Prikazuje izbor jezika sa ikonama zastava - PROŠIRENA VERZIJA"""
    for widget in root.winfo_children():
        widget.destroy()
    
    # OKVIR ZA NASLOV SA BOJOM #FFE183
    title_container = tk.Frame(root, bg="#FFE183", relief="solid", borderwidth=2)
    title_container.pack(pady=5, padx=10, fill="x")
    
    # NASLOV U DVA REDA - SMANJEN FONT ZA 1/3
    title_frame = tk.Frame(title_container, bg="#FFE183")
    title_frame.pack(pady=8, padx=10)
    
    # PRVI RED: Odaberi jezik na svim jezicima
    languages_line1 = [
        "Odaberi jezik",        # srpski
        "Válasszon nyelvet",    # mađarski
        "Виберіть мову",        # ukrajinski
        "Выберите язык",        # ruski
        "Choose language",      # engleski
        "Sprache auswählen"     # nemački
    ]
    
    # DRUGI RED: Kineski, španski, portugalski, francuski
    languages_line2 = [
        "选择语言",             # kineski
        "Elija idioma",         # španski
        "Escolha o idioma",     # portugalski
        "Choisir la langue"     # francuski
    ]
    
    header_font_size = FONT_SIZE - 3
    
    # PRVI RED JEZIKA
    tk.Label(title_frame, text=" | ".join(languages_line1), 
             font=("Arial", header_font_size, "bold"), fg="darkblue", bg="#FFE183",
             wraplength=root.winfo_screenwidth() - 100).pack(pady=3)
    
    # DRUGI RED JEZIKA
    tk.Label(title_frame, text=" | ".join(languages_line2), 
             font=("Arial", header_font_size, "bold"), fg="darkblue", bg="#FFE183",
             wraplength=root.winfo_screenwidth() - 100).pack(pady=3)
    
    # Okvir za dugmad jezika
    languages_frame = tk.Frame(root)
    languages_frame.pack(expand=True, fill="both", padx=10, pady=5)
    
    # ISPRAVLJENA DEFINICIJA JEZIKA - 10 JEZIKA u željenom redosledu
    languages = [
        ("Srpski", "srpski"),          # Red 0, Kolona 0
        ("Magyar", "hungary"),         # Red 0, Kolona 1
        ("Українська", "ukrajinski"),  # Red 0, Kolona 2
        
        ("Русский", "ruski"),          # Red 1, Kolona 0
        ("English", "english"),        # Red 1, Kolona 1
        ("Deutsch", "deutsch"),        # Red 1, Kolona 2
        
        ("中文", "mandarinski"),        # Red 2, Kolona 0
        ("Español", "espanol"),        # Red 2, Kolona 1
        ("Português", "portugalski"),  # Red 2, Kolona 2
        
        ("Français", "francais")       # Red 3, Kolona 0 - SAM u četvrtom redu!
    ]
    
    # VEĆE DIMENZIJE DUGMADI - 3 kolone šire dugmad
    btn_width = 160  # POVEĆANO za 3 kolone
    btn_height = 60  # POVEĆANO za bolji prikaz ikona
    
    # Kreiraj DUGMAD za sve jezike - 3 kolone, 4 reda
    for i, (lang_name, lang_code) in enumerate(languages):
        row = i // 3  # 3 dugmeta po redu
        col = i % 3   # 0, 1 ili 2
        
        # Uzmi ikonu za ovaj jezik
        icon_image = language_icons.get(lang_code)
        
        # Kreiraj DUGME sa ikonom i tekstom
        if icon_image:
            btn = tk.Button(languages_frame, 
                          text=lang_name,
                          image=icon_image,
                          compound='top',
                          font=("Arial", 9, "bold"),  # POVEĆAN FONT
                          bg="lightblue",
                          fg="black",
                          activebackground="#a8d5ff",
                          activeforeground="black",
                          wraplength=300,  # POVEĆANO
                          padx=8,
                          pady=6,
                          height=btn_height,
                          width=btn_width,
                          justify="center",
                          anchor="center",
                          command=lambda code=lang_code: set_language(code))
        else:
            # Dugme bez ikone
            btn = tk.Button(languages_frame, 
                          text=lang_name,
                          font=("Arial", 11, "bold"),  # POVEĆAN FONT
                          bg="lightblue",
                          fg="black",
                          activebackground="#a8d5ff",
                          activeforeground="black",
                          wraplength=140,
                          padx=8,
                          pady=6,
                          height=btn_height,
                          width=btn_width,
                          justify="center",
                          anchor="center",
                          command=lambda code=lang_code: set_language(code))
        
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        # Sačuvaj referencu za ikonu
        if icon_image:
            btn.image = icon_image
        
        # Hover efekat
        def make_hover(button=btn):
            def on_enter(e):
                button.config(bg="#a8d5ff")
            def on_leave(e):
                button.config(bg="lightblue")
            return on_enter, on_leave
        
        on_enter_func, on_leave_func = make_hover()
        btn.bind("<Enter>", on_enter_func)
        btn.bind("<Leave>", on_leave_func)
    
    # PRAZNA POLJA za ostatak četvrtog reda (francuski je u koloni 0)
    # Kreiraj prazna mesta u kolonama 1 i 2 četvrtog reda
    for col in [1, 2]:
        empty_space = tk.Frame(languages_frame, bg=root.cget('bg'))
        empty_space.grid(row=3, column=col, padx=8, pady=8, sticky="nsew")
    
    # Ravnomerna raspodela - 3 kolone, 4 reda
    for i in range(3):  # 3 kolone
        languages_frame.columnconfigure(i, weight=1, uniform="lang_cols")
    for i in range(4):  # 4 reda
        languages_frame.rowconfigure(i, weight=1)
    
    # Dugme za izlaz
    exit_frame = tk.Frame(root)
    exit_frame.pack(pady=15)
    
    # Koristimo privremeno srpski za dugme "Izlaz" dok se ne postavi jezik
    tk.Button(exit_frame, text="Exit", font=("Arial", BUTTON_FONT_SIZE, "bold"),
              command=exit_program, bg="red", fg="white", 
              width=20, height=2).pack()
			  
def set_language(lang_code):
    global current_language
    current_language = lang_code
    show_main_categories()
        
# ---------------- POČETNI EKRAN - SADA JE IZBOR JEZIKA ----------------
def start_screen():
    """Početni ekran - direktno prikazuje izbor jezika"""
    show_language_selection()

# ---------------- POKRETANJE PROGRAMA ----------------
if __name__ == "__main__":
    init_db()
    start_screen()
    root.mainloop()
# ... VAŠ CEo POSTOJEĆI KOD ...
