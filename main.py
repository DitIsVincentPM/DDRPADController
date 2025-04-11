import serial
import serial.tools.list_ports
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pynput.keyboard import Controller, Key
import json
import os

keyboard = Controller()
ser = None  # Globale variabele voor de seriële connectie
held_keys = set()  # Houdt bij welke toetsen ingedrukt zijn
key_mapping = {}  # Dit wordt gevuld met de gebruikersmapping
mapping_file = "key_mapping.json"


def list_ports():
    """Zoekt alle beschikbare COM-poorten en vult de dropdown"""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]


def load_mapping():
    """Laadt de key mapping uit een bestand als deze bestaat"""
    global key_mapping
    if os.path.exists(mapping_file):
        with open(mapping_file, "r") as f:
            key_mapping = json.load(f)
    else:
        key_mapping = {}  # Lege mapping als er geen bestand is


def save_mapping():
    """Slaat de key mapping op naar een bestand"""
    with open(mapping_file, "w") as f:
        json.dump(key_mapping, f)


def connect():
    """Verbindt als de juiste poort is geselecteerd"""
    global ser
    selected_port = port_var.get()

    if not selected_port:
        messagebox.showwarning("Fout", "Selecteer een COM-poort!")
        return

    try:
        ser = serial.Serial(selected_port, 115200, timeout=1)
        time.sleep(2)  # Wacht op ESP32
        ser.write(b"CONNECTED\n")  # Stuur connectie-signaal naar ESP32

        status_label.config(text=f"Verbonden met {selected_port}", foreground="green")

        if not key_mapping:  # Als er nog geen mapping is, start het instellen
            threading.Thread(target=setup_mapping, daemon=True).start()
        else:
            threading.Thread(target=listen_serial, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Fout", f"Kan niet verbinden met {selected_port}\n{e}")


def disconnect():
    """Verbreekt de seriële verbinding"""
    global ser
    if ser:
        ser.write(b"DISCONNECT\n")  # Stuur een disconnect signaal naar de ESP32
        ser.close()
        ser = None
        status_label.config(text="Niet verbonden", foreground="red")


def is_valid_button_input(data):
    return data.endswith("_PRESSED")

def setup_mapping():
    """Vraagt de gebruiker om de knoppen in te stellen"""
    global key_mapping
    key_mapping.clear()

    keys_to_map = ["W", "A", "S", "D"]

    for key in keys_to_map:
        log_text.insert(tk.END, f"Druk op een knop voor {key}...\n")
        log_text.yview(tk.END)

        while True:
            if ser and ser.is_open and ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()

                if not is_valid_button_input(data):
                    continue  # overslaan als het ruis of boot-info is

                button_id = data.replace("_PRESSED", "")  # strip de suffix

                if button_id not in key_mapping.values():  # Zorgt dat dezelfde knop niet twee keer wordt gebruikt
                    key_mapping[key] = button_id
                    log_text.insert(tk.END, f"{key} is nu gekoppeld aan: {button_id}\n")
                    log_text.yview(tk.END)
                    break

    save_mapping()
    log_text.insert(tk.END, "Key mapping voltooid!\n")
    threading.Thread(target=listen_serial, daemon=True).start()

def listen_serial():
    """Luistert naar seriële input en simuleert toetsenbordacties"""
    global ser, held_keys

    keyboard_keys = {
        "W": Key.up,
        "A": Key.left,
        "S": Key.down,
        "D": Key.right
    }

    while ser and ser.is_open:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()

                for key, button_id in key_mapping.items():
                    if data == f"{button_id}_PRESSED":
                        if key not in held_keys:
                            keyboard.press(keyboard_keys[key])
                            held_keys.add(key)
                            log_text.insert(tk.END, f"Pressed: {key} (Holding)\n")
                            log_text.yview(tk.END)

                    elif data == f"{button_id}_RELEASED":
                        if key in held_keys:
                            keyboard.release(keyboard_keys[key])
                            held_keys.remove(key)
                            log_text.insert(tk.END, f"Released: {key}\n")
                            log_text.yview(tk.END)

        except serial.SerialException:
            disconnect()
            break
        except Exception as e:
            print(f"Onverwachte fout: {e}")
            break

# GUI Setup
root = tk.Tk()
root.title("DDR Pad Controller door Vincent")
root.geometry("400x300")

ttk.Label(root, text="Selecteer COM-poort:").pack(pady=5)

port_var = tk.StringVar()
port_dropdown = ttk.Combobox(root, textvariable=port_var, values=list_ports())
port_dropdown.pack(pady=5)

refresh_button = ttk.Button(root, text="🔄 Vernieuwen", command=lambda: port_dropdown.config(values=list_ports()))
refresh_button.pack(pady=5)

connect_button = ttk.Button(root, text="🔗 Verbinden", command=connect)
connect_button.pack(pady=5)

disconnect_button = ttk.Button(root, text="❌ Verbreken", command=disconnect)
disconnect_button.pack(pady=5)

status_label = ttk.Label(root, text="Niet verbonden", foreground="red")
status_label.pack(pady=10)

log_text = tk.Text(root, height=8, width=40)
log_text.pack(pady=5)


def on_closing():
    if ser:
        disconnect()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Laad de bestaande mapping bij het starten
load_mapping()

root.mainloop()
