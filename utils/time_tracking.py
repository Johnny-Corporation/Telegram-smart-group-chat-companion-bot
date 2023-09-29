def generate_code(size=8):
    import string
    from random import choice

    chars = string.ascii_letters + string.digits
    code = "".join(choice(chars) for _ in range(size))
    return code


# ------- Promocodes --------


def add_new_code(type_):
    global promocodes
    promocodes[type_] = generate_code()


def update_codes():
    global promocodes

    for type_ in promocodes:
        promocodes[type_] = generate_code()


def check_code(promocodes, promocode_in):
    type_ = next(
        (key for key, value in promocodes.items() if value == promocode_in), None
    )

    if type_ == None:
        ("NOOOOOOOOONEEEEEEEEEEEE")
        return []
    if 'discount' in type_:
        discount = int(type_.split("_")[1])/100
        view = type_.split('_')[2]
        return [discount, view, type_]
    elif 'sub' in type_:
        promocodes[type_] = generate_code()
        return ['Pro', 100, '', type_]
    elif 'JOHNNY' in type_:
        return [0.50, type_]
    elif "messages" in type_:
        num = int(type_.split("_")[1])
        promocodes[type_] = generate_code()
        return [num, '', type_]

    
    else:
        return []
