from math import asin, cos, pi, sin, sqrt

class ManIsland(object):
    LONG = 0
    LAT = 1
    POST_OFFICE_ARC_LIMIT = 4
    EARTH_RADIUS = 6371

    def __init__(self):
        self.arcs = {}                      # {crossroad_id: [crossroad_id_1, ..., crossroad_id_10]}
        self.distances = {}                 # {crossroad_id: {post_office_id: distance}}
        self.crossroads = {}                # {crossroad_id: (long, lat)}
        self.potential_post_offices = []    # [crossroad_id_1, ..., crossroad_id_10]
        self.get_data()

    def get_data(self):
        """
        Imports data from man.txt and calculate the distances between the crossroads and the potential post offices
        """
        self.print_title("Part 1 : Get Data")
        self.print_progress(0)
        self.crossroads = self.get_crossroads()
        self.print_progress(0.2)
        self.arcs = self.get_arcs()
        self.print_progress(0.4)
        self.potential_post_offices = self.get_potential_post_offices()
        self.print_progress(0.7)
        self.distances = self.get_distances()
        self.print_progress(1)

    def save_laposte_data(self):
        """
        Save the data needed for the facility_location.zpl file into "man_laposte.txt"
        """
        self.print_title("Part 2 : Save Data")
        with open("man_data/man_laposte.txt", "w") as file:
            self.print_progress(0)
            for crossroad_id in self.crossroads:
                file.write("v %s %s %s\n" % (crossroad_id, self.crossroads[crossroad_id][self.LONG], self.crossroads[crossroad_id][self.LAT]))
            file.write("\n")
            self.print_progress(0.2)
            for post_office_id in self.potential_post_offices:
                file.write("p %s\n" % (post_office_id))
            file.write("\n")
            self.print_progress(0.4)
        with open("man_data/man_laposte_distance.txt", "w") as file:
            for crossroad_id in self.distances:
                for post_office_id in self.distances[crossroad_id]:
                    file.write("d %s %s %s\n" % (crossroad_id, post_office_id, self.distances[crossroad_id][post_office_id]))
            self.print_progress(1)
            file.write("\n")

    def get_crossroads(self):
        """
        Builds the crossroads dictionnary from "man.txt"
        crossroads = { crossroad_id : (logitude, latitude) }
        """
        crossroads = {}
        with open("man_data/man.txt", "r") as content_file:
            line = content_file.readline()
            while line:
                if self.is_crossroad(line):
                    line = line.split()
                    if not len(line) == 4:
                        raise SyntaxError
                    crossroad_id = int(line[1])
                    longitude = float(line[2])
                    latitude = float(line[3])
                    crossroads[crossroad_id] = (longitude, latitude)
                line = content_file.readline()
        return crossroads

    def is_crossroad(self, line):
        return line.startswith("v")

    def get_arcs(self):
        """
        Builds the arcs dictionnary from "man.txt"
        arcs = { crossroad_id : [crossroad_id_1, crossroad_id_2, ...] }
        In the array, all the crossroads that are linked by an arc to the crossroad_id are saved.
        """
        arcs = {}
        for crossroad_id in self.crossroads:
            arcs[crossroad_id] = []
        with open("man_data/man.txt", "r") as content_file:
            line = content_file.readline()
            while line:
                if self.is_arc(line):
                    line = line.split()
                    if not len(line) == 4:
                        raise SyntaxError
                    crossroad_id_1 = int(line[1])
                    crossroad_id_2 = int(line[2])
                    arcs[crossroad_id_1].append(crossroad_id_2)
                line = content_file.readline()
        return arcs

    def is_arc(self, line):
        return line.startswith("a")

    def get_potential_post_offices(self):
        """
        Builds the potential_post_offices array using the data from self.crossroads and self.arcs
        """
        potential_post_offices = [crossroad_id for crossroad_id in self.crossroads if self.is_potential_post_office(crossroad_id)]
        return potential_post_offices

    def is_potential_post_office(self, crossroad_id):
        """
        Only the crossroads that have more than 4 branches are considered as a potential post office
        """
        return len(self.arcs[crossroad_id]) >= self.POST_OFFICE_ARC_LIMIT

    def get_distances(self):
        """
        Builds the distances dictionnary using the data from self.crossroads and self.potential_post_offices
        distances = { crossroad_id : { post_office_id : distance(crossroad_id, post_office_id) } }
        """
        distances = {}
        for crossroad_id in self.crossroads:
            distances[crossroad_id] = {}
        for crossroad_id in self.crossroads:
            for post_office_id in self.potential_post_offices:
                distance = self.calculate_distance(crossroad_id, post_office_id)
                distances[crossroad_id][post_office_id] = distance
        return distances

    def calculate_distance(self, crossroad_id_1, crossroad_id_2):
        """
        Calculate the great-circle distance between two points on a sphere given their longitudes and latitudes
        using the haversine formula.
        """
        lat_1, long_1 = self.crossroads[crossroad_id_1][self.LONG], self.crossroads[crossroad_id_1][self.LAT]
        lat_2, long_2 = self.crossroads[crossroad_id_2][self.LONG], self.crossroads[crossroad_id_2][self.LAT]
        term_1 = pow(sin((pi/180)*(lat_2 - lat_1)/2), 2)
        term_2 = cos((pi/180)*lat_1) * cos((pi/180)*lat_2) * pow(sin((pi/180)*(long_2 - long_1)/2), 2)
        distance = 2 * self.EARTH_RADIUS * asin(sqrt(term_1 + term_2))
        return round(distance, 3)

    def print_progress(self, percentage):
        progress = int(10 * percentage)
        print("####" * progress + "    " * (10 - progress) + (" %s%s ") % (progress * 10, '%'))

    def print_title(self, title):
        print("_" * 80)
        print(" " * 31 + title)
        print("_" * 80)