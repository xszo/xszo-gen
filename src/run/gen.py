import yaml
from subprocess import run

with open("src/run/run.yml", "tr", encoding="utf-8") as file:
    data = yaml.safe_load(file)

for item in data["run-point"]:
    run([data["env-python"], "src/" + item + "/run.py"], check=True)

run(["cp", "-f", "LICENSE", "out/LICENSE"], check=True)
run([data["env-python"], "src/out/run.py"], check=True)
