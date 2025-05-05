import os

# Define la ruta de la base de datos según el entorno de ejecución
DATABASE_PATH = (
    # Usa un archivo de prueba si se detecta que se está ejecutando pytest
    "gestor/tests/clientes_test.csv"
    if "PYTEST_CURRENT_TEST" in os.environ
    # Usa el archivo de producción por defecto en caso contrario
    else "clientes.csv"
)