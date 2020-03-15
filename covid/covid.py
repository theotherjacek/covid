import sys
from typing import List, Dict
import requests
from colorama import Fore, Style


DATA_URL = "https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Z7biAeD8PAkqgmWhxG2A/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"
ATTRIBUTES = ['Country_Region', 'Confirmed', 'Active', 'Deaths', 'Recovered']
SPACING = 10


def print_country_stats(country_data: Dict):
    for attribute in ATTRIBUTES:
        if attribute == 'Country_Region':
            print(Style.BRIGHT + Fore.GREEN, country_data[attribute], Style.RESET_ALL)
        else:
            print(Style.BRIGHT, attribute, Style.RESET_ALL, ' ' * (SPACING - len(attribute)), country_data[attribute])


def parse_args(argv: List[str]):
    countries = [c.strip() for c in ' '.join(argv[1:]).split(',') if c]
    if not len(countries):
        return ["poland", "us", "china"]

    return [c.lower() for c in countries]


if __name__ == '__main__':
    get_country_name = lambda cdict: cdict['attributes']['Country_Region'].lower()
    countries = parse_args(sys.argv)
    data = requests.get(DATA_URL).json()['features']
    countries_data = {
        get_country_name(country): {
            attribute: country['attributes'][attribute] for attribute in ATTRIBUTES
        } for country in data if get_country_name(country) in countries
    }

    print()
    for country in countries:
        print_country_stats(countries_data[country])
        print()
