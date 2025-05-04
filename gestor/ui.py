from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING
from tkinter.messagebox import showerror
import database as db
import helpers

class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws / 2) - (w / 2))
        y = int((hs / 2) - (h / 2))
        self.geometry(f"{w}x{h}+{x}+{y}")

class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.center()
    
    def create_client_window(self):
        self.CreateClientWindow(self)

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, 'values')
            confirmar = askokcancel(
                title='Confirmación',
                message=f'¿Borrar a {campos[1]} {campos[2]}?',
                icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    def build(self):
        # --- Frame superior ---
        top_frame = Frame(self)
        top_frame.pack()

        # --- Scrollbar ---
        scrollbar = Scrollbar(top_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        # --- Treeview ---
        treeview = ttk.Treeview(top_frame, yscrollcommand=scrollbar.set)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        # --- Formato columnas ---
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        # --- Encabezados ---
        treeview.heading("#0", anchor=CENTER)
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        # --- Cargar datos de la base de datos ---
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='', index='end', iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )

        treeview.pack()
        scrollbar.config(command=treeview.yview)

        # --- Frame inferior (botones) ---
        bottom_frame = Frame(self)
        bottom_frame.pack(pady=20)

        Button(bottom_frame, text="Crear", command=self.create_client_window).grid(row=1, column=0)
        Button(bottom_frame, text="Modificar", command=self.edit_client_window).grid(row=1, column=1)
        Button(bottom_frame, text="Borrar", command=self.delete).grid(row=1, column=2)

        # --- Exportar el Treeview a atributo de clase ---
        self.treeview = treeview
    
    def create_client_window(self):
        CreateClientWindow(self)
    
    def edit_client_window(self):
        EditClientWindow(self)

class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Crear cliente')
        self.build()
        self.center()
        # Obligar al usuario a interactuar con la subventana
        self.transient(parent)
        self.grab_set()

    def build(self):
        self.validaciones = [0, 0, 0]  # Lista para control de campos

        # Top frame
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Labels
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)

        # --- Entries con bind ---
        self.dni = Entry(frame)
        self.nombre = Entry(frame)
        self.apellido = Entry(frame)

        self.dni.grid(row=1, column=0)
        self.nombre.grid(row=1, column=1)
        self.apellido.grid(row=1, column=2)

        self.dni.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))
        self.nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))
        self.apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 2))

        # Bottom frame
        bottom = Frame(self)
        bottom.pack(pady=10)

        self.crear_button = Button(bottom, text="Crear", command=self.create_client)
        self.crear_button.configure(state=DISABLED)
        self.crear_button.grid(row=0, column=0)

        Button(bottom, text="Cancelar", command=self.close).grid(row=0, column=1)
        
    def validate(self, event, index):
        valor = event.widget.get()
        valido = (
            helpers.dni_valido(valor, db.Clientes.lista)
            if index == 0
            else valor.isalpha() and 2 <= len(valor) <= 30
        )
        event.widget.configure({"bg": "Green" if valido else "Red"})
        self.validaciones[index] = 1 if valido else 0
        self.crear.config(state=NORMAL if self.validaciones == [1, 1, 1] else DISABLED)

    def create_client(self):
        self.master.treeview.insert(
            parent='', index='end', iid=self.dni.get(),
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Actualizar cliente')
        self.master = parent
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        # --- Frame superior ---
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # --- Labels ---
        Label(frame, text="DNI (no editable)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)

        # --- Entries ---
        dni = Entry(frame)
        dni.grid(row=1, column=0)

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda ev: self.validate(ev, 0))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda ev: self.validate(ev, 1))

        # --- Cargar datos del cliente seleccionado ---
        cliente = self.master.treeview.focus()
        if not cliente:
            showerror("Error", "No hay ningún cliente seleccionado.")
            self.destroy()
            return

        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        # --- Frame inferior ---
        frame = Frame(self)
        frame.pack(pady=10)

        actualizar = Button(frame, text="Actualizar", command=self.update_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)

        # --- Activar el botón por defecto ---
        self.validaciones = [1, 1]  # True, True

        # --- Exportar elementos como atributos de clase ---
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def validate(self, event, index):
        valor = event.widget.get()
        valido = valor.isalpha() and 2 <= len(valor) <= 30
        event.widget.configure({"bg": "Green" if valido else "Red"})
        self.validaciones[index] = 1 if valido else 0
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)

    def update_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(
            cliente,
            values=(self.dni.get(), self.nombre.get(), self.apellido.get())
        )
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

