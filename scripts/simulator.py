

class Simulator:
    def __init__(self):
        self.instances = []
        self.factory = self.init_factory()

    def create_instances(self):
        self.ego_vehicle = self.create(ENUM.EgoVehicleStatus)
        self.collision = self.create(ENUM.CollisionInfo)
        self.intersection = self.create(ENUM.IntersectionInfo)
        self.sur_vehicle = self.create(ENUM.SurVehicleStatus)
        self.traffic_light = self.create(ENUM.TrafficLightInfo)
        self.gps = self.create(ENUM.GPSStatus)
        self.instances = [
            self.ego_vehicle,
            self.collision,
            self.intersection,
            self.sur_vehicle,
            self.traffic_light,
            self.gps
        ]

    def create(self, name):
        return self.factory.build(name)

    def start(self):
        for inst in self.instances:
            inst.run()

    def status(self):
        for inst in self.instances:
            inst.status()

    def write_data(self):
        for inst in self.instances:
            inst.write_data()
