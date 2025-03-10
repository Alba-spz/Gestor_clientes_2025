class Cliente:
    def __init__(self, dni, nombre, apellidos):
        self.dni = dni
        self.nombre = nombre
        self.apellidos = apellidos

    def __repr__(self):
        return f"Cliente({self.dni}, {self.nombre}, {self.apellidos})"
    