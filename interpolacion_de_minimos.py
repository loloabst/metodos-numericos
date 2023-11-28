import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, simplify

def main():
    # Declarar funcion_interpolante como variable global
    funcion_interpolante = None

    def minimos_cuadrados(valores_x, valores_y):
        n = len(valores_x)

        # Cálculos para minimos cuadrados
        suma_x = sum(valores_x)
        suma_y = sum(valores_y)
        suma_x_squared = sum(x**2 for x in valores_x)
        suma_xy = sum(x*y for x, y in zip(valores_x, valores_y))

        # Coeficientes de la recta de regresión (pendiente y ordenada al origen)
        m = (n * suma_xy - suma_x * suma_y) / (n * suma_x_squared - suma_x**2)
        b = (suma_y * suma_x_squared - suma_x * suma_xy) / (n * suma_x_squared - suma_x**2)

        # Coeficiente de correlación lineal
        r = (n * suma_xy - suma_x * suma_y) / np.sqrt((n * suma_x_squared - suma_x**2) * (n * sum(y**2 for y in valores_y) - suma_y**2))

        # Coeficiente de determinación
        r_squared = r**2

        x = symbols('x')
        funcion_interpolante = m * x + b
        return funcion_interpolante, m, b, r, r_squared

    def graficar_interpolacion():
        nonlocal funcion_interpolante
        valores_x = [float(x) for x in entrada_x.get().split(',')]
        valores_y = [float(y) for y in entrada_y.get().split(',')]

        # Mínimos Cuadrados
        funcion_interpolante, pendiente, ordenada_al_origen, coef_corr_lineal, coef_det = minimos_cuadrados(valores_x, valores_y)
        funcion_interpolante = simplify(funcion_interpolante)

        rango_x = np.linspace(min(valores_x), max(valores_x), 100)
        rango_y_minimos_cuadrados = [float(funcion_interpolante.subs('x', x)) for x in rango_x]

        fig, ax = plt.subplots()
        ax.scatter(valores_x, valores_y, label='Puntos Originales', color='red')
        ax.plot(rango_x, rango_y_minimos_cuadrados, label=f'Mínimos Cuadrados: y = {pendiente:.2f}x + {ordenada_al_origen:.2f}', color='green')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Mínimos Cuadrados')
        ax.legend()
        ax.grid(True)

        lienzo = FigureCanvasTkAgg(fig, master=ventanaMinimos)
        widget_lienzo = lienzo.get_tk_widget()
        widget_lienzo.grid(row=5, column=0, columnspan=2)

        # Mostrar resultados
        resultado_texto.set(f'Pendiente: {pendiente:.4f}\nOrdenada al Origen: {ordenada_al_origen:.4f}\nCoef. Correlación Lineal: {coef_corr_lineal:.4f}\nCoef. Determinación: {coef_det:.4f}')

    def obtener_valor_y():
        nonlocal funcion_interpolante
        try:
            x_valor = float(entrada_x_valor.get())
            y_valor = float(funcion_interpolante.subs('x', x_valor))
            messagebox.showinfo("Resultado", f'f({x_valor}) = {y_valor:.2f}')
        except ValueError:
            messagebox.showerror("Error", "Ingresa un valor válido para x")

    ventanaMinimos = tk.Tk()
    ventanaMinimos.title("Mínimos Cuadrados")

    etiqueta_x = ttk.Label(ventanaMinimos, text="Valores de x (separados por comas):")
    etiqueta_x.grid(row=0, column=0, padx=10, pady=5)
    entrada_x = ttk.Entry(ventanaMinimos)
    entrada_x.grid(row=0, column=1, padx=10, pady=5)

    etiqueta_y = ttk.Label(ventanaMinimos, text="Valores de y (separados por comas):")
    etiqueta_y.grid(row=1, column=0, padx=10, pady=5)
    entrada_y = ttk.Entry(ventanaMinimos)
    entrada_y.grid(row=1, column=1, padx=10, pady=5)

    resultado_texto = tk.StringVar()
    etiqueta_resultado = ttk.Label(ventanaMinimos, textvariable=resultado_texto)
    etiqueta_resultado.grid(row=3, columnspan=2, pady=10)

    boton_interpolacion = ttk.Button(ventanaMinimos, text="Interpolar", command=graficar_interpolacion)
    boton_interpolacion.grid(row=4, columnspan=2, pady=10)

    # Entry para ingresar el valor de x
    etiqueta_x_valor = ttk.Label(ventanaMinimos, text="Valor de x:")
    etiqueta_x_valor.grid(row=6, column=0, padx=10, pady=5)
    entrada_x_valor = ttk.Entry(ventanaMinimos)
    entrada_x_valor.grid(row=6, column=1, padx=10, pady=5)

    # Botón para obtener el valor correspondiente de y
    boton_obtener_y = ttk.Button(ventanaMinimos, text="Obtener Valor de y", command=obtener_valor_y)
    boton_obtener_y.grid(row=7, columnspan=2, pady=10)

    resultado_valor_y = tk.StringVar()
    etiqueta_resultado_y = ttk.Label(ventanaMinimos, textvariable=resultado_valor_y)
    etiqueta_resultado_y.grid(row=8, columnspan=2, pady=10)

    ventanaMinimos.mainloop()

if __name__ == "__main__":
    main()
