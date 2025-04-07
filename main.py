import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
import re

# Función para seleccionar la carpeta de destino
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, carpeta)

# Función que actualiza la descarga en un hilo
def hilo_descarga():
    video_url = entry_url.get()
    download_path = entry_ruta.get()

    if not video_url or not download_path:
        messagebox.showerror("Error", "Por favor, ingresa la URL y la carpeta de destino.")
        return

    label_estado.config(text="Iniciando descarga en máxima calidad...")
    barra_progreso["value"] = 0
    ventana.update_idletasks()

    try:
        comando = [
            'yt-dlp',
            '-f', 'bv*+ba/b',
            '--merge-output-format', 'mkv',
            video_url,
            '-o', f'{download_path}/%(title)s.%(ext)s'
        ]

        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        for linea in proceso.stdout:
            print(linea.strip())  # Opcional: para debug
            porcentaje = extraer_porcentaje(linea)
            if porcentaje is not None:
                barra_progreso["value"] = porcentaje
                ventana.update_idletasks()

        proceso.wait()
        if proceso.returncode == 0:
            label_estado.config(text="Video descargado correctamente.")
        else:
            label_estado.config(text="Ocurrió un error en la descarga.")

    except Exception as e:
        label_estado.config(text=f"Error: {str(e)}")

# Función para extraer porcentaje de una línea de salida
def extraer_porcentaje(linea):
    # Busca líneas como "[download]  42.3%"
    match = re.search(r"\[download\]\s+(\d{1,3}\.\d)%", linea)
    if match:
        return float(match.group(1))
    return None

# Función que lanza el hilo de descarga
def descargar_video():
    threading.Thread(target=hilo_descarga, daemon=True).start()

# Crear ventana
ventana = tk.Tk()
ventana.title("Descargador de YouTube en Máxima Calidad")
ventana.geometry("600x350")
ventana.config(bg="#f4f4f9")

label_titulo = tk.Label(ventana, text="Descargador de YouTube", font=("Arial", 18, "bold"), bg="#f4f4f9")
label_titulo.pack(pady=10)

frame = tk.Frame(ventana, bg="#f4f4f9")
frame.pack(pady=20)

tk.Label(frame, text="URL del Video:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, padx=10, pady=5)
entry_url = tk.Entry(frame, width=40, font=("Arial", 12))
entry_url.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Ruta de Descarga:", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, padx=10, pady=5)
entry_ruta = tk.Entry(frame, width=40, font=("Arial", 12))
entry_ruta.grid(row=1, column=1, padx=10, pady=5)

btn_ruta = ttk.Button(frame, text="Seleccionar Carpeta", command=seleccionar_carpeta)
btn_ruta.grid(row=2, columnspan=2, pady=10)

btn_descargar = ttk.Button(ventana, text="Descargar en Máxima Calidad", command=descargar_video)
btn_descargar.pack(pady=10)

label_estado = tk.Label(ventana, text="", font=("Arial", 12), fg="blue", bg="#f4f4f9")
label_estado.pack(pady=10)

# Barra de progreso
barra_progreso = ttk.Progressbar(ventana, orient="horizontal", length=400, mode="determinate")
barra_progreso.pack(pady=10)

# Estilo para los botones
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, relief="flat", background="#4CAF50", foreground="black")
style.map("TButton", background=[("active", "#45a049")])

ventana.mainloop()
