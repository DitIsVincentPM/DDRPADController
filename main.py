import serial
import serial.tools.list_ports
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pynput.keyboard import Controller, Key

keyboard = Controller()
ser = None  # Globale variabele voor de seriële connectie
held_keys = set()  # Houdt bij welke toetsen ingedrukt zijn

def list_ports():
    """Zoekt alle beschikbare COM-poorten en vult de dropdown"""
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

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

def listen_serial():
    """Luistert naar seriële input en simuleert toetsenbordacties"""
    global ser, held_keys
    key_mapping = {
        "W": Key.up,
        "A": Key.left,
        "S": Key.down,
        "D": Key.right
    }

    while ser and ser.is_open:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()

                if data.endswith("_PRESSED"):
                    key = data.split("_")[0]
                    if key in key_mapping and key not in held_keys:
                        keyboard.press(key_mapping[key])
                        held_keys.add(key)
                        log_text.insert(tk.END, f"Pressed: {key} (Holding)\n")

                elif data.endswith("_RELEASED"):
                    key = data.split("_")[0]
                    if key in key_mapping and key in held_keys:
                        keyboard.release(key_mapping[key])
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
root.mainloop()
