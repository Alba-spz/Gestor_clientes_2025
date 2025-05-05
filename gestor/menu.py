import database as db
import helpers

def iniciar():
    while True:
        # Limpiar la pantalla
        helpers.limpiar_pantalla()

        # Mostrar el menú principal
        print("========================")
        print("  BIENVENIDO AL Manager ")
        print("========================")
        print("[1] Listar clientes     ")
        print("[2] Buscar cliente      ")
        print("[3] Añadir cliente      ")
        print("[4] Modificar cliente   ")
        print("[5] Borrar cliente      ")
        print("[6] Cerrar el Manager   ")
        print("========================")

        # Solicitar la opción del usuario
        opcion = input("> ")
        # Limpiar la pantalla nuevamente
        helpers.limpiar_pantalla()

        if opcion == '1':
            # Listar todos los clientes
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)

        elif opcion == '2':
            # Buscar un cliente por DNI
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 números y 1 letra)").upper()
            cliente = db.Clientes.buscar(dni)
            # Mostrar el cliente encontrado o un mensaje de error
            print(cliente if cliente else "Cliente no encontrado.")

        elif opcion == '3':
            # Añadir un nuevo cliente
            print("Añadiendo un cliente...\n")

            # Validar el DNI del cliente
            while True:
                dni = helpers.leer_texto(3, 3, "DNI (2 números y 1 letra)").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break

            # Validar el nombre del cliente
            while True:
                nombre = helpers.leer_texto(2, 30, "Nombre (2-30 caracteres)").capitalize()
                if helpers.nombre_valido(nombre):
                    break
                print("Nombre inválido. Solo letras y entre 2 y 30 caracteres.")
                
            # Validar el apellido del cliente
            while True:
                apellido = helpers.leer_texto(2, 30, "Apellido (2-30 caracteres)").capitalize()
                if helpers.apellido_valido(apellido):
                    break
                print("Apellido inválido. Solo letras y entre 2 y 30 caracteres.")

            # Crear el cliente en la base de datos
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente.")

        elif opcion == '4':
            # Modificar un cliente existente
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 números y 1 letra)").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                # Solicitar nuevos datos para el cliente
                nombre = helpers.leer_texto(2, 30, f"Nombre nuevo [{cliente.nombre}]").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido nuevo [{cliente.apellido}]").capitalize()
                # Actualizar el cliente en la base de datos
                db.Clientes.modificar(dni, nombre, apellido)
                print("Cliente modificado correctamente.")
            else:
                # Mostrar mensaje si el cliente no existe
                print("Cliente no encontrado.")

        elif opcion == '5':
            # Borrar un cliente existente
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 números y 1 letra)").upper()
            cliente = db.Clientes.borrar(dni)
            # Mostrar mensaje de éxito o error
            print("Cliente borrado correctamente." if cliente else "Cliente no encontrado.")

        elif opcion == '6':
            # Salir del programa
            print("Saliendo...\n")
            break
        else:
            # Manejar opción no válida
            print("Opción no válida")

        # Pausar la ejecución hasta que el usuario presione ENTER
        input("\nPresiona ENTER para continuar...")

