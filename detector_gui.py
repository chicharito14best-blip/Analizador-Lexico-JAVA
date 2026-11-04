import tkinter as tk
from tkinter import filedialog, messagebox
import re

# Variables globales para controlar la animación paso a paso
detalles_pendientes = []
explicacion_final = ""

def analizar_codigo(codigo_fuente):
    # Patrón actualizado para tokens básicos de JAVA (palabras reservadas, operadores, delimitadores)
    patron_palabras = re.compile(r'\b(public|class|static|void|int|String|if|else|for|while|new|return)\b')
    patron_simbolos = re.compile(r'([\{\}\(\)\[\]\;])')
    
    conteo = {'reservadas': 0, 'simbolos': 0}
    detalles = []

    en_comentario_multilinea = False

    lineas = codigo_fuente.splitlines()
    for num_linea, linea in enumerate(lineas, start=1):
        linea_limpia = linea.strip()
        
        if not linea_limpia:
            continue

        # Detectar comentarios multilínea en Java (/* ... */)
        if '/*' in linea_limpia:
            en_comentario_multilinea = True
        
        if en_comentario_multilinea:
            if '*/' in linea_limpia:
                en_comentario_multilinea = False
            continue # Ignoramos el contenido del comentario

        # Detectar comentarios de una línea en Java (//)
        if linea_limpia.startswith('//'):
            detalles.append(f"LÍNEA {num_linea}: COMENTARIO IGNORADO\n→ {linea_limpia}\n")
            continue

        # Buscar tokens en la línea
        tokens_encontrados = []
        
        # 1. Buscar palabras reservadas
        for coincidencia in patron_palabras.finditer(linea):
            tokens_encontrados.append(f"Reservada: '{coincidencia.group()}'")
            conteo['reservadas'] += 1
            
        # 2. Buscar símbolos/delimitadores
        for coincidencia in patron_simbolos.finditer(linea):
            tokens_encontrados.append(f"Símbolo: '{coincidencia.group()}'")
            conteo['simbolos'] += 1

        if tokens_encontrados:
            lista_tokens = ", ".join(tokens_encontrados)
            detalles.append(f"LÍNEA {num_linea}: TOKENS DETECTADOS\n→ {linea_limpia}\n   [ {lista_tokens} ]\n")

    return conteo, detalles

def cargar_archivo():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar código Java",
        filetypes=[("Archivos de Java", "*.java"), ("Todos los archivos", "*.*")]
    )
    
    if ruta_archivo:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                
            texto_codigo.delete('1.0', tk.END)
            texto_codigo.insert(tk.END, contenido)
            
            texto_resultados.delete('1.0', tk.END)
            texto_explicacion.delete('1.0', tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

def mostrar_siguiente_detalle():
    """Imprime el siguiente resultado con un retraso visible y hace scroll automático."""
    global detalles_pendientes, explicacion_final
    
    if detalles_pendientes:
        detalle = detalles_pendientes.pop(0)
        texto_resultados.insert(tk.END, detalle + "\n")
        texto_resultados.see(tk.END) # Scroll automático hacia abajo
        
        # Llamar a esta misma función en 500 ms (0.5 segundos)
        ventana.after(500, mostrar_siguiente_detalle)
    else:
        texto_resultados.insert(tk.END, "--- ANÁLISIS LÉXICO TERMINADO ---\n")
        texto_resultados.see(tk.END)
        # Mostrar la explicación hasta que termine la animación
        texto_explicacion.insert(tk.END, explicacion_final)

def ejecutar_detector():
    global detalles_pendientes, explicacion_final
    codigo = texto_codigo.get('1.0', tk.END).strip()
    
    if not codigo:
        messagebox.showwarning("Advertencia", "No hay código para analizar.")
        return
        
    conteo, detalles = analizar_codigo(codigo)
    
    # Preparar la explicación teórica
    explicacion_final = "RESUMEN DEL ANÁLISIS LÉXICO (JAVA):\n\n"
    explicacion_final += f"• Palabras reservadas encontradas: {conteo['reservadas']}\n"
    explicacion_final += f"• Símbolos/Delimitadores encontrados: {conteo['simbolos']}\n\n"
    explicacion_final += "FUNCIONAMIENTO:\n"
    explicacion_final += "El analizador léxico escaneó el código fuente carácter por carácter para agruparlos en 'Tokens' con significado para el compilador de Java, ignorando los espacios y los comentarios (// y /* */)."
    
    texto_resultados.delete('1.0', tk.END)
    texto_explicacion.delete('1.0', tk.END)
    
    if detalles:
        detalles_pendientes = detalles.copy()
        texto_resultados.insert(tk.END, "INICIANDO ANÁLISIS PASO A PASO...\n\n")
        mostrar_siguiente_detalle() # Inicia el bucle de animación
    else:
        texto_resultados.insert(tk.END, "NO SE ENCONTRARON TOKENS DE JAVA.\n")
        texto_explicacion.insert(tk.END, explicacion_final)

# ==========================================
# CONFIGURACIÓN VISUAL Y VENTANA
# ==========================================
COLOR_FONDO_APP = "#E5F0F9"
COLOR_BOTONES = "#2C5B9C"
COLOR_TEXTO_TITULO = "#1A2E4C"
COLOR_FONDO_EDITOR = "#121A2F"
COLOR_TEXTO_EDITOR = "#8BE9FD"
COLOR_MARCOS = "#C4DDF0"

ventana = tk.Tk()
ventana.title("Analizador Léxico en Python para JAVA")
ventana.geometry("1200x700")
ventana.configure(bg=COLOR_FONDO_APP)

# --- PANEL SUPERIOR (Botones y Título) ---
frame_top = tk.Frame(ventana, bg=COLOR_FONDO_APP)
frame_top.pack(fill=tk.X, padx=20, pady=15)

# Textos actualizados para JAVA
btn_cargar = tk.Button(frame_top, text="📂 CARGAR ARCHIVO .JAVA", command=cargar_archivo, 
                       bg=COLOR_BOTONES, fg="white", font=("Segoe UI", 11, "bold"), 
                       relief="flat", padx=15, pady=8, cursor="hand2")
btn_cargar.pack(side=tk.LEFT, padx=(0, 10))

btn_analizar = tk.Button(frame_top, text="🔍 INICIAR ANÁLISIS", command=ejecutar_detector, 
                         bg=COLOR_BOTONES, fg="white", font=("Segoe UI", 11, "bold"), 
                         relief="flat", padx=15, pady=8, cursor="hand2")
btn_analizar.pack(side=tk.LEFT)

lbl_titulo = tk.Label(frame_top, text="ANALIZADOR LÉXICO (JAVA)", 
                      bg=COLOR_FONDO_APP, fg=COLOR_TEXTO_TITULO, font=("Segoe UI", 16, "bold"))
lbl_titulo.pack(side=tk.RIGHT)

# --- PANEL CENTRAL (3 Columnas) ---
frame_central = tk.Frame(ventana, bg=COLOR_FONDO_APP)
frame_central.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

frame_central.columnconfigure(0, weight=1, uniform="col")
frame_central.columnconfigure(1, weight=1, uniform="col")
frame_central.columnconfigure(2, weight=1, uniform="col")
frame_central.rowconfigure(0, weight=1)

def crear_columna(parent, col, titulo, bg_contenido, fg_contenido, font_contenido):
    marco = tk.Frame(parent, bg=COLOR_MARCOS, bd=2, relief="flat")
    marco.grid(row=0, column=col, sticky="nsew", padx=10, pady=5)
    
    lbl_header = tk.Label(marco, text=titulo, bg=COLOR_MARCOS, fg=COLOR_TEXTO_TITULO, 
                          font=("Segoe UI", 12, "bold"), pady=10)
    lbl_header.pack(fill=tk.X)
    
    texto = tk.Text(marco, wrap=tk.WORD, font=font_contenido, bg=bg_contenido, fg=fg_contenido, bd=0, padx=10, pady=10)
    texto.pack(fill=tk.BOTH, expand=True, padx=2, pady=(0, 2))
    return texto

texto_codigo = crear_columna(frame_central, 0, "</> CÓDIGO FUENTE JAVA", COLOR_FONDO_EDITOR, COLOR_TEXTO_EDITOR, ("Consolas", 11))
texto_resultados = crear_columna(frame_central, 1, "≡ PROCESO PASO A PASO", "white", "#333333", ("Segoe UI", 11, "bold"))
texto_explicacion = crear_columna(frame_central, 2, "📄 EXPLICACIÓN TEÓRICA", "white", "#333333", ("Segoe UI", 11))

if __name__ == "__main__":
    ventana.mainloop()