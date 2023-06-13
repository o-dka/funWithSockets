from ser import Ser
"""
 Make it send random coordinates to the server that will change the positon
 of the square in a smooth fashion!
"""


class Square:
    def __init__(self):
        self.w = 200
        self.h = 200


sq = Square()
serv = Ser("localhost")
serv.start()
