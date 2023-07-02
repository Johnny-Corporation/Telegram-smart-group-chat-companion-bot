from os import path, listdir


def load_templates(dir):
    file_dict = {}
    for file_name in listdir(dir):
        if file_name.endswith(".txt"):
            file_path = path.join(dir, file_name)
            with open(file_path, "r") as file:
                content = file.read()
                file_dict[file_name] = content
    return file_dict
