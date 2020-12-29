from invoke import task, run

# Tarea de limpieza de ficheros
@task 
def clean(c):
	print("Borrando caché de python.")
	run("find . -maxdepth 5 -type d -name  .pytest_cache -exec rm -r {} +")
	run("find . -maxdepth 5 -type d -name __pycache__ -exec rm -r {} +")

# Tarea de ejecución de tests
@task
def test(c):
	print("Ejecución de test.\n")
	run("pytest -v --disable-pytest-warnings src/test/*")

# Tarea de ejecución del modelo
@task
def execute(c):
	print("Ejecución del modelo\n")
	run("python3 ./src/core/main.py")
	print("Fin de la ejecución.")

# Tarea build, en nuestro caso no hace nada
@task
def build(c):
	print("Build realizado\n")

# Tarea install, en nuestro caso no hace nada
@task
def install(c):
	print("Instalación completada\n")
