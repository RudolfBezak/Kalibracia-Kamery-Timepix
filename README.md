# Kalibrácia Kamery Timepix

## Popis
Aplikácia na kalibráciu detektora Timepix - spracovanie spektrálnych dát a kalibráciu pixelov.

## Inštalácia

### Požiadavky
- Python 3.13
- Knižnice: tkinter, matplotlib, numpy, scipy

### Inštalácia závislostí
```bash
pip install -r requirements.txt
```

## Spustenie

### Spustenie zo zdrojového kódu
```bash
cd step1
python UI.py
```

### Spustenie z exe súboru
```bash
.\dist\calibration.exe
```

## Použitie

1. **Per pixel spektrá** - Spracovanie surových dát z `.clog` súborov
2. **Zobrazenie dát** - Zobrazenie histogramov a kalibračných kriviek
3. **Kalibrovanie** - Automatická kalibrácia pomocou známych energetických píkov

## Buildovanie exe súboru

### Vytvorenie spustiteľného súboru
```bash
pyinstaller UI.spec
```

Výsledný súbor bude v `dist\calibration.exe` (~70 MB).

### Poznámky k buildovaniu
- Spec súbor vylučuje veľké ML knižnice (torch, tensorflow, cv2, numba) pre menšiu veľkosť
- Console window je zapnuté pre ladenie
- Pre vypnutie konzoly zmeň `console=True` na `console=False` v `UI.spec`

## Štruktúra projektu

```
step1/
  ├── UI.py                              # Hlavné GUI
  ├── rawDataToCalibrationData.py        # Spracovanie surových dát
  ├── multithreadingFitting.py           # Viacvláknové fitovanie
  ├── americium4peaky.py                 # Detekcia ameríciových píkov
  ├── custom_function.py                 # Kalibračná funkcia
  ├── printHistogram.py                  # Zobrazenie histogramov
  ├── printHistogramCalibrated.py        # Zobrazenie kalibrovaných histogramov
  └── globals.py                         # Globálne konštanty

UI.spec                                  # PyInstaller konfigurácia
```

## Kalibračné súbory

Po kalibrácii sa vytvárajú súbory:
- `calib_a.txt` - Parameter a kalibračnej funkcie
- `calib_b.txt` - Parameter b kalibračnej funkcie
- `calib_c.txt` - Parameter c kalibračnej funkcie
- `calib_t.txt` - Parameter t kalibračnej funkcie

## Workflow

1. Najprv si tam hoď `.clog` súbory s dátami
2. Spusti "Per pixel spektrá" a spracuj surové dáta
3. V sekcii "Kalibrovanie" pridaj ameríciové/iné známe zdroje
4. Aplikácia vytvorí kalibračné súbory
5. V sekcii "Zobrazenie dát" môžeš zobraziť výsledky
