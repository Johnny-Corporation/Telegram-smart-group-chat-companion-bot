try:
    exec(open("main.py", encoding="utf-8").read())
except Exception as e:
    print("~" * 500)
    print("main.py fell due to the error:")
    print(e)
    print("~" * 500)
    exec(open("reserve.py", encoding="utf-8").read())
