import json
from pprint import pprint
from House import House

def check_nested_feature_exists(average, age, house):
    if house[average][age] != "":
        return True
    return False

def check_feature_exists(feature, entry):
    if feature in entry:
        return True
    return False

def main():
    with open('remaxDataset.json') as data_file:
        data = json.load(data_file)
        current_house = House()
        house_list = []
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

            if not check_feature_exists('rooms', house):
                continue #skip iteration
            if house['rooms'] == 0:
                continue #skip iteration
            current_house.rooms = house['rooms']

            if not check_nested_feature_exists('average', 'age', house):
                continue #skip iteration
            current_house.average_age_area = house['average']['age']

            house_list.append(current_house)

        print "Total house objects:", len(house_list)



if __name__ == "__main__":
    main()
