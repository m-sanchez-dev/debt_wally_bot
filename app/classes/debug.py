""" Method containing the debugger class """


class Debugger:
    def __init__(self):
        pass

    def log(self, *args):
        print(" ".join(map(str, args)))
