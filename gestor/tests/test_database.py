import copy
import unittest
import database as db
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Configurar la lista inicial de clientes para las pruebas
        db.Clientes.lista = [
            db.Cliente('18L', 'Hugo', 'González'),
            db.Cliente('23H', 'Víctor', 'Laso'),
            db.Cliente('44F', 'Julia', 'Pozo')
        ]

    def test_buscar_cliente(self):
        # Probar la búsqueda de un cliente existente
        cliente_existente = db.Clientes.buscar('18L')
        # Probar la búsqueda de un cliente no existente
        cliente_no_existente = db.Clientes.buscar('77S')
        # Verificar que el cliente existente no sea None
        self.assertIsNotNone(cliente_existente)
        # Verificar que el cliente no existente sea None
        self.assertIsNone(cliente_no_existente)

    def test_crear_cliente(self):
        # Crear un nuevo cliente
        nuevo_cliente = db.Clientes.crear('60B', 'Manolo', 'Gallardo')
        # Verificar que la lista de clientes tenga un cliente más
        self.assertEqual(len(db.Clientes.lista), 4)
        # Verificar que los datos del nuevo cliente sean correctos
        self.assertEqual(nuevo_cliente.dni, '60B')
        self.assertEqual(nuevo_cliente.nombre, 'Manolo')
        self.assertEqual(nuevo_cliente.apellido, 'Gallardo')

    def test_modificar_cliente(self):
        # Hacer una copia del cliente antes de modificarlo
        cliente_a_modificar = copy.copy(db.Clientes.buscar('18L'))
        # Modificar el cliente
        cliente_modificado = db.Clientes.modificar('18L', 'Luis', 'Díaz')
        # Verificar que el nombre del cliente haya cambiado
        self.assertEqual(cliente_a_modificar.nombre, 'Hugo')
        self.assertEqual(cliente_modificado.nombre, 'Luis')

    def test_borrar_cliente(self):
        # Borrar un cliente existente
        cliente_borrado = db.Clientes.borrar('23H')
        # Intentar buscar el cliente borrado
        cliente_rebuscado = db.Clientes.buscar('23H')
        # Verificar que el cliente borrado no sea igual al cliente buscado
        self.assertNotEqual(cliente_borrado, cliente_rebuscado)
    
    def test_dni_valido(self):
        # Verificar que un DNI válido sea aceptado
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))       # válido
        # Verificar que un DNI demasiado largo sea rechazado
        self.assertFalse(helpers.dni_valido('23223S', db.Clientes.lista))   # demasiado largo
        # Verificar que un DNI con formato incorrecto sea rechazado
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))      # formato incorrecto
        # Verificar que un DNI ya existente sea rechazado
        self.assertFalse(helpers.dni_valido('18L', db.Clientes.lista))      # ya existe

    def test_escritura_csv(self):
        # Borrar clientes y modificar uno para probar la escritura en CSV
        db.Clientes.borrar('18L')
        db.Clientes.borrar('23H')
        db.Clientes.modificar('44F', 'Nieves', 'Murillo')
        dni, nombre, apellido = None, None, None
        # Leer el archivo CSV y verificar los datos escritos
        with open(config.DATABASE_PATH, newline="\n") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            dni, nombre, apellido = next(reader)
        self.assertEqual(dni, '44F')
        self.assertEqual(nombre, 'Nieves')
        self.assertEqual(apellido, 'Murillo')

if __name__ == '__main__':
    # Ejecutar las pruebas
    unittest.main()
