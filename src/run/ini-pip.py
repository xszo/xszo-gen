from subprocess import run
from var import data

run([data["env-python"], "-m", "pip", "install"] + data["env-pip"], check=True)
