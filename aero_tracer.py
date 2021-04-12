import servo
from angle import Angle
from aviation_edge_api import AviationEdgeApi
import json
import time
from photo_maker import Camera
from aws_s3_controller import AWSS3Controller


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
                plane_point = {"x": float(nearest[0]['geography']['latitude']),
                               "y": float(nearest[0]['geography']['longitude'])}
                aero_tracer.move_servo(aero_tracer.config['initial_vector']['start'],
                                       aero_tracer.config['initial_vector']['end'], plane_point)
            time.sleep(300)

    def move_servo_and_take_photo(self, photo, aws, move_angle, full_filename, small_filename):
        # photo = Camera()
        # aws = AWSS3Controller(self.config['aws'])
        servo.move_to_angle(move_angle)
        time.sleep(2)
        photo.take_full_picture(full_filename)
        photo.take_small_picture(small_filename)
        aws.upload_to_s3(small_filename, self.config['aws']['bucket'],
                         self.config['aws']['prefix'] + small_filename, {'ACL': 'public-read'})
        time.sleep(self.config['servo']['moving_pause'])

    def camera_rotating_start(self):
        photo = Camera()
        aws = AWSS3Controller(self.config['aws'])
        full_filename = "image.jpg"
        small_filename = "image_small.jpg"
        while True:
            init = self.config['servo']['init_angle']
            last = self.config['servo']['final_angle']
            step = self.config['servo']['moving_step']
            for x in range(init, last, step):
                self.move_servo_and_take_photo(photo, aws, x, full_filename, small_filename)

            for y in range(last, init, step*(-1)):
                self.move_servo_and_take_photo(photo, aws, y, full_filename, small_filename)


start = AeroTracer()
start.camera_rotating_start()
