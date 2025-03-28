import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Función para seleccionar la carpeta de destino
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry_ruta.delete(0, tk.END)
        entry_ruta.insert(0, carpeta)

# Función para descargar el video en la mejor calidad en un solo archivo
def descargar_video():
    video_url = entry_url.get()
    download_path = entry_ruta.get()

    if not video_url or not download_path:
        messagebox.showerror("Error", "Por favor, ingresa la URL y la carpeta de destino.")
        return

    label_estado.config(text="Iniciando descarga en máxima calidad...")

    try:
        # Descargar en un solo archivo (mkv, mp4, etc.)
        comando = f'yt-dlp -f "bv*+ba/b" --merge-output-format mkv "{video_url}" -o "{download_path}/%(title)s.mkv"'
        
        # Ejecutar el comando
        proceso = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if proceso.returncode == 0:
            label_estado.config(text="Video descargado correctamente en máxima calidad.")
        else:
            label_estado.config(text=f"Ocurrió un error: {proceso.stderr}")

    except Exception as e:
        label_estado.config(text=f"Error: {str(e)}")

# Crear ventana
ventana = tk.Tk()
ventana.title("Descargador de YouTube en Máxima Calidad")
ventana.geometry("600x300")
ventana.config(bg="#f4f4f9")  # Fondo color claro

# Encabezado
label_titulo = tk.Label(ventana, text="Descargador de YouTube", font=("Arial", 18, "bold"), bg="#f4f4f9")
label_titulo.pack(pady=10)

# Elementos de la interfaz
frame = tk.Frame(ventana, bg="#f4f4f9")
frame.pack(pady=20)

tk.Label(frame, text="URL del Video:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, padx=10, pady=5)
entry_url = tk.Entry(frame, width=40, font=("Arial", 12))
entry_url.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Ruta de Descarga:", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, padx=10, pady=5)
entry_ruta = tk.Entry(frame, width=40, font=("Arial", 12))
entry_ruta.grid(row=1, column=1, padx=10, pady=5)

# Botón para seleccionar la carpeta
btn_ruta = ttk.Button(frame, text="Seleccionar Carpeta", command=seleccionar_carpeta, style="TButton")
btn_ruta.grid(row=2, columnspan=2, pady=10)

# Botón para descargar
btn_descargar = ttk.Button(ventana, text="Descargar en Máxima Calidad", command=descargar_video, style="TButton")
btn_descargar.pack(pady=10)

# Etiqueta para mostrar el estado
label_estado = tk.Label(ventana, text="", font=("Arial", 12), fg="blue", bg="#f4f4f9")
label_estado.pack(pady=10)

# Estilo para los botones con texto negro
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, relief="flat", background="#4CAF50", foreground="black")  # Cambio de color de texto
style.map("TButton", background=[("active", "#45a049")])

# Iniciar el loop de la interfaz
ventana.mainloop()
