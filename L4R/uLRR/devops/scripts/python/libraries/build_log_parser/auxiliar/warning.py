class Warning:
    def __init__(self, message, position):
        self.message = message
        self.position = []
        self.counter = 1

        self.position.append(position)

    def increase_counter(self, position):
        self.counter += 1
        self.position.append(position)