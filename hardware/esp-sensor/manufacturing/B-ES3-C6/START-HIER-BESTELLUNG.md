# B-ES3-C6: Start hier – Bestellung von 5 Engineering Samples

Dieses Paket ist für die Bestellung und Bestückung der B-ES3-C6-Platine bei
JLCPCB vorbereitet. Es ist eine Engineering-Sample-Freigabe für zunächst fünf
Platinen. Erst nach dem Erststücktest darf die Platine an eine Wärmepumpe oder
in eine größere Serie gehen.

## 1. PCB und Bestückung bei JLCPCB

1. `IDM-RoomSensor-ESP-B-ES3-C6-fabrication.zip` als PCB-Datei hochladen.
2. Vier Lagen, 1,6 mm FR-4 und 1 oz Außenkupfer auswählen.
3. Stückzahl 5 auswählen.
4. Standard PCBA, Bestückungsseite oben und THT/Wave-Soldering aktivieren.
5. `JLCPCB/JLCPCB_BOM.csv` als BOM hochladen.
6. `JLCPCB/JLCPCB_CPL.csv` als CPL/Pick-and-Place-Datei hochladen.
7. Im JLCPCB-Viewer jede Orientierung prüfen, besonders U1-U7, D1-D4,
   TVS1-TVS5, LED1-LED3, J3, SW3 und J1/J2/J5-J8.
8. Keine automatische Bauteilsubstitution akzeptieren. Bei fehlendem Bestand
   erst Rücksprache halten bzw. die Teile vorbestellen.

Die sechs grünen Feldanschlüsse sind Push-in-Federklemmen. J1/J2/J5-J8 sind
THT-Bauteile und benötigen die THT-/Wellenlötoption. Die detaillierte Stückliste
pro Platine steht in `B-ES3-C6-BOM.csv`; die JLCPCB-Uploadliste enthält 53
BOM-Zeilen und 80 bestückte Positionen pro Platine.

## 2. Gehäuse drucken

Das komplette Gehäusepaket liegt unter `Gehaeuse/`. Für einen UltiMaker S5 mit
AA 0.4 Print Core und UltiMaker PLA kann der vorbereitete G-Code verwendet
werden. Bei PETG, ASA, anderem PLA oder anderer Düse die kombinierte S5-STL neu
slicen.

Benötigte Schrauben und Inserts stehen in `B-ES3-C6-MECHANIK-BOM.csv`.

## 3. Zwingender Erststücktest

- USB allein, 24 V allein und beide Versorgungen gemeinsam mit Strombegrenzung
- 24-V-, 5-V- und 3,3-V-Schiene messen
- Flashen über USB-C, Reset, Boot und Service-Taster prüfen
- SHT45 sowie einen bis vier DS18B20 testen
- 0-10-V-Ausgang kalibrieren und 0-10-V-Eingang bei 0/5/10 V prüfen
- beide Kontakteingänge sowie RS-485 mit Terminierung aus/ein testen
- Gehäuseschluss, Klemmenzugang und Temperaturverhalten prüfen
- J1 erst danach und nur gegen die Dokumentation der konkreten IDM-Anlage
  anschließen

Die aktuelle Lager- und Preisfreigabe erfolgt immer erst im JLCPCB-BOM-Viewer,
da Bestand, Vorbestellung und Extended-/Standard-Status dynamisch sind.
