from ser import Ser
from sensor import Sensor

sensors = []

for i in range(1, 5):
    sensors.append(Sensor(id=i, name=f"sensor {i}"))
serv = Ser("localhost", sensors)
serv.start()
