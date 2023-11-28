import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, simplify

def main():
    def lagrange(valores_x, valores_y):
        n = len(valores_x)
        x = symbols('x')

        def funcion_interpolada(x):
            resultado = 0.0

            for i in range(n):
                termino = valores_y[i]
                for j in range(n):
                    if i != j:
                        termino *= (x - valores_x[j]) / (valores_x[i] - valores_x[j])
                resultado += termino

            return resultado

        expr = funcion_interpolada(x)
        return expr

    def graficar_interpolacion():
        valores_x = [float(x) for x in entrada_x.get().split(',')]
        valores_y = [float(y) for y in entrada_y.get().split(',')]
        funcion_interpolante = lagrange(valores_x, valores_y)
        funcion_interpolante = simplify(funcion_interpolante)

        rango_x = np.linspace(min(valores_x), max(valores_x), 100)
        rango_y = [float(funcion_interpolante.subs('x', x)) for x in rango_x]

        fig, ax = plt.subplots()
        ax.scatter(valores_x, valores_y, label='Puntos Originales', color='red')
        ax.plot(rango_x, rango_y, label=f'Función Interpolante: f(x)={funcion_interpolante}', color='blue')
        print(funcion_interpolante)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Interpolación de Lagrange')
        ax.legend()
        ax.grid(True)

        lienzo = FigureCanvasTkAgg(fig, master=ventanaLagrange)
        widget_lienzo = lienzo.get_tk_widget()
        widget_lienzo.grid(row=5, column=0, columnspan=2)

        # Obtener el valor de x para interpolar
        x_interpolado = float(entrada_x_interpolado.get())

        # Calcular y
        y_interpolado = float(funcion_interpolante.subs('x', x_interpolado))

        # Mostrar resultado en un messagebox
        messagebox.showinfo("Resultado de Interpolación", f'f({x_interpolado}) = {y_interpolado:.2f}')

    ventanaLagrange = tk.Tk()
    ventanaLagrange.title("1.- Interpolación de Lagrange")

    etiqueta_x = ttk.Label(ventanaLagrange, text="Valores de x (separados por comas):")
    etiqueta_x.grid(row=0, column=0, padx=10, pady=5)
    entrada_x = ttk.Entry(ventanaLagrange)
    entrada_x.grid(row=0, column=1, padx=10, pady=5)

    etiqueta_y = ttk.Label(ventanaLagrange, text="Valores de y (separados por comas):")
    etiqueta_y.grid(row=1, column=0, padx=10, pady=5)
    entrada_y = ttk.Entry(ventanaLagrange)
    entrada_y.grid(row=1, column=1, padx=10, pady=5)

    etiqueta_x_interpolado = ttk.Label(ventanaLagrange, text="Valor de x a interpolar:")
    etiqueta_x_interpolado.grid(row=2, column=0, padx=10, pady=5)
    entrada_x_interpolado = ttk.Entry(ventanaLagrange)
    entrada_x_interpolado.grid(row=2, column=1, padx=10, pady=5)

    boton_interpolacion = ttk.Button(ventanaLagrange, text="Interpolar", command=graficar_interpolacion)
    boton_interpolacion.grid(row=3, columnspan=2, pady=10)

    ventanaLagrange.mainloop()

if __name__ == "__main__":
    main()
