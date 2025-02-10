import tkinter as tk
from tkinter import scrolledtext, font, filedialog
from analizador import lexer  

def analyze_code():
    output_text.config(state='normal')
    code = input_text.get("1.0", tk.END)  # Obtener el código del textfield
    try:
        tokens = lexer(code)  
        output_text.delete("1.0", tk.END)  
        for token_type, value in tokens:
            output_text.insert(tk.END, f"{token_type}: {value}\n")  
        output_text.config(state='disabled')
    except SyntaxError as e:
        output_text.delete("1.0", tk.END)

        output_text.insert(tk.END, f"Error: {e}")


def load_file():
    # Abrir un diálogo para seleccionar un archivo
    file_path = filedialog.askopenfilename(filetypes=[("Java files", "*.java")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()  
            input_text.delete("1.0", tk.END)  
            input_text.insert(tk.END, code) 

#ventana principal
root = tk.Tk()
root.title("Super Analizador Léxico")
root.geometry("900x500") 
root.configure(bg="#f0f0f0")  

# Fuente
custom_font = font.Font(family="Helvetica", size=10)

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_label = tk.Label(main_frame, text="Código Java:", font=custom_font, bg="#f0f0f0")
input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

input_text = scrolledtext.ScrolledText(main_frame, width=50, height=15, font=custom_font, wrap=tk.WORD)
input_text.grid(row=1, column=0, padx=(0, 10), sticky="nsew")

load_button = tk.Button(
    main_frame,
    text="Cargar Archivo",
    command=load_file,
    font=("Arial", 12, "bold"),  
    bg="#2196F3",  
    fg="white",   
    activebackground="#1976D2",  
)
load_button.grid(row=2, column=0, pady=5, sticky="ew")


analyze_button = tk.Button(
    main_frame,
    text="Analizar",
    command=analyze_code,
    font=("Arial", 12, "bold"),  
    bg="#4CAF50", 
    fg="white",
    activebackground="#3e8e41"   
)

analyze_button.grid(row=3, column=0, pady=10, sticky="ew")

output_label = tk.Label(main_frame, text="Resultados del análisis:", font=custom_font, bg="#f0f0f0")
output_label.grid(row=0, column=1, sticky="w", pady=(0, 5))

output_text = scrolledtext.ScrolledText(main_frame, width=50, height=15, font=custom_font, wrap=tk.WORD)
output_text.grid(row=1, column=1, sticky="nsew")

main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()