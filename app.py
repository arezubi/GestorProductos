from tkinter import ttk
import tkinter as tk
from tkinter import *
from database.repository import ProductoRepository
from database.config import db_config

class VentanaPrincipal():
    def __init__(self, root):
        # Inicializar la base de datos y el repositorio
        db_config.init_db()
        self.repo = ProductoRepository()

        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(0,0)
        self.ventana.configure(background='#f4f6fb')
        self.centrar_ventana(800, 600)
        self.ventana.wm_iconbitmap("icono.ico")

        #Creación del contenedor
        frame = ttk.LabelFrame(
            self.ventana,
            text = "Registrar un nuevo producto",
            padding=(20,10)
        )
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20, padx = 20, sticky="ew")

        #Label y Entry Nombre
        ttk.Label(frame, text="Nombre:", font=('Calibri', 13)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nombre = ttk.Entry(frame, font=('Calibri', 13), width=30)
        self.nombre.focus()
        self.nombre.grid(row=0, column=1, padx=5, pady=5)

        #Label y Entry Precio
        ttk.Label(frame, text="Precio:", font=('Calibri', 13)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.precio = ttk.Entry(frame, font=('Calibri', 13), width=30)
        self.precio.grid(row=1, column=1, padx=5, pady=5)

        # Label y Entry Categoría
        ttk.Label(frame, text="Categoría:", font=('Calibri', 13)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.categoria = ttk.Entry(frame, font=('Calibri', 13), width=30)
        self.categoria.grid(row=2, column=1, padx=5, pady=5)

        # Label y Entry Stock
        ttk.Label(frame, text="Stock:", font=('Calibri', 13)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.stock = ttk.Entry(frame, font=('Calibri', 13), width=30)
        self.stock.grid(row=3, column=1, padx=5, pady=5)

        #Botón Agregar Producto
        s = ttk.Style()
        s.configure('my.TButton', font = ('Calibri', 14, 'bold'))
        self.boton_agregar = ttk.Button(frame, text = "Guardar producto", command=self.add_producto, style='my.TButton')
        self.boton_agregar.grid(row=4, columnspan=2, sticky=W+E)

        #Tabla de productos
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("mystyle.Treeview", font=('Calibri', 11), rowheight=28, background="#eaf0fa",
                        fieldbackground="#eaf0fa")
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'), background="#b3c6e7")
        style.configure('Accent.TButton', font=('Calibri', 14, 'bold'), foreground="#fff", background="#4a90e2")
        style.map('Accent.TButton', background=[('active', '#357ab8')])
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        #Estructura de la tabla
        self.tabla = ttk.Treeview(height = 20, columns=("precio", "categoria", "stock"), style="mystyle.Treeview")
        self.tabla.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.ventana, orient=VERTICAL, command=self.tabla.yview)
        scrollbar.grid(row=2, column=2, sticky="ns", pady=10)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        self.tabla.column("#0", width=150, anchor="w")
        self.tabla.heading("#0", text="Nombre", anchor="center")
        self.tabla.column("precio", width=100, anchor="center")
        self.tabla.heading("precio", text="Precio", anchor="center")
        self.tabla.column("categoria", width=150, anchor="center")
        self.tabla.heading("categoria", text="Categoria", anchor="center")
        self.tabla.column("stock", width=80, anchor="center")
        self.tabla.heading("stock", text="Stock", anchor="center")

        self.get_productos()

        # Botones eliminar y editar
        botones_frame = tk.Frame(self.ventana, bg="#f4f6fb")
        botones_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        self.boton_eliminar = ttk.Button(botones_frame, text="ELIMINAR", command=self.del_producto,
                                         style='Accent.TButton')
        self.boton_eliminar.pack(side="left", expand=True, fill="x", padx=5)
        self.boton_editar = ttk.Button(botones_frame, text="EDITAR", command=self.edit_producto, style='Accent.TButton')
        self.boton_editar.pack(side="left", expand=True, fill="x", padx=5)

        self.ventana.grid_rowconfigure(2, weight=1)
        self.ventana.grid_columnconfigure(0, weight=1)


        # Mensaje informativo para el usuario
        self.mensaje = tk.Label(self.ventana, text=' ', fg='red', bg="#f4f6fb", font=('Calibri', 12, 'bold'))
        self.mensaje.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20)


    def centrar_ventana(self, ancho, alto):
            self.ventana.update_idletasks()
            w = self.ventana.winfo_screenwidth()
            h = self.ventana.winfo_screenheight()
            x = (w // 2) - (ancho // 2)
            y = (h // 2) - (alto // 2)
            self.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


    def get_productos(self):
        # Limpiar la tabla
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Obtener productos del repositorio
        productos = self.repo.obtener_todos_productos(orden_por='nombre', descendente=True)

        # Insertar productos en la tabla
        for producto in productos:
            try:
                precio_float = float(producto.precio)
                precio_formateado = (
                        f"{precio_float:,.2f}"
                        .replace(",", "X")
                        .replace(".", ",")
                        .replace("X", ".") + " €"
                )
            except (ValueError, TypeError):
                precio_formateado = str(producto.precio)

            self.tabla.insert(
                '',
                'end',
                text=producto.nombre,
                values=(precio_formateado, producto.categoria, producto.stock)
            )
    def validacion_nombre(self):
        return len(self.nombre.get().strip()) > 0

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio y no puede quedar vacío'
            return
        if not self.validacion_precio():
            self.mensaje['text'] = 'El precio es obligatorio y tiene que ser un número mayor que 0'
            return

        # Crear producto usando el repositorio
        producto = self.repo.crear_producto(
            nombre=self.nombre.get(),
            precio=self.precio.get(),
            categoria=self.categoria.get(),
            stock=self.stock.get() if self.stock.get() else 0
        )

        if producto:
            print("Datos guardados correctamente")
            self.mensaje['text'] = f'Producto {self.nombre.get()} agregado correctamente'
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)
            self.get_productos()
        else:
            self.mensaje['text'] = 'Error al guardar el producto'

    def del_producto(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']

        # Eliminar usando el repositorio
        if self.repo.eliminar_producto(nombre):
            self.mensaje['text'] = f'Producto {nombre} eliminado correctamente'
            self.get_productos()
        else:
            self.mensaje['text'] = f'Error al eliminar el producto {nombre}'

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            categoria = self.tabla.item(self.tabla.selection())['values'][1]
            stock = self.tabla.item(self.tabla.selection())['values'][2]
            VentanaEditarProducto(self, nombre, precio, categoria, stock, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'

class VentanaEditarProducto():
    def __init__(self, ventana_principal, nombre, precio, categoria, stock, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.configure(background='#f4f6fb')

        # Creación del contenedor Frame de editar producto
        style = ttk.Style()
        style.configure('Custom.TLabelframe.Label', font=('Calibri', 16, 'bold'))
        frame_ep = ttk.LabelFrame(self.ventana_editar,
                                  text="Editar el siguiente Producto",
                                  padding=(20, 10),
                                  style='Custom.TLabelframe')
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        self.ventana_editar.resizable(0, 0)
        self.ventana_editar.transient(ventana_principal.ventana)
        self.ventana_editar.grab_set()

        # Centrar la ventana
        self.ventana_editar.update_idletasks()
        ancho = 450
        alto = 400
        x = (self.ventana_editar.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana_editar.winfo_screenheight() // 2) - (alto // 2)
        self.ventana_editar.geometry(f"{ancho}x{alto}+{x}+{y}")

        # Label y Entry para el nombre antiguo
        ttk.Label(frame_ep, text="Nombre antiguo:", font=('Calibri', 13)).grid(row=1, column=0, pady=5, sticky='w', padx=5)
        entry_nombre_antiguo = ttk.Entry(frame_ep, font=('Calibri', 13))
        entry_nombre_antiguo.insert(0, nombre)
        entry_nombre_antiguo.config(state='readonly')
        entry_nombre_antiguo.grid(row=1, column=1, pady=5, padx=5)

        # Label y Entry para el nuevo nombre
        ttk.Label(frame_ep, text="Nombre nuevo:", font=('Calibri', 13)).grid(row=2, column=0, pady=5, sticky='w', padx=5)
        self.input_nombre_nuevo = ttk.Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1, pady=5, padx=5)
        self.input_nombre_nuevo.focus()

        # Precio antiguo
        ttk.Label(frame_ep, text="Precio antiguo:", font=('Calibri', 13)).grid(row=3, column=0, pady=5, sticky='w', padx=5)
        entry_precio_antiguo = ttk.Entry(frame_ep, font=('Calibri', 13))
        entry_precio_antiguo.insert(0, precio)
        entry_precio_antiguo.config(state='readonly')
        entry_precio_antiguo.grid(row=3, column=1, pady=5, padx=5)

        # Precio nuevo
        ttk.Label(frame_ep, text="Precio nuevo:", font=('Calibri', 13)).grid(row=4, column=0, pady=5, sticky='w', padx=5)
        self.input_precio_nuevo = ttk.Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1, pady=5, padx=5)

        # Categoría antigua
        ttk.Label(frame_ep, text="Categoría antigua:", font=('Calibri', 13)).grid(row=5, column=0, pady=5, sticky='w', padx=5)
        entry_categoria_antigua = ttk.Entry(frame_ep, font=('Calibri', 13))
        entry_categoria_antigua.insert(0, categoria)
        entry_categoria_antigua.config(state='readonly')
        entry_categoria_antigua.grid(row=5, column=1, pady=5, padx=5)

        # Categoría nueva
        ttk.Label(frame_ep, text="Categoría nueva:", font=('Calibri', 13)).grid(row=6, column=0, pady=5, sticky='w', padx=5)
        self.input_categoria_nueva = ttk.Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nueva.grid(row=6, column=1, pady=5, padx=5)

        # Stock antiguo
        ttk.Label(frame_ep, text="Stock antiguo:", font=('Calibri', 13)).grid(row=7, column=0, pady=5, sticky='w', padx=5)
        entry_stock_antiguo = ttk.Entry(frame_ep, font=('Calibri', 13))
        entry_stock_antiguo.insert(0, stock)
        entry_stock_antiguo.config(state='readonly')
        entry_stock_antiguo.grid(row=7, column=1, pady=5, padx=5)

        # Stock nuevo
        ttk.Label(frame_ep, text="Stock nuevo:", font=('Calibri', 13)).grid(row=8, column=0, pady=5, sticky='w', padx=5)
        self.input_stock_nuevo = ttk.Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=8, column=1, pady=5, padx=5)

        # Botón Actualizar producto
        ttk.Button(frame_ep, text="Actualizar Producto", style="my.TButton", command=self.actualizar).grid(row=9, columnspan=2, sticky=W+E, pady=10)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() if self.input_nombre_nuevo.get().strip() else None
        nuevo_precio_str = self.input_precio_nuevo.get()
        nueva_categoria = self.input_categoria_nueva.get() if self.input_categoria_nueva.get().strip() else None
        nuevo_stock_str = self.input_stock_nuevo.get()

        # Extraer solo el número del precio antiguo (quitar el símbolo € y formato)
        precio_a_usar = None
        if nuevo_precio_str.strip():
            try:
                precio_a_usar = float(nuevo_precio_str.replace(',', '.'))
            except ValueError:
                pass

        stock_a_usar = None
        if nuevo_stock_str.strip():
            try:
                stock_a_usar = int(nuevo_stock_str)
            except ValueError:
                pass

        # Actualizar usando el repositorio
        if self.ventana_principal.repo.actualizar_producto(
            nombre_antiguo=self.nombre,
            nombre_nuevo=nuevo_nombre,
            precio_nuevo=precio_a_usar,
            categoria_nueva=nueva_categoria,
            stock_nuevo=stock_a_usar
        ):
            self.mensaje['text'] = f'Producto {self.nombre} ha sido actualizado con éxito'
            self.ventana_editar.destroy()
            self.ventana_principal.get_productos()
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'

if __name__ == '__main__':
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()