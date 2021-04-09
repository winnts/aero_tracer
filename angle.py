from math import *


class Angle:
    def angle_diff(self, angle1, angle2):
        diff = abs(angle1 - angle2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def bearing_angle(self, first_point, second_point):
        delta = atan2(sin(second_point["y"] - first_point["y"]) * cos(second_point["x"]),
                      (cos(first_point["x"]) * sin(second_point["x"])) - (sin(first_point["x"]) * cos(second_point["x"]) *
                                                                          cos(second_point["y"] - first_point["y"])))
        initial_bearing = (delta*180/pi + 360) % 360
        return initial_bearing

    def convert_vector_to_rad(self, point):
        new_point = {"x", "y"}
        new_point = {"x": point["x"] * pi / 180, "y": point["y"] * pi / 180}
        return new_point

    def calculate_angle(self, first_point, second_point, third_point):
        home_rad = self.convert_vector_to_rad(first_point)
        aero_rad = self.convert_vector_to_rad(second_point)
        plane_rad = self.convert_vector_to_rad(third_point)

        delta_a = self.bearing_angle(home_rad, aero_rad)
        delta_b = self.bearing_angle(home_rad, plane_rad)
        angle = self.angle_diff(delta_a, delta_b)
        print("Angle: ", angle)
        return angle

    def calculate_distance(self, first_point, second_point):
        start = self.convert_vector_to_rad(first_point)
        end = self.convert_vector_to_rad(second_point)

        a = sin((end["x"]-start["x"])/2) * sin((end["x"]-start["x"])/2) + \
            cos(start["x"]) * cos(end["x"]) * sin((end["y"]-start["y"])/2) * sin((end["y"]-start["y"])/2)

        c = 2 * atan2(sqrt(a), sqrt(1-a))

        d = 6371e3 * c
        print("Distance in km: ", str(round(d/1000, 2)))
        return d
