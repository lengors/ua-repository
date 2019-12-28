class stopping:
    def __init__(self, arguments):
        if arguments is None:
            self.words = [ ]
        elif type(arguments) == str:
            with open(arguments, 'r') as fin:
                self.words = [ line.strip() for line in fin ]
        else:
            self.words = [ line.strip() for line in arguments ]

    def __call__(self, content):
        return [ word for word in content if word not in self.words ]