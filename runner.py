from time import sleep

try:
    sleep(1)
    exec(open("main.py", encoding="utf-8").read())
except Exception as e:
    print("~" * 3000)
    print("main.py fell due to the error:")
    print(e)
    print("~" * 3000)
    exec(open("reserve.py", encoding="utf-8").read())
