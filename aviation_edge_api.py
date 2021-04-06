import requests


class AviationEdgeApi:
    url = "https://aviation-edge.com/v2/public/flights?key="
    headers = {"Content-type": "application/json"}

    def __init__(self, api_key):
        self.api_key = api_key

    def get_all_flights_to(self, airport):
        flights = requests.get(self.url + self.api_key + "&arrIata=" + airport)
        return flights.json()

    def get_flight(self, flight):
        flight = requests.get(self.url + self.api_key + "&flightIata=" + flight)
        return flight.json()
