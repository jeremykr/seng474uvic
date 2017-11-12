import json
from House import House

def check_nested_feature_exists(block, index, house):
    if house[block][index] != "":
        return True
    return False

def check_feature_exists(feature, entry):
    if feature in entry:
        return True
    return False

def main():


    with open('../RemaxScrape/remaxDataset2.json') as data_file:
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

        print "Total house objects:", len(house_list)


if __name__ == "__main__":
    main()
