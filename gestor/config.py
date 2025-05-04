import os

DATABASE_PATH = (
    "gestor/tests/clientes_test.csv"
    if "PYTEST_CURRENT_TEST" in os.environ
    else "clientes.csv"
)