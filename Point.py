class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, point):
        a = abs(self.x - point.x)
        b = abs(self.y - point.y)
        return ((a ** 2) + (b ** 2)) ** 0.5

    '''
    def __repr__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + ")"

    def __str__(self):
        return self.__repr__()
    '''
