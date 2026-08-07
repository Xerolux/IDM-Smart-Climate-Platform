# B-ES5-MODULAR – hier mit der Bestellung starten

## 1. Basisplatine bei JLCPCB

1. `IDM-RoomSensor-ESP-B-ES5-MODULAR-fabrication.zip` hochladen.
2. 4 Lagen, 1,6 mm FR-4, 1 oz Außenkupfer und zunächst 5 Stück wählen.
3. Standard-PCBA, Oberseite und THT-/Wellenlöten aktivieren.
4. `JLCPCB/JLCPCB_BOM.csv` und `JLCPCB/JLCPCB_CPL.csv` hochladen.
5. Alle 84 Platzierungen prüfen, besonders U1-U7, U4/SHT45, USB-C, Dioden,
   C30 sowie J9-J11.

## 2. Gewünschte Module

Für jedes gewünschte Modul den gleichnamigen Ordner unter `Modules/` öffnen
und dessen Fabrication-ZIP, BOM und CPL als eigenen PCBA-Auftrag hochladen.
Auch die Module sind vierlagig. J1 ist jeweils auf der Unterseite; alle übrigen
Bauteile sind auf der Oberseite.

- `AIR-CO2`: SCD41
- `AIR-VOCNOX`: SGP41
- `AIR-PRESSURE`: BMP390

Die Basis-Stecker C225519 waren bei der Paketprüfung einzeln verfügbar. Die
weibliche Modulbuchse C58378 war nur per Vorbestellung/Mindestmenge gelistet.
Lagerbestand, Preis, Ausrichtung und Beschaffungsoption unmittelbar vor der
Bezahlung erneut prüfen. Keine automatische Sensor-Substitution akzeptieren.

## 3. Gehäuse und Inbetriebnahme

Gehäuse-STLs und S5-Profil liegen in `Gehaeuse/`. Vor dem Aufstecken Versorgung
abschalten. Das Pinout ist bei 180 Grad elektrisch sicher, die vorgesehene
Orientierung zeigt jedoch mit den Sensorflächen zum großen Lüftungsfeld.

Erst USB allein, dann 24 V allein und danach beide Quellen gemeinsam mit
Strombegrenzung testen. Anschließend Module einzeln einsetzen und den I2C-Scan
sowie plausible Messwerte prüfen.

