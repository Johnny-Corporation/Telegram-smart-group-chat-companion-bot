from time import sleep
from traceback import format_exc

try:
    sleep(1)
    exec(open("main.py", encoding="utf-8").read())
except Exception as e:
    with open("temp\\error.txt","w") as f:
        f.write(str(format_exc()))
        f.write("\n\n\n================\n\n\n")
        f.write(str(e))
    print("~" * 3000)
    print("main.py fell due to the error:")
    print(e)
    print("~" * 3000)
    exec(open("reserve.py", encoding="utf-8").read())
