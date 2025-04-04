import json
import requests
from geopy import distance
from pprint import pprint


with open("coffee.json", "r", encoding="CP1251") as coffee_info_file:
    coffee_info = coffee_info_file.read()

coffee_content = json.loads(coffee_info)

""" first_coffee_shop_name = coffee_content[0]["Name"]
first_coffee_shop_logitude = coffee_content[0]["geoData"]["coordinates"][0]
first_coffee_shop_latitude = coffee_content[0]["geoData"]["coordinates"][1]
print(first_coffee_shop_name)
print(first_coffee_shop_logitude)
print(first_coffee_shop_latitude) """


""" for i in coffee_content:
    coffee_shop_name = i["Name"]
    coffee_shop_longitude = i["geoData"]["coordinates"][0]
    coffee_shop_latitude = i["geoData"]["coordinates"][1]
    print(coffee_shop_name, coffee_shop_longitude, coffee_shop_latitude)
 """


api_key = "d1b69c92-c76a-48da-8a9a-21f31e1fed80"


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


# city_A = input("Где вы находитесь? ")
# city_B = input("Где вы находитесь? ")

city = input("Где вы находитесь? ")

# coords_a = fetch_coordinates(api_key, city_A)
# coords_b = fetch_coordinates(api_key, city_B)
coords = fetch_coordinates(api_key, city)

new_structure = []

for i in coffee_content:
    coffee_shop_name = i["Name"]
    coffee_shop_longitude = i["geoData"]["coordinates"][0]
    coffee_shop_latitude = i["geoData"]["coordinates"][1]
    distance_to_coffee_shop = distance.distance(
        reversed(coords), (coffee_shop_latitude, coffee_shop_longitude)
    ).km
    new_structure_coffee_shop = {
        "title": coffee_shop_name,
        "distance": distance_to_coffee_shop,
        "latitude": coffee_shop_latitude,
        "longitude": coffee_shop_longitude,
    }
    new_structure.append(new_structure_coffee_shop)


def get_coffee_shop_distance(cofee_shop):
    return cofee_shop["distance"]


min_distance_to_coffee_shop = min(new_structure, key=get_coffee_shop_distance)

print("Ваши координаты: ", coords)
pprint(min_distance_to_coffee_shop, sort_dicts=False)

sorted_new_structure = sorted(new_structure, key=get_coffee_shop_distance)

for i in sorted_new_structure[:5]:
    print(i["title"])


# distance = distance.distance(reversed(coords_a), reversed(coords_b)).km

# print("Расстояние: ",distance)
