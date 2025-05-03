import copy
import unittest
import database as db
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente('18L', 'Hugo', 'González'),
            db.Cliente('23H', 'Víctor', 'Laso'),
            db.Cliente('44F', 'Julia', 'Pozo')
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('18L')
        cliente_no_existente = db.Clientes.buscar('77S')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_no_existente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('60B', 'Manolo', 'Gallardo')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '60B')
        self.assertEqual(nuevo_cliente.nombre, 'Manolo')
        self.assertEqual(nuevo_cliente.apellido, 'Gallardo')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('18L'))
        cliente_modificado = db.Clientes.modificar('18L', 'Luis', 'Díaz')
        self.assertEqual(cliente_a_modificar.nombre, 'Hugo')
        self.assertEqual(cliente_modificado.nombre, 'Luis')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('23H')
        cliente_rebuscado = db.Clientes.buscar('23H')
        self.assertNotEqual(cliente_borrado, cliente_rebuscado)
    
    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))       # válido
        self.assertFalse(helpers.dni_valido('23223S', db.Clientes.lista))   # demasiado largo
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))      # formato incorrecto
        self.assertFalse(helpers.dni_valido('18L', db.Clientes.lista))      # ya existe

    def test_escritura_csv(self):
        db.Clientes.borrar('18L')
        db.Clientes.borrar('23H')
        db.Clientes.modificar('44F', 'Nieves', 'Murillo')
        dni, nombre, apellido = None, None, None
        with open(config.DATABASE_PATH, newline="\n") as fichero:
            reader = csv.reader(fichero, delimiter=";")
            dni, nombre, apellido = next(reader)
        self.assertEqual(dni, '44F')
        self.assertEqual(nombre, 'Nieves')
        self.assertEqual(apellido, 'Murillo')



if __name__ == '__main__':
    unittest.main()
