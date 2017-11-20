import json
from pprint import pprint

class House:

    def __init__(self):

        self.price = 0
        self.bedrooms = 0
        self.bathrooms = 0
        self.land_size = 0
        self.square_footage = 0 #(square footage)
        self.building_age = 0
        self.rooms = 0
        self.average_age_area = 0 #(average home age in area)
        self.walk_score = 0
        self.building_type = -1
        self.postal_code_prefix = ""
        self.postal_code_prefix_mapping = ""

        self.postal_code_prefix_dict = dict ([('V8N', 0), ('V9E', 1), ('V9B', 2), ('V9C', 3), ('V9A', 4), ('V8Y', 5), ('V8X',6), ('V8Z', 7), ('V8T', 8), ('V8W', 9), ('V8V', 10), ('V8P', 11), ('V8S', 12), ('V8R', 13)])
        self.dict = dict([('Townhome', 0), ('Apartment', 1), ('Duplex', 2), ('Single Family', 3), ('Mobile Home', 4), ('Manufactured Home', 5), ('House', 6), ('Condo', 7), ('Townhouses', 8) ])
