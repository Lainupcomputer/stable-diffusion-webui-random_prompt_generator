import sys

try:
    from ez_storage.ez_storage import Ez_Storage
except ModuleNotFoundError:
    print("ez_storage module is missing (pip install ez-storage)")

SPACER = "-" * 50
if len(sys.argv) > 1:
    if sys.argv[1] == "--help":
        print("HELP PAGE")
        print("(m/f/n) = (manual_input/read_from_file/no)")
        print("file imports: put every prompt into a separated line.")
        print("category weight:(0-10) = How many prompts should be take from list when generating.")
        print("Programm will auto save after each procedure.")
        sys.exit()


def read_file(file_path):
    l_data: list[str] = []
    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            # remove new line
            sl = line.split("\n")
            l_data.append(sl[0])
        return l_data


def get_input(hint=None, mode="y_n"):
    i = input(hint)
    if mode == "y_n":
        if i == "y":
            return True
        elif i == "n":
            return False
    if mode == "i":
        if i == "n":
            return False
        else:
            return i
    else:
        return i


default = Ez_Storage("default.ezs")
print("migrate_to_ez:")
print(SPACER)
# ask static_positive
enable_static_positive = get_input("enable: add static prompt ?\n(y/n):\n")
if enable_static_positive:
    try:
        static_positive = default.get_storage(mode="l", obj="static_positive")
        print(f"Found {len(static_positive)} Prompts.")
    except KeyError:
        print(f"Found 0 Prompts.")
    finally:
        static_positive_import = get_input("import static positive prompts?\n(m/f/n)\n", mode="i")
        if static_positive_import == "m":
            inp = get_input("enter static_positive prompts:\nput multiple separated by ';':\n", mode="r")
            data = inp.split(";")
        elif static_positive_import == "f":
            path = get_input("enter file name:\nplace file in '/Tools':\n", mode="r")
            data = read_file(path)
        else:
            data = None
    if get_input(f"add: {data} to 'static_positive'?\n(y/n)\n"):
        default.add_storage(mode="l", obj="static_positive", data=data)
elif not enable_static_positive:
    pass
default.add_storage(mode="o", obj="Settings", data="enable_static_positive", value=enable_static_positive,
                    override=True)
print(SPACER)
# ask static_negative
enable_static_negative = get_input("enable: add static negative prompt ?\n(y/n):\n")
if enable_static_negative:
    try:
        static_negative = default.get_storage(mode="l", obj="static_negative")
        print(f"Found {len(static_negative)} Prompts.")
    except KeyError:
        print(f"Found 0 Prompts.")
    finally:
        static_negative_import = get_input("import static negative prompts?\n(m/f/n)\n", mode="i")
        if static_negative_import == "m":
            inp = get_input("enter static_negative prompts:\nput multiple separated by ';':\n", mode="i")
            data = inp.split(";")
        elif static_negative_import == "f":
            path = get_input("enter file name:\nplace file in '/Tools':\n", mode="p")
            data = read_file(path)
        else:
            data = None
    if get_input(f"add: {data} to 'static_negative'?\n(y/n)\n"):
        default.add_storage(mode="l", obj="static_negative", data=data)
elif not enable_static_negative:
    pass
default.add_storage(mode="o", obj="Settings", data="enable_static_negative", value=enable_static_negative,
                    override=True)
print(SPACER)
print("static prompts setup: done")
try:
    print(f'Found {len(default.get_storage(mode="l", obj="static_negative"))} negative Prompts.')
    print(f'Found {len(default.get_storage(mode="l", obj="static_positive"))} positive Prompts.')
except KeyError:
    pass
print(SPACER)
while True:
    print("import mode:")
    name = input("enter category name:\n")
    weight = input("enter category weight:\n(0-10)\n")
    i = get_input("is nsfw ?\n")
    if i:
        prefix = "nsfw_"
    else:
        prefix = "sfw_"
    ipt = get_input("import from?\n(m/f)\n", mode="i")
    if ipt == "m":
        inp = get_input("enter prompts:\nput multiple separated by ';':\n", mode="i")
        data = inp.split(";")
    elif ipt == "f":
        path = get_input("enter file name:\nplace file in '/Tools':\n", mode="i")
        data = read_file(path)
    else:
        data = None
    array = {f"{prefix + name}": int(weight)}
    default.add_storage(mode="a", obj=f"{prefix}registered_prompts", array_data=array)
    default.add_storage(mode="l", obj=f"{prefix + name}", data=data)
    print(SPACER)
    i = input("type 'q + ENTER' to exit or press 'ENTER' to resume\n")
    if i == "q":
        sys.exit()
