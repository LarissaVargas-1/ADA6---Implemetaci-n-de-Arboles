import tkinter as tk
from tkinter import messagebox


class Nodo:

    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class Arbol:

    def __init__(self):
        self.raiz = None

    # --- INSERCIÓN ---
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
            return True
        return self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(valor)
                return True
            return self._insertar_recursivo(nodo_actual.izquierda, valor)
        elif valor > nodo_actual.valor:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(valor)
                return True
            return self._insertar_recursivo(nodo_actual.derecha, valor)
        else:
            return False  # El valor ya existe

    # --- BÚSQUEDA ---
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return False
        if valor == nodo_actual.valor:
            return True
        elif valor < nodo_actual.valor:
            return self._buscar_recursivo(nodo_actual.izquierda, valor)
        else:
            return self._buscar_recursivo(nodo_actual.derecha, valor)

    # --- ELIMINACIÓN ---
    def eliminar(self, valor):
        if not self.buscar(valor):
            return False
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
        return True

    def _eliminar_recursivo(self, nodo_actual, valor):
        if nodo_actual is None:
            return nodo_actual

        if valor < nodo_actual.valor:
            nodo_actual.izquierda = self._eliminar_recursivo(
                nodo_actual.izquierda, valor
            )
        elif valor > nodo_actual.valor:
            nodo_actual.derecha = self._eliminar_recursivo(
                nodo_actual.derecha, valor
            )
        else:
            if nodo_actual.izquierda is None:
                return nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return nodo_actual.izquierda

            sucesor = self._encontrar_minimo(nodo_actual.derecha)
            nodo_actual.valor = sucesor.valor
            nodo_actual.derecha = self._eliminar_recursivo(
                nodo_actual.derecha, sucesor.valor
            )

        return nodo_actual

    def _encontrar_minimo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    # --- RECORRIDOS (INORDEN, PREFIJO, POSFIJO) ---
    def recorrido_inorden(self):
        elementos = []
        self._inorden(self.raiz, elementos)
        return elementos

    def _inorden(self, nodo, elementos):
        if nodo:
            self._inorden(nodo.izquierda, elementos)
            elementos.append(nodo.valor)
            self._inorden(nodo.derecha, elementos)

    def recorrido_prefijo(self):
        elementos = []
        self._prefijo(self.raiz, elementos)
        return elementos

    def _prefijo(self, nodo, elementos):
        if nodo:
            elementos.append(nodo.valor)
            self._prefijo(nodo.izquierda, elementos)
            self._prefijo(nodo.derecha, elementos)

    def recorrido_posfijo(self):
        elementos = []
        self._posfijo(self.raiz, elementos)
        return elementos

    def _posfijo(self, nodo, elementos):
        if nodo:
            self._posfijo(nodo.izquierda, elementos)
            self._posfijo(nodo.derecha, elementos)
            elementos.append(nodo.valor)

    # --- PROPIEDADES DEL ÁRBOL ---
    def obtener_altura(self, nodo="inicio"):
        if nodo == "inicio":
            nodo = self.raiz
        if nodo is None:
            return 0
        return 1 + max(
            self.obtener_altura(nodo.izquierda),
            self.obtener_altura(nodo.derecha),
        )

    def contar_nodos(self, nodo="inicio"):
        if nodo == "inicio":
            nodo = self.raiz
        if nodo is None:
            return 0
        return (
            1
            + self.contar_nodos(nodo.izquierda)
            + self.contar_nodos(nodo.derecha)
        )

    def contar_hojas(self, nodo="inicio"):
        if nodo == "inicio":
            nodo = self.raiz
        if nodo is None:
            return 0
        if nodo.izquierda is None and nodo.derecha is None:
            return 1
        return self.contar_hojas(nodo.izquierda) + self.contar_hojas(
            nodo.derecha
        )

    def valor_minimo(self):
        if self.raiz is None:
            return "N/A"
        return self._encontrar_minimo(self.raiz).valor

    def valor_maximo(self):
        if self.raiz is None:
            return "N/A"
        actual = self.raiz
        while actual.derecha is not None:
            actual = actual.derecha
        return actual.valor

    def es_lleno(self, nodo="inicio"):
        if nodo == "inicio":
            nodo = self.raiz
        if nodo is None:
            return True
        if nodo.izquierda is None and nodo.derecha is None:
            return True
        if nodo.izquierda is not None and nodo.derecha is not None:
            return self.es_lleno(nodo.izquierda) and self.es_lleno(nodo.derecha)
        return False


# ==========================================
# INTERFAZ GRÁFICA INTERACTIVA
# ==========================================
class AplicacionArbol:

    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Visual de Árbol Binario de Búsqueda")
        self.root.geometry("1000x750")
        self.arbol = Arbol()
        self.nodo_resaltado = None

        # Cargar valores iniciales de ejemplo corregidos
        for v in [50, 30, 70, 20, 40, 60, 80]:
            self.arbol.insertar(v)

        self._crear_widgets()
        self.actualizar_vista()

    def _crear_widgets(self):
        # 1. Panel superior de controles
        frame_controles = tk.Frame(self.root, pady=10, bg="#f0f0f0")
        frame_controles.pack(fill=tk.X)

        tk.Label(
            frame_controles,
            text="Valor numérico:",
            bg="#f0f0f0",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=(15, 5))

        self.entrada_valor = tk.Entry(
            frame_controles, width=10, font=("Arial", 11)
        )
        self.entrada_valor.pack(side=tk.LEFT, padx=5)
        self.entrada_valor.bind("<Return>", lambda event: self.accion_insertar())

        tk.Button(
            frame_controles,
            text="Insertar Nodo",
            command=self.accion_insertar,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame_controles,
            text="Eliminar Nodo",
            command=self.accion_eliminar,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame_controles,
            text="Buscar Nodo",
            command=self.accion_buscar,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            frame_controles,
            text="Vaciar Árbol",
            command=self.accion_limpiar,
            bg="#757575",
            fg="white",
            font=("Arial", 10),
        ).pack(side=tk.RIGHT, padx=15)

        # 2. Lienzo central para dibujar el árbol
        self.canvas = tk.Canvas(self.root, bg="white", height=420)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 3. Panel inferior de Propiedades y Recorridos
        frame_info = tk.Frame(
            self.root, pady=10, padx=15, bg="#e8eef5", relief=tk.RIDGE, bd=2
        )
        frame_info.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Columna izquierda: Propiedades
        frame_props = tk.Frame(frame_info, bg="#e8eef5")
        frame_props.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            frame_props,
            text="PROPIEDADES DEL ÁRBOL",
            font=("Arial", 10, "bold"),
            bg="#e8eef5",
            fg="#1C3D6E",
        ).pack(anchor="w")
        self.lbl_propiedades = tk.Label(
            frame_props,
            text="",
            justify=tk.LEFT,
            font=("Consolas", 10),
            bg="#e8eef5",
        )
        self.lbl_propiedades.pack(anchor="w", pady=5)

        # Columna derecha: Recorridos
        frame_rec = tk.Frame(frame_info, bg="#e8eef5")
        frame_rec.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            frame_rec,
            text="RECORRIDOS",
            font=("Arial", 10, "bold"),
            bg="#e8eef5",
            fg="#1C3D6E",
        ).pack(anchor="w")
        self.lbl_recorridos = tk.Label(
            frame_rec,
            text="",
            justify=tk.LEFT,
            font=("Consolas", 10),
            bg="#e8eef5",
        )
        self.lbl_recorridos.pack(anchor="w", pady=5)

    def _leer_numero(self):
        texto = self.entrada_valor.get().strip()
        try:
            valor = int(texto)
            self.entrada_valor.delete(0, tk.END)
            return valor
        except ValueError:
            messagebox.showwarning(
                "Entrada inválida", "Por favor ingresa un número entero válido."
            )
            return None

    def accion_insertar(self):
        valor = self._leer_numero()
        if valor is not None:
            self.nodo_resaltado = None
            if self.arbol.insertar(valor):
                messagebox.showinfo(
                    "Éxito", f"El valor {valor} fue insertado correctamente."
                )
            else:
                messagebox.showinfo(
                    "Información", f"El valor {valor} ya existe en el árbol."
                )
            self.actualizar_vista()

    def accion_eliminar(self):
        valor = self._leer_numero()
        if valor is not None:
            self.nodo_resaltado = None
            if self.arbol.eliminar(valor):
                messagebox.showinfo(
                    "Éxito", f"El valor {valor} fue eliminado correctamente."
                )
            else:
                messagebox.showinfo(
                    "Información",
                    f"El valor {valor} no se encontró en el árbol.",
                )
            self.actualizar_vista()

    def accion_buscar(self):
        valor = self._leer_numero()
        if valor is not None:
            if self.arbol.buscar(valor):
                self.nodo_resaltado = valor
                messagebox.showinfo(
                    "Encontrado", f"¡El valor {valor} sí está en el árbol!"
                )
            else:
                self.nodo_resaltado = None
                messagebox.showinfo(
                    "No encontrado",
                    f"El valor {valor} no existe en el árbol.",
                )
            self.actualizar_vista()

    def accion_limpiar(self):
        if messagebox.askyesno(
            "Confirmar", "¿Estás seguro de vaciar todo el árbol?"
        ):
            self.arbol = Arbol()
            self.nodo_resaltado = None
            self.actualizar_vista()

    def actualizar_vista(self):
        self.canvas.delete("all")

        # Dibujar árbol si no está vacío
        if self.arbol.raiz:
            canvas_width = self.canvas.winfo_width()
            if canvas_width < 100:
                canvas_width = 1000
            self._dibujar_arbol(
                self.arbol.raiz,
                canvas_width // 2,
                40,
                canvas_width // 4,
            )

        # Actualizar etiquetas de propiedades
        altura = self.arbol.obtener_altura()
        nodos = self.arbol.contar_nodos()
        hojas = self.arbol.contar_hojas()
        minimo = self.arbol.valor_minimo()
        maximo = self.arbol.valor_maximo()
        lleno = "Sí" if self.arbol.es_lleno() else "No"

        texto_props = (
            f"• Nodos totales : {nodos}\n"
            f"• Altura        : {altura}\n"
            f"• Hojas         : {hojas}\n"
            f"• Mínimo / Máx  : {minimo} / {maximo}\n"
            f"• ¿Es lleno?    : {lleno}"
        )
        self.lbl_propiedades.config(text=texto_props)

        # Actualizar recorridos
        inorden = self.arbol.recorrido_inorden()
        prefijo = self.arbol.recorrido_prefijo()
        posfijo = self.arbol.recorrido_posfijo()

        texto_rec = (
            f"• Inorden (I-R-D) : {inorden}\n"
            f"• Prefijo (R-I-D) : {prefijo}\n"
            f"• Posfijo (I-D-R) : {posfijo}"
        )
        self.lbl_recorridos.config(text=texto_rec)

    def _dibujar_arbol(self, nodo, x, y, dx):
        radio = 20
        # Dibujar conexiones a los hijos primero (para que queden detrás de los nodos)
        if nodo.izquierda:
            x_izq = x - dx
            y_izq = y + 60
            self.canvas.create_line(x, y, x_izq, y_izq, width=2, fill="#555555")
            self._dibujar_arbol(nodo.izquierda, x_izq, y_izq, dx // 2)

        if nodo.derecha:
            x_der = x + dx
            y_der = y + 60
            self.canvas.create_line(x, y, x_der, y_der, width=2, fill="#555555")
            self._dibujar_arbol(nodo.derecha, x_der, y_der, dx // 2)

        # Color del nodo (resaltado en amarillo si coincide con una búsqueda)
        if self.nodo_resaltado == nodo.valor:
            color_fondo = "#FFEB3B"
            color_borde = "#F57C00"
        else:
            color_fondo = "#4CAF50"
            color_borde = "#2E7D32"

        # Dibujar el círculo del nodo
        self.canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            fill=color_fondo,
            outline=color_borde,
            width=2,
        )
        # Dibujar el valor dentro del nodo
        self.canvas.create_text(
            x,
            y,
            text=str(nodo.valor),
            font=("Arial", 10, "bold"),
            fill="black" if self.nodo_resaltado == nodo.valor else "white",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionArbol(root)
    root.mainloop()