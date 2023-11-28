import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def main():
    class InterpolacionCuadraticaApp:
        def __init__(self):
            self.ventana = tk.Tk()
            self.ventana.title("Interpolación Cuadrática")

            tk.Label(
                self.ventana,
                text="Ingrese los valores de x separados por comas (por ejemplo, '1,3,5'):",
            ).pack()
            self.entry_x_valores = tk.Entry(self.ventana)
            self.entry_x_valores.pack()

            tk.Label(
                self.ventana,
                text="Ingrese los valores de y separados por comas (por ejemplo, '2,4,1'):",
            ).pack()
            self.entry_y_valores = tk.Entry(self.ventana)
            self.entry_y_valores.pack()

            tk.Label(self.ventana, text="Ingrese el valor de x a interpolar:").pack()
            self.entry_x_interpolado = tk.Entry(self.ventana)
            self.entry_x_interpolado.pack()

            tk.Button(
                self.ventana,
                text="Calcular Interpolación",
                command=self.calcular_interpolacion,
            ).pack()

            # Etiqueta para mostrar la fórmula de interpolación
            self.label_formula = tk.Label(self.ventana, text="")
            self.label_formula.pack()

            # Crear un contenedor para la gráfica
            self.figura, self.ax = plt.subplots()
            self.canvas = FigureCanvasTkAgg(self.figura, master=self.ventana)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        def interpolacion_cuadratica(self, x_vals, y_vals, x_interpolado):
            n = len(x_vals)
            if n < 3:
                messagebox.showerror(
                    "Error",
                    "Se necesitan al menos 3 puntos para la interpolación cuadrática.",
                )
                return None, None

            # Construir el sistema de ecuaciones para encontrar los coeficientes a, b, c
            A = [[x**2, x, 1] for x in x_vals]
            B = [[y] for y in y_vals]

            # Resolver el sistema de ecuaciones utilizando la eliminación gaussiana
            coeficientes = self.gaussian_elimination(A, B)

            if coeficientes is None:
                messagebox.showerror(
                    "Error", "No se puede realizar la interpolación cuadrática."
                )
                return None, None

            a, b, c = coeficientes

            # Evaluar el polinomio cuadrático en el punto x_interpolado
            y_interpolado = a * x_interpolado**2 + b * x_interpolado + c

            # Crear la fórmula de interpolación cuadrática
            formula = f"{a:.2f} * x^2 + {b:.2f} * x + {c:.2f}"

            return y_interpolado, formula

        def gaussian_elimination(self, A, B):
            n = len(A)

            for i in range(n):
                max_row = i
                for j in range(i + 1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j

                A[i], A[max_row] = A[max_row], A[i]
                B[i], B[max_row] = B[max_row], B[i]

                pivot = A[i][i]
                if pivot == 0:
                    return None

                for j in range(i + 1, n):
                    ratio = A[j][i] / pivot
                    for k in range(i, n):
                        A[j][k] -= ratio * A[i][k]
                    B[j][0] -= ratio * B[i][0]

            # Sustitución hacia atrás
            x = [0] * n
            for i in range(n - 1, -1, -1):
                x[i] = B[i][0]
                for j in range(i + 1, n):
                    x[i] -= A[i][j] * x[j]
                x[i] /= A[i][i]

            return x

        def plot_interpolation(self, x_vals, y_vals, x_interpolado, y_interpolado):
            self.ax.clear()
            self.ax.scatter(x_vals, y_vals, label='Puntos Originales', color='red')
            
            # Crear un rango de puntos para la representación gráfica
            x_range = np.linspace(min(x_vals), max(x_vals), 100)
            y_range = [self.interpolacion_cuadratica(x_vals, y_vals, x)[0] for x in x_range]
            
            # Agregar el punto interpolado a la gráfica
            self.ax.scatter(x_interpolado, y_interpolado, label='Punto Interpolado', color='blue')
            
            # Graficar la interpolación cuadrática
            self.ax.plot(x_range, y_range, label='Interpolación Cuadrática', color='green')

            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('Interpolación Cuadrática')
            self.ax.legend()
            self.canvas.draw()

        def calcular_interpolacion(self):
            try:
                x_vals = [float(x) for x in self.entry_x_valores.get().split(",")]
                y_vals = [float(y) for y in self.entry_y_valores.get().split(",")]
                x_interpolado = float(self.entry_x_interpolado.get())

                resultado, formula = self.interpolacion_cuadratica(
                    x_vals, y_vals, x_interpolado
                )

                if resultado is not None:
                    messagebox.showinfo(
                        "Resultado",
                        f"El valor interpolado en x={x_interpolado} es y={resultado}",
                    )

                    if formula is not None:
                        self.label_formula.config(
                            text=f"Fórmula de Interpolación Cuadrática: {formula}"
                        )

                        # Agregar la gráfica de interpolación cuadrática
                        self.plot_interpolation(x_vals, y_vals, x_interpolado, resultado)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Ingrese valores válidos para los puntos y la x a interpolar.",
                )

    # Crear una instancia de la aplicación y ejecutar la interfaz gráfica
    app = InterpolacionCuadraticaApp()
    app.ventana.mainloop()


if __name__ == "__main__":
    main()
