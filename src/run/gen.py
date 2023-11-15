from subprocess import run
from var import data

for item in data["run-point"]:
    run([data["env-python"], "src/" + item + "/run.py"], check=True)

run(["cp", "-f", "LICENSE", "out/LICENSE"], check=True)
run([data["env-python"], "src/out/run.py"], check=True)
