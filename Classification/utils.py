import json
from House import House

class Utils:
    
    @staticmethod
    def check_nested_feature_exists(block, index, house):
        return house[block][index] != ""

    @staticmethod
    def check_feature_exists(feature, entry):
        return feature in entry and entry[feature] != ""

    @staticmethod
    def get_house_data(json_file):

        check_feature_exists = Utils.check_feature_exists
        check_nested_feature_exists = Utils.check_nested_feature_exists

        with open(json_file) as data_file:
            data = json.load(data_file)
            current_house = House()
            house_list = []

            prefix_list = []

            for house in data:
                current_house = House()
                if not check_feature_exists('price', house):
                    continue #skip iteration
                current_house.price = house['price']

                if not check_feature_exists('bedrooms', house):
                    continue #skip iteration
                current_house.bedrooms = house['bedrooms']

                if not check_feature_exists('bathrooms', house):
                    continue #skip iteration
                current_house.bathrooms = house['bathrooms']

                if not check_feature_exists('landSize', house):
                    continue #skip iteration
                current_house.land_size = house['landSize']

                if not check_feature_exists('space', house):
                    continue #skip iteration
                current_house.square_footage = house['space']

                if not check_feature_exists('ageofBuilding', house):
                    continue #skip iteration
                current_house.building_age = house['ageofBuilding']

                if not check_feature_exists('buildingType', house):
                    continue
                mapping = current_house.dict[house['buildingType']]
                current_house.building_type = mapping

                if not check_feature_exists('walkScore', house) or house['walkScore'] == None:
                    continue
                current_house.walk_score = house['walkScore']

                if not check_feature_exists('averageLocalAge', house):
                    continue #skip iteration
                current_house.average_age_area = house['averageLocalAge']

                if not check_nested_feature_exists('address', 'postal', house):
                    continue
                current_house.postal_code_prefix = house['address']['postal'][0:3]
                mapping = current_house.postal_code_prefix_dict[house['address']['postal'][0:3]]
                current_house.postal_code_prefix_mapping = mapping

                house_list.append(current_house)

            return house_list

    # Returns len(L)*num_feat numpy matrix and len(L) class matrix
    # for use in classification tasks. The index of a row in X corresponds
    # to the index of its class in y.
    #   L:        List of House objects
    #   num_feat: Number of features
    @staticmethod
    def create_matrices(L, num_feat):
        import numpy as np
        X = np.empty(shape=(len(L), num_feat), dtype=np.float)
        y = np.empty(len(L), dtype=np.float)
        for i, h in enumerate(L):
            y[i] = h.price
            X[i][0] = h.bedrooms
            X[i][1] = h.bathrooms
            X[i][2] = h.land_size
            X[i][3] = h.square_footage
            X[i][4] = h.building_age
            X[i][5] = h.average_age_area
            X[i][6] = h.walk_score
            X[i][7] = h.building_type
            X[i][8] = h.postal_code_prefix_mapping
        return X, y