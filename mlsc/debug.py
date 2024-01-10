""" Various output stuff. """

class Debug:
    def __init__(self, name):
        self.name = name

    def log(self, text):
        """ Print debugging output in a consistent way. """
        print(self.name + ": " + text)

