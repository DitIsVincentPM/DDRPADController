import serial
import serial.tools.list_ports
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pynput.keyboard import Controller, Key

keyboard = Controller()
ser = None  # Globale variabele voor de seriële connectie


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
        print(f"Proberen te verbinden met {selected_port}...")  # Debugging: toon geselecteerde poort
        ser = serial.Serial(selected_port, 115200, timeout=1)
        time.sleep(2)  # Wacht op ESP32
        ser.write(b"CONNECTED\n")  # Stuur connectie-signaal naar ESP32
        print(f"Verbonden met {selected_port}")  # Debugging: verbindingssucces

        status_label.config(text=f"Verbonden met {selected_port}", foreground="green")
        threading.Thread(target=listen_serial, daemon=True).start()

    except Exception as e:
        print(f"Fout bij verbinden: {e}")  # Extra foutmelding voor debugging
        messagebox.showerror("Fout", f"Kan niet verbinden met {selected_port}\n{e}")


def disconnect():
    """Verbreekt de seriële verbinding"""
    global ser
    if ser:
        print("Verbinding verbreken...")  # Debugging: bevestigen dat we disconnecten
        ser.write(b"DISCONNECT\n")  # Stuur een disconnect signaal naar de ESP32
        ser.close()
        ser = None
        status_label.config(text="Niet verbonden", foreground="red")
        print("Verbinding verbroken.")  # Debugging: bevestigen dat de verbinding gesloten is
    else:
        print("Geen actieve verbinding om te verbreken.")  # Debugging: geen verbinding


def listen_serial():
    """Luistert naar seriële input en simuleert toetsenbordacties"""
    global ser
    while ser and ser.is_open:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()
                if data == "W":
                    keyboard.press(Key.up)   # W -> Up Arrow
                    keyboard.release(Key.up)
                    log_text.insert(tk.END, f"Pressed: W (Up Arrow)\n")
                elif data == "A":
                    keyboard.press(Key.left)  # A -> Left Arrow
                    keyboard.release(Key.left)
                    log_text.insert(tk.END, f"Pressed: A (Left Arrow)\n")
                elif data == "S":
                    keyboard.press(Key.down)  # S -> Down Arrow
                    keyboard.release(Key.down)
                    log_text.insert(tk.END, f"Pressed: S (Down Arrow)\n")
                elif data == "D":
                    keyboard.press(Key.right)  # D -> Right Arrow
                    keyboard.release(Key.right)
                    log_text.insert(tk.END, f"Pressed: D (Right Arrow)\n")
                log_text.yview(tk.END)
        except serial.SerialException as e:
            print(f"Fout tijdens het luisteren naar de seriële poort: {e}")  # Error handling for disconnects
            disconnect()  # Force a disconnect if the port is not responding
            break
        except Exception as e:
            print(f"Onverwachte fout: {e}")  # Fout bij andere uitzonderingen
            break

def check_connection():
    """Controleer regelmatig of de seriële verbinding nog open is"""
    global ser
    while True:
        if ser and ser.is_open:
            try:
                # Probeer om een klein commando te lezen, bijvoorbeeld een lege lijn, om te controleren of de verbinding nog actief is
                ser.write(b"\n")  # Stuur een kleine byte om te controleren of de poort reageert
                time.sleep(1)
            except serial.SerialException:
                print("Verbinding met ESP32 verloren!")  # Debugging: laat zien dat de verbinding is verloren
                disconnect()  # Sluit de verbinding als er een probleem is
                status_label.config(text="Verbinding verloren", foreground="orange")
        else:
            print("Geen actieve seriële verbinding!")
            time.sleep(1)  # Wacht 1 seconde voordat opnieuw wordt gecontroleerd


# 🌟 GUI Aanmaken
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

# Start de controle-thread voor verbinding
threading.Thread(target=check_connection, daemon=True).start()

# Zorg ervoor dat we altijd de verbinding netjes sluiten als het programma afsluit
def on_closing():
    print("Afsluiten programma...")
    if ser:
        disconnect()
    root.destroy()


root.protocol("WM_DELETE_WINDOW",
              on_closing)  # Zorg ervoor dat de verbinding goed wordt gesloten als het venster wordt gesloten

root.mainloop()
