# B-ES4-AIR Ultimate – hier mit der Bestellung starten

## 1. Fünf Platinen bei JLCPCB

1. `IDM-RoomSensor-ESP-B-ES4-AIR-fabrication.zip` hochladen.
2. 4 Lagen, 1,6 mm FR-4, 1 oz Außenkupfer und 5 Stück wählen.
3. Standard-PCBA, Oberseite und THT-/Wellenlöten aktivieren.
4. `JLCPCB/JLCPCB_BOM.csv` und `JLCPCB/JLCPCB_CPL.csv` hochladen.
5. Im Viewer alle 94 Platzierungen kontrollieren, besonders Sensoren U4 und
   U8-U10, Spannungsregler U1/U2/U11, RS-485 U7, Dioden/TVS, LEDs und C30.
6. Fehlbestand oder Ersatztypen vor Bezahlung manuell klären. Keine
   automatische Substitution der Sensoren akzeptieren.

Die sechs grünen Feldanschlüsse sind Push-in-Federklemmen, aber THT und damit
JLCPCB-Wellenlötteile. Für den Nutzer ist später kein Löten nötig.

## 2. Gehäuse

Im Ordner `Gehaeuse/` liegen Grundteil, Deckel und eine gemeinsame S5-
Druckplatte. PETG ist für Technikräume bevorzugt; PLA eignet sich für den
ersten Passformtest. Schrauben und Inserts stehen in
`B-ES4-AIR-MECHANIK-BOM.csv`.

## 3. Pflichtprüfung des ersten Geräts

- erst USB-C allein, dann 24 V allein, dann beide gemeinsam, jeweils mit
  Strombegrenzung; 24 V, SYS_5V, +3V3 und AIR_3V3 messen
- USB-Flash, Reset, Boot und Service prüfen
- SHT45, SCD41, SGP41 und BMP390 auf plausible Werte und Erwärmung prüfen
- zwei bis vier DS18B20, beide Kontakteingänge und 0-10-V-Eingang testen
- 0-10-V-Ausgang kalibrieren und unter Last messen
- RS-485 galvanische Trennung und Terminierung aus/ein testen
- Gehäuse, Luftaustausch und Push-in-Zugänglichkeit prüfen

Erst danach die Klemme J1 anhand der Dokumentation der konkreten Anlage
anschließen. Die Platine trägt physisch nur Xerolux, Revision und Jahr.

