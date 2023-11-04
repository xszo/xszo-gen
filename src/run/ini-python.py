import yaml
from subprocess import run

with open("src/run/run.yml", "tr", encoding="utf-8") as file:
    data = yaml.safe_load(file)

run([data["env-python"], "-m", "pip", "install", "-r", "requirements.txt"], check=True)
