import servo
from angle import Angle
from aviation_edge_api import AviationEdgeApi
from collections import OrderedDict
from operator import itemgetter
import json
import time
from photo_maker import Camera


class AeroTracer:
    def __init__(self):
        self.config = self.get_config()

    def get_config(self):
        file = open("config.json", "r")
        return json.load(file)

    def get_flights(self, airport):
        return AviationEdgeApi(self.config['api']['aviation_edge_api_key']).get_all_flights_to(airport)

    def get_nearest_flight(self, airport, home):
        # flight_list = {}
        nearest_flight = {}
        all_flights = self.get_flights(airport)
        print(all_flights)
        try:
            for flight in all_flights:
                angle = Angle()
                print("Flight: " + flight['flight']['iataNumber'])
                flight_xy = {"x": float(flight['geography']['latitude']), "y": float(flight['geography']['longitude'])}
                flight['distance'] = angle.calculate_distance(home, flight_xy)
                # flight_list[flight['flight']['icaoNumber']] = angle.calculate_distance(home, flight_xy)
            # print("All flights: ", all_flights)
            # nearest_flight = OrderedDict(sorted(flight_list.items(), key=itemgetter(1)))
            # nearest_flight = OrderedDict(sorted(all_flights, key=lambda i: i['distance']))
            # print("Nearest flights: ", nearest_flight)
            nearest_flight = sorted(all_flights, key=lambda i: i['distance'])
            print("Nearest flights: ", nearest_flight[0])
        except:
            print("No Flights")
        # nearest_flight = sorted(all_flights, key=lambda i: i['distance'])
        # print("Nearest flights: ", nearest_flight[0])
        return nearest_flight

    def move_servo(self, start, end, plane):
        # while True:
        # plane = {"x", "y"}
        # x = float(input("Input x: "))
        # y = float(input("Input y: "))
        # plane = {"x": x, "y": y}
        angle = Angle()
        angle_to_move = angle.calculate_angle(start, end, plane)
        # angle.calculate_distance(start, end)
        # angle.calculate_distance(start, plane)
        print("Rotating to: ", str(angle_to_move+90))
        servo.move_to_angle(angle_to_move+90)

    def aeroTracer_start(self):
        while True:
            aero_tracer = AeroTracer()
            # config = aero_tracer.get_config()
            nearest = aero_tracer.get_nearest_flight("ODS", aero_tracer.config['initial_vector']['start'])
            if len(nearest) > 0:
                plane_point = {"x": float(nearest[0]['geography']['latitude']), "y": float(nearest[0]['geography']['longitude'])}
                aero_tracer.move_servo(aero_tracer.config['initial_vector']['start'], aero_tracer.config['initial_vector']['end'], plane_point)
            time.sleep(300)

    def camera_rotating_start(self):
        photo = Camera()
        while True:
            init = 60
            last = 120
            step = 10
            for x in range(init, last, step):
                servo.move_to_angle(x)
                time.sleep(2)
                photo.take_picture()
                time.sleep(30)
            for y in range(last, init, step*(-1)):
                servo.move_to_angle(y)
                time.sleep(2)
                photo.take_picture()
                time.sleep(30)


start = AeroTracer()
start.camera_rotating_start()
