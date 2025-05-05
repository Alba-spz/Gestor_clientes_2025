from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from tkinter.messagebox import showerror
import database as db
import helpers

# Define una clase para centrar widgets en la pantalla
class CenterWidgetMixin:
    def center(self):
        # Actualiza las dimensiones del widget
        self.update()
        # Obtén el ancho y alto del widget
        w = self.winfo_width()
        h = self.winfo_height()
        # Obtén el ancho y alto de la pantalla
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        # Calcula las coordenadas para centrar el widget
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        # Establece la geometría del widget
        self.geometry(f"{w}x{h}+{x}+{y}")

# Define la ventana principal de la aplicación
class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        # Establece el título de la ventana
        self.title('Gestor de clientes')
        # Construye la interfaz
        self.build()
        # Centra la ventana
        self.center()
    
    def create_client_window(self):
        # Abre la ventana para crear un cliente
        self.CreateClientWindow(self)

    def delete(self):
        # Obtén el cliente seleccionado en el Treeview
        cliente = self.treeview.focus()
        if cliente:
            # Obtén los valores del cliente seleccionado
            campos = self.treeview.item(cliente, 'values')
            # Muestra un cuadro de confirmación
            confirmar = askokcancel(
                title='Confirmación',
                message=f'¿Borrar a {campos[1]} {campos[2]}?',
                icon=WARNING)
            if confirmar:
                # Borra el cliente del Treeview y la base de datos
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def build(self):
        # Crea el frame superior
        top_frame = Frame(self)
        top_frame.pack()

        # Crea la barra de desplazamiento
        scrollbar = Scrollbar(top_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Crea el Treeview para mostrar los clientes
        treeview = ttk.Treeview(top_frame, yscrollcommand=scrollbar.set)
        treeview['columns'] = ('DNI', 'NOMBRE', 'APELLIDO')

        # Configura las columnas del Treeview
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("NOMBRE", anchor=CENTER)
        treeview.column("APELLIDO", anchor=CENTER)

        # Configura los encabezados del Treeview
        treeview.heading("#0", anchor=CENTER)
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("NOMBRE", text="NOMBRE", anchor=CENTER)
        treeview.heading("APELLIDO", text="APELLIDO", anchor=CENTER)

        # Carga los datos de la base de datos en el Treeview
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

        # Empaqueta el Treeview y configura la barra de desplazamiento
        treeview.pack()
        scrollbar.config(command=treeview.yview)

        # Crea el frame inferior para los botones
        bottom_frame = Frame(self)
        bottom_frame.pack(pady=20)

        # Crea los botones de acción
        Button(bottom_frame, text="Crear", command=self.create_client_window).grid(row=1, column=0)
        Button(bottom_frame, text="Modificar", command=self.edit_client_window).grid(row=1, column=1)
        Button(bottom_frame, text="Borrar", command=self.delete).grid(row=1, column=2)

        # Exporta el Treeview como un atributo de clase
        self.treeview = treeview
    
    def create_client_window(self):
        # Abre la ventana para crear un cliente
        CreateClientWindow(self)
    
    def edit_client_window(self):
        # Abre la ventana para editar un cliente
        EditClientWindow(self)

# Define la ventana para crear un cliente
class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        # Establece el título de la ventana
        self.title('Crear cliente')
        # Construye la interfaz
        self.build()
        # Centra la ventana
        self.center()
        # Obliga al usuario a interactuar con esta ventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Inicializa la lista de validaciones
        self.validaciones = [0, 0, 0]

        # Crea el frame superior
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Crea las etiquetas para los campos
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)

        # Crea las entradas de texto con eventos de validación
        self.dni = Entry(frame)
        self.nombre = Entry(frame)
        self.apellido = Entry(frame)

        self.dni.grid(row=1, column=0)
        self.nombre.grid(row=1, column=1)
        self.apellido.grid(row=1, column=2)

        self.dni.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))
        self.nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))
        self.apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 2))

        # Crea el frame inferior para los botones
        bottom = Frame(self)
        bottom.pack(pady=10)

        # Crea el botón para crear un cliente
        self.crear_button = Button(bottom, text="Crear", command=self.create_client)
        self.crear_button.configure(state=DISABLED)
        self.crear_button.grid(row=0, column=0)

        # Crea el botón para cancelar
        Button(bottom, text="Cancelar", command=self.close).grid(row=0, column=1)
        
    def validate(self, event, index):
        # Valida el contenido de los campos
        valor = event.widget.get()
        valido = (
            helpers.dni_valido(valor, db.Clientes.lista)
            if index == 0
            else valor.isalpha() and 2 <= len(valor) <= 30
        )
        # Cambia el color de fondo según la validación
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Actualiza la lista de validaciones
        self.validaciones[index] = 1 if valido else 0
        # Habilita o deshabilita el botón de crear
        self.crear_button.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

    def create_client(self):
        # Inserta el nuevo cliente en el Treeview
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        # Crea el cliente en la base de datos
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        # Cierra la ventana
        self.close()

    def close(self):
        # Cierra la ventana
        self.destroy()
        self.update()

# Define la ventana para editar un cliente
class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        # Establece el título de la ventana
        self.title('Actualizar cliente')
        self.master = parent
        # Construye la interfaz
        self.build()
        # Centra la ventana
        self.center()
        # Obliga al usuario a interactuar con esta ventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        # Crea el frame superior
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Crea las etiquetas para los campos
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)

        # Crea las entradas de texto
        dni = Entry(frame)
        dni.grid(row=1, column=0)

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))

        # Carga los datos del cliente seleccionado
        cliente = self.master.treeview.focus()
        if not cliente:
            # Muestra un error si no hay cliente seleccionado
            showerror("Error", "No hay ningún cliente seleccionado.")
            self.destroy()
            return

        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        # Crea el frame inferior para los botones
        frame = Frame(self)
        frame.pack(pady=10)

        # Crea el botón para actualizar el cliente
        actualizar = Button(frame, text="Actualizar", command=self.update_client)
        actualizar.grid(row=0, column=0)
        # Crea el botón para cancelar
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        # Inicializa las validaciones
        self.validaciones = [1, 1]

        # Exporta los elementos como atributos de clase
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def validate(self, event, index):
        # Valida el contenido de los campos
        valor = event.widget.get()
        valido = valor.isalpha() and 2 <= len(valor) <= 30
        # Cambia el color de fondo según la validación
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Actualiza la lista de validaciones
        self.validaciones[index] = 1 if valido else 0
        # Habilita o deshabilita el botón de actualizar
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)

    def update_client(self):
        # Obtén el cliente seleccionado
        cliente = self.master.treeview.focus()
        # Actualiza los valores en el Treeview
        self.master.treeview.item(
            cliente,
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        # Actualiza el cliente en la base de datos
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        # Cierra la ventana
        self.close()

    def close(self):
        # Cierra la ventana
        self.destroy()
        self.update()

# Ejecuta la aplicación principal
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()