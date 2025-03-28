DDR Pad Controller

This is a Python script that uses serial communication to control a DDR (Dance Dance Revolution) Pad via an ESP32. This project was developed as a final assignment and provides an alternative solution because the ESP32 does not support HID (Human Interface Device) functionality.

🎯 Purpose

The ESP32 cannot be used directly as a keyboard (HID), so serial communication is used to send button presses from the DDR pad to a computer. This script translates the received serial signals into keystrokes.

🛠 Features

Automatic or manual selection of the correct COM port.

Establish and disconnect serial connections via a simple GUI.

Handshake system to confirm the connection with the ESP32.

Reads input from the ESP32 (W, A, S, D) and simulates arrow key presses.

W ➝ ⬆️ Up Arrow

A ➝ ⬅️ Left Arrow

S ➝ ⬇️ Down Arrow

D ➝ ➡️ Right Arrow

Logs received signals in a GUI window.

Detects and recovers lost connections automatically.

🖥 Installation

Install Python (if not already installed):

Download and install Python 3.8+ from python.org

Install required libraries:

pip install pyserial pynput tkinter

Connect your ESP32 via USB and check which COM port is being used.

Start the script:

python ddr_controller.py

⚙️ Hardware Setup

ESP32 pinout for DDR Pad:

GPIO 12 = Up (W)

GPIO 13 = Left (A)

GPIO 14 = Down (S)

GPIO 15 = Right (D)

Connect the buttons of your DDR pad to the ESP32 and ensure they are correctly read.

📜 How It Works

Start the Python script and select the correct COM port.

The ESP32 sends "HANDSHAKE" until the script responds with "CONNECTED".

From that moment, every time a button is pressed, the ESP32 will send the corresponding key (W, A, S, D) via the serial port.

The Python script translates these into the correct arrow key presses and simulates them.

When the connection is lost, the script attempts to reconnect automatically.

🛠 Possible Issues & Solutions

❌ "Cannot connect to COM port"

Ensure you have selected the correct port.

Check if another program is using the port.

❌ "ESP32 remains in Connected Mode"

If the script crashes, the ESP32 remains in the connected state. Restart the ESP32 or manually send a "DISCONNECT" signal.

❌ "Buttons are not working"

Check if the GPIO pinout is correctly connected.

Open the Serial Monitor in the Arduino IDE and see if the ESP32 is sending the correct signals.

📌 Future Improvements

Automatic COM port detection and direct connection.

Visual feedback in the GUI for pressed keys.

Additional configuration options for custom key bindings.

👨‍💻 Contributions

Pull requests and suggestions are welcome! This is a learning project, and any help to improve it is appreciated.

🚀 Enjoy your DDR Pad!

