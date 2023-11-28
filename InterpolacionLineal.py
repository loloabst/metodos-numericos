import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def main():
    class InterpolacionLinealGUI:
        def __init__(self, master):
            self.master = master
            self.master.title("Interpolación Lineal")

            self.label_x = tk.Label(master, text="Valores de x (separados por comas):")
            self.entry_x = tk.Entry(master)
            self.label_y = tk.Label(master, text="Valores de y (separados por comas):")
            self.entry_y = tk.Entry(master)
            self.label_interpolado = tk.Label(
                master, text="Valor de x para interpolar/extrapolar:"
            )
            self.entry_interpolado = tk.Entry(master)
            self.button_calcular = tk.Button(
                master, text="Calcular", command=self.calcular_interpolacion
            )

            self.label_x.pack()
            self.entry_x.pack()
            self.label_y.pack()
            self.entry_y.pack()
            self.label_interpolado.pack()
            self.entry_interpolado.pack()
            self.button_calcular.pack()

            # Crear un contenedor para la gráfica
            self.figura, self.ax = plt.subplots()
            self.canvas = FigureCanvasTkAgg(self.figura, master=self.master)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        def calcular_interpolacion(self):
            try:
                x_vals = [float(x) for x in self.entry_x.get().split(",")]
                y_vals = [float(y) for y in self.entry_y.get().split(",")]

                # Validar que las listas tengan la misma longitud
                if len(x_vals) != len(y_vals):
                    messagebox.showerror("Error", "Las listas deben tener la misma longitud")
                    return

                x_interpolado = float(self.entry_interpolado.get())

                y_interpolado = self.interpolacion_lineal(x_vals, y_vals, x_interpolado)

                messagebox.showinfo(
                    "Resultado",
                    f"Para x={x_interpolado}, la interpolación/extrapolación da y={y_interpolado}",
                )

                # Agregar la gráfica de interpolación lineal
                self.plot_interpolation(x_vals, y_vals, x_interpolado, y_interpolado)

            except ValueError as e:
                messagebox.showerror("Error", f"Error: {e}")

        def interpolacion_lineal(self, x_vals, y_vals, x):
            for i in range(len(x_vals) - 1):
                if x_vals[i] <= x <= x_vals[i + 1]:
                    x0, y0 = x_vals[i], y_vals[i]
                    x1, y1 = x_vals[i + 1], y_vals[i + 1]
                    y = y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
                    return y

            # Extrapolación cuando x está fuera del rango conocido
            if x < x_vals[0]:
                x0, y0 = x_vals[0], y_vals[0]
                x1, y1 = x_vals[1], y_vals[1]
            else:
                x0, y0 = x_vals[-2], y_vals[-2]
                x1, y1 = x_vals[-1], y_vals[-1]

            y = y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
            return y

        def plot_interpolation(self, x_vals, y_vals, x_interpolado, y_interpolado):
            self.ax.clear()
            self.ax.scatter(x_vals, y_vals, label='Puntos Originales', color='red')
            
            # Agregar el punto interpolado a la gráfica
            self.ax.scatter(x_interpolado, y_interpolado, label='Punto Interpolado', color='blue')

            # Graficar la interpolación lineal
            self.ax.plot([min(x_vals), max(x_vals)], [self.interpolacion_lineal(x_vals, y_vals, min(x_vals)), self.interpolacion_lineal(x_vals, y_vals, max(x_vals))], label='Interpolación Lineal', color='green')

            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('Interpolación Lineal')
            self.ax.legend()
            self.canvas.draw()

    # Inicializar la aplicación
    root = tk.Tk()
    app = InterpolacionLinealGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()