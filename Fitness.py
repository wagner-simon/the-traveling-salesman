class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def path_distance(self):
        if self.distance == 0:
            path_distance = 0
            for i in range(0, len(self.route)):
                from_point = self.route[i]
                if i + 1 < len(self.route):
                    to_point = self.route[i + 1]
                else:
                    to_point = self.route[i]
                path_distance += from_point.distance_to(to_point)
            self.distance = path_distance
        return self.distance

    def path_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.path_distance())
        return self.fitness
