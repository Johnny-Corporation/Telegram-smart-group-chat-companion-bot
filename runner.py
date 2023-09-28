from time import sleep
from traceback import format_exc
from os import makedirs

try:
    sleep(1)
    exec(open("main.py", encoding="utf-8").read())
except Exception as e:
    makedirs("temp\\", exist_ok=True)
    with open("temp\\error.txt", "w") as f:
        f.write(str(format_exc()))
        f.write("\n\n\n================\n\n\n")
        f.write(str(e))
    ("~" * 3000)
    ("main.py fell due to the error:")
    (e)
    ("~" * 3000)
    exec(open("reserve.py", encoding="utf-8").read())
