DDR Pad Controller

Dit is een Python-script dat seriële communicatie gebruikt om een DDR (Dance Dance Revolution) Pad aan te sturen via een ESP32. Dit project is ontwikkeld als een eindopdracht en biedt een alternatieve oplossing omdat de ESP32 geen HID (Human Interface Device) functionaliteit ondersteunt.

🎯 Doel

De ESP32 kan niet direct worden gebruikt als een toetsenbord (HID), daarom wordt seriële communicatie gebruikt om knoppen van het DDR-pad door te sturen naar een computer. Dit script vertaalt de ontvangen seriële signalen naar toetsaanslagen.

🛠 Functionaliteiten

Automatische of handmatige selectie van de juiste COM-poort.

Seriële verbinding maken en verbreken via een eenvoudige GUI.

Handshake-systeem om de verbinding met de ESP32 te bevestigen.

Leest de input van de ESP32 (W, A, S, D) en simuleert pijltjestoetsen.

W ➝ ⬆️ Up Arrow

A ➝ ⬅️ Left Arrow

S ➝ ⬇️ Down Arrow

D ➝ ➡️ Right Arrow

Logt de ontvangen signalen in een GUI-venster.

Herkent en herstelt verbroken verbindingen automatisch.

🖥 Installatie

Python installeren (indien nog niet geïnstalleerd):

Download en installeer Python 3.8+ via python.org

Benodigde bibliotheken installeren:

pip install pyserial pynput tkinter

Sluit je ESP32 aan via USB en check welke COM-poort wordt gebruikt.

Start het script:

python ddr_controller.py

⚙️ Hardware Setup

ESP32 pinout voor DDR Pad:

GPIO 12 = Up (W)

GPIO 13 = Left (A)

GPIO 14 = Down (S)

GPIO 15 = Right (D)

Verbind de knoppen van je DDR-pad met de ESP32 en zorg dat deze correct worden uitgelezen.

📜 Hoe het Werkt

Start het Python-script en selecteer de juiste COM-poort.

De ESP32 stuurt "HANDSHAKE" totdat het script reageert met "CONNECTED".

Vanaf dat moment zal de ESP32 elke keer dat een knop wordt ingedrukt de bijbehorende toets (W, A, S, D) via de seriële poort versturen.

Het Python-script vertaalt deze naar de juiste pijltjestoetsen en simuleert deze.

Wanneer de verbinding wordt verbroken, probeert het script automatisch opnieuw verbinding te maken.

🛠 Mogelijke Problemen & Oplossingen

❌ "Kan niet verbinden met COM-poort"

Zorg ervoor dat je de juiste poort hebt geselecteerd.

Controleer of geen ander programma de poort bezet houdt.

❌ "ESP32 blijft in Connected Mode hangen"

Als het script crasht, blijft de ESP32 in de connected state. Start de ESP32 opnieuw of stuur handmatig een "DISCONNECT" signaal.

❌ "Knoppen werken niet"

Controleer of de GPIO-pinout correct is aangesloten.

Open de Seriële Monitor in de Arduino IDE en kijk of de ESP32 de juiste signalen verstuurt.

📌 Toekomstige Verbeteringen

Automatische COM-poort detectie en directe verbinding.

Visuele feedback in de GUI voor ingedrukte toetsen.

Extra configuratie-opties voor aangepaste toetsbindingen.

👨‍💻 Bijdragen

Pull requests en suggesties zijn welkom! Dit is een leerproject en alle hulp om het te verbeteren wordt gewaardeerd.

🚀 Veel plezier met je DDR Pad!

