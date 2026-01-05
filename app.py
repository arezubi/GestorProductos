from tkinter import ttk
import tkinter as tk
from tkinter import *
import sqlite3

class VentanaPrincipal():
    db = 'database/productos.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(0,0)
        self.ventana.configure(background='#f4f6fb')
        self.centrar_ventana(600, 600)
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

        #Botón Agregar Producto
        s = ttk.Style()
        s.configure('my.TButton', font = ('Calibri', 14, 'bold'))
        self.boton_agregar = ttk.Button(frame, text = "Guardar producto", command=self.add_producto, style='my.TButton')
        self.boton_agregar.grid(row=3, columnspan=2, sticky=W+E)

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
        self.tabla = ttk.Treeview(height = 20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.tabla.heading("#0", text="Nombre", anchor="center")
        self.tabla.heading("#1", text="Precio", anchor="center")
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

    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)

        for fila in registros_db:
            try:
                precio_float = float(fila[2])
                precio_formateado = f"{precio_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"
            except (ValueError, TypeError):
                precio_formateado = fila[2]

            self.tabla.insert('', 0, text = fila[1], values = (precio_formateado,))

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

        query = 'INSERT INTO producto VALUES (NULL, ?, ?)'
        parametros = (self.nombre.get(), self.precio.get())
        self.db_consulta(query, parametros)
        print("Datos guardados correctamente")
        self.mensaje['text'] = f'Producto {self.nombre.get()} agregado correctamente'
        self.nombre.delete(0, END)
        self.precio.delete(0, END)

        self.get_productos()

    def del_producto(self):
        #DEBUG
        #print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())['text'])
        #print(self.tabla.item(self.tabla.selection())['values'])
        #print(self.tabla.item(self.tabla.selection())['values'][0])

        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?'
        self.db_consulta(query, (nombre,))
        self.mensaje['text'] = f'Producto {nombre} eliminado correctamente'
        self.get_productos() #Actializa tabla productos

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'

class VentanaEditarProducto():
    def __init__(self, ventana_principal, nombre, precio, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        #Creación del contenedor Frame de editar producto
        frame_ep = LabelFrame(self.ventana_editar, text = "Editar el siguiente Producto", font= ('Calibri', 16, 'bold'))
        frame_ep.grid(row = 0, column = 0, columnspan = 2, pady = 20, padx = 20)

        #Label y Entry para el nombre antiguo
        Label(frame_ep, text = "Nombre antiguo: ", font = ('Calibri', 13)).grid(row = 1, column = 0)
        Entry(frame_ep, textvariable = StringVar(self.ventana_editar, value = nombre), state = 'readonly', font = ('Calibri', 13)).grid(row = 1, column = 1)

        #Label y Entry para el nuevo nombre
        Label(frame_ep, text = "Nombre nuevo: ", font = ('Calibri', 13)).grid(row = 2, column = 0)
        self.input_nombre_nuevo = Entry (frame_ep, font = ('Calibri', 13))
        self.input_nombre_nuevo.grid(row = 2, column = 1)
        self.input_nombre_nuevo.focus()

        #Precio antiguo
        Label(frame_ep, text = "Precio antiguo: ", font = ('Calibri', 13)).grid(row = 3, column = 0)
        Entry(frame_ep, textvariable = StringVar(self.ventana_editar, value = precio), state = 'readonly', font = ('Calibri', 13)).grid(row = 3, column = 1)

        #Precio nuevo
        Label(frame_ep, text = "Precio nuevo: ", font = ('Calibri', 13)).grid(row = 4, column = 0)
        self.input_precio_nuevo = Entry (frame_ep, font = ('Calibri', 13))
        self.input_precio_nuevo.grid(row = 4, column = 1)

        #Botón Actualizar producto
        ttk.Style().configure("my.TButton", font = ('Calibri', 14, 'bold'))
        ttk.Button(frame_ep, text = "Actualizar Producto", style="my.TButton", command=self.actualizar).grid(row = 5, columnspan = 2, sticky = W + E)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio

        if nuevo_nombre and nuevo_precio:
            query = 'UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = f'Producto {self.nombre} ha sido actualizado con éxito'
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'
        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()




if __name__ == '__main__':
    root = Tk()
    app = VentanaPrincipal(root)
    root.mainloop()