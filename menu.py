import tkinter as tk
from interpolacion_de_Lagrange import main as lagrange_main
from interpolacion_de_minimos import main as minimos_main
from InterpolacionCuadratica import main as cuad_main
from InterpolacionLineal import main as lineal_main


ventana = tk.Tk()
ventana.title("Programa de Métodos de Interpolación")
ventana.geometry("600x400")  # Tamaño de la ventana

    # Etiqueta en la parte superior de la ventana
lbl_titulo = tk.Label(ventana, text="Programa de Métodos de Interpolación", font=("Arial", 16))
lbl_titulo.pack(pady=10)

def ejecutar_interpolacion_lagrange():
    lagrange_main()

def ejecutar_interpolacion_minimos_cuadrados():
    minimos_main()

def ejecutar_interpolacionCuadratica():
    cuad_main()

def ejecutar_interpolacion_Lineal():
    lineal_main()


    # Crear botones en lugar de opciones en el menú
btn_lagrange = tk.Button(ventana, text="Interpolación de Lagrange", command=ejecutar_interpolacion_lagrange)
btn_lagrange.pack(pady=5)

btn_lineal = tk.Button(ventana, text="Interpolación Lineal", command=ejecutar_interpolacion_Lineal)
btn_lineal.pack(pady=5)

btn_cuadratica = tk.Button(ventana, text="Interpolación Cuadrática", command=ejecutar_interpolacionCuadratica)
btn_cuadratica.pack(pady=5)

btn_cuadrados = tk.Button(ventana, text="Mínimos Cuadrados", command=ejecutar_interpolacion_minimos_cuadrados)
btn_cuadrados.pack(pady=5)

ventana.mainloop()

