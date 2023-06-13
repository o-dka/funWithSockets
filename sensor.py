# just a placeholder
class Sensor:
    data = "data"

    def __init__(self, id, name):
        self.id = int(id)
        self.name = str(name)

    def check_data(self):
        return f"{self.data} - from {self.name}"
