import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser


#Instalar liberira
# pip install yt-dlp

# Función para seleccionar la carpeta de destino
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, carpeta)

# Función para descargar el video en la mejor calidad
def descargar_video():
    video_url = entry_url.get()
    download_path = entry_ruta.get()

    if not video_url or not download_path:
        messagebox.showerror("Error", "Por favor, ingresa la URL y la carpeta de destino.")
        return

    label_estado.config(text="Iniciando descarga en máxima calidad...")

    try:
        # Comando yt-dlp para descargar en máxima calidad (mejor video + mejor audio)
        comando = f'yt-dlp -f bestvideo+bestaudio --merge-output-format mp4 "{video_url}" -o "{download_path}/%(title)s.%(ext)s"'
        
        # Ejecutar el comando
        proceso = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if proceso.returncode == 0:
            label_estado.config(text="Video descargado correctamente en máxima calidad.")
        else:
            label_estado.config(text=f"Ocurrió un error: {proceso.stderr}")

    except Exception as e:
        label_estado.config(text=f"Error: {str(e)}")

# Función para ver el video en un navegador
def ver_video():
    video_url = entry_url.get()
    if "=" in video_url:
        video_id = video_url.split("=")[-1]
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        webbrowser.open(embed_url)
    else:
        messagebox.showerror("Error", "URL de YouTube no válida.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Descargador de YouTube en Máxima Calidad")
ventana.geometry("500x250")

# Elementos de la interfaz
tk.Label(ventana, text="URL del Video:").pack(pady=5)
entry_url = tk.Entry(ventana, width=50)
entry_url.pack(pady=5)

tk.Label(ventana, text="Ruta de Descarga:").pack(pady=5)
entry_ruta = tk.Entry(ventana, width=50)
entry_ruta.pack(pady=5)
btn_ruta = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
btn_ruta.pack(pady=5)

btn_descargar = tk.Button(ventana, text="Descargar en Máxima Calidad", command=descargar_video)
btn_descargar.pack(pady=5)

btn_ver = tk.Button(ventana, text="Ver Video", command=ver_video)
btn_ver.pack(pady=5)

label_estado = tk.Label(ventana, text="", fg="blue")
label_estado.pack(pady=10)

# Iniciar el loop de la interfaz
ventana.mainloop()



