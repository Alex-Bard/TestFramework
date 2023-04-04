def print_red(text):
    print("\033[31m{}\033[37m".format(text))
    reset_print()


def print_yellow(text):
    print("\033[33m{}\033[37m".format(text))
    reset_print()


def print_green(text):
    print("\033[32m{}\033[37m".format(text))
    reset_print()


def reset_print():
    pass
