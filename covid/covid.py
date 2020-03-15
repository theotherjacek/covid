import requests
from colorama import Fore, Style


data_url = "https://services9.arcgis.com/N9p5hsImWXAccRNI/arcgis/rest/services/Z7biAeD8PAkqgmWhxG2A/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"
countries = ['US', 'Poland', 'Germany', 'Italy', 'China']
attributes = ['Country_Region', 'Confirmed', 'Active', 'Deaths', 'Recovered']
spacing = 10


def print_country(data: dict):
    for attribute in attributes:
        if attribute == 'Country_Region':
            print(Style.BRIGHT + Fore.GREEN, data[attribute], Style.RESET_ALL)
        else:
            print(Style.BRIGHT, attribute, Style.RESET_ALL, ' ' * (spacing - len(attribute)), data[attribute])


if __name__ == '__main__':
    data = requests.get(data_url).json()['features']
    countries_data = [{
            attribute: c['attributes'][attribute] for attribute in attributes
        } for c in data if c['attributes']['Country_Region'] in countries
    ]

    for country in countries_data:
        print_country(country)
        print()
