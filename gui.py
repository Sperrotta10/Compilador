import tkinter as tk
from tkinter import scrolledtext, font
from analizador import lexer  # Importar la función lexer desde el archivo analizador.py

def analyze_code():
    code = input_text.get("1.0", tk.END)  # Obtener el código del textfield
    try:
        tokens = lexer(code)  # Llamar a la función lexer
        output_text.delete("1.0", tk.END)  # Limpiar el textfield de salida
        for token_type, value in tokens:
            output_text.insert(tk.END, f"{token_type}: {value}\n")  # Mostrar los tokens en el textfield de salida
    except SyntaxError as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Analizador Léxico")
root.geometry("1000x600")  # Tamaño de la ventana
root.configure(bg="#f0f0f0")  # Color de fondo

# Configurar fuentes
custom_font = font.Font(family="Helvetica", size=12)

# Crear un frame para organizar los elementos
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Crear un label y un textfield para ingresar el código
input_label = tk.Label(main_frame, text="Ingrese el código Java:", font=custom_font, bg="#f0f0f0")
input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

input_text = scrolledtext.ScrolledText(main_frame, width=60, height=25, font=custom_font, wrap=tk.WORD)
input_text.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

# Crear un botón para iniciar el análisis
analyze_button = tk.Button(main_frame, text="Analizar", command=analyze_code, font=custom_font, bg="#4CAF50", fg="white")
analyze_button.grid(row=2, column=0, pady=10, sticky="ew")

# Crear un label y un textfield para mostrar los resultados
output_label = tk.Label(main_frame, text="Resultados del análisis:", font=custom_font, bg="#f0f0f0")
output_label.grid(row=0, column=1, sticky="w", pady=(0, 5))

output_text = scrolledtext.ScrolledText(main_frame, width=60, height=25, font=custom_font, wrap=tk.WORD)
output_text.grid(row=1, column=1, sticky="nsew")

# Configurar el sistema de grid para que los elementos se expandan correctamente
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()