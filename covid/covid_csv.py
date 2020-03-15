#!/usr/bin/env python

import sys
from collections import defaultdict
from io import StringIO
from typing import List, Dict
import requests
import csv
from colorama import Fore, Style

DATA_URL_TEMPLATE = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-{}.csv'
COUNTRY_COLUMN = 'Country/Region'
SPACING = 10


def parse_args(argv: List[str]):
    countries = [c.strip() for c in ' '.join(argv[1:]).split(',') if c]
    if not len(countries):
        return ["poland", "us", "china"]

    return [c.lower() for c in countries]


def accumulate(csv_rows, countries: List[str], country_column: str):
    # sum cases from csv_rows in each country present in countries list accumulating its provinces/states.
    result = defaultdict(int)
    for row in [r for r in csv_rows if r[country_column].lower() in countries]:  # filter out rows from other countries
        result[row[country_column]] += int(row[-1])  # get last day from timeseries (latest datapoint)

    return result


if __name__ == '__main__':

    countries = parse_args(sys.argv)
    confirmed, deaths, recovered = [
        csv.reader(
            StringIO(requests.get(DATA_URL_TEMPLATE.format(dataset)).text), delimiter=','
        )
        for dataset in ['Confirmed', 'Deaths', 'Recovered']
    ]
    confirmed_columns, deaths_columns, recovered_columns = next(confirmed), next(deaths), next(recovered)
    confirmed_country_index, deaths_country_index, recovered_country_index = (
        confirmed_columns.index(COUNTRY_COLUMN),
        deaths_columns.index(COUNTRY_COLUMN),
        recovered_columns.index(COUNTRY_COLUMN)
    )

    confirmed_results = accumulate(confirmed, countries, confirmed_country_index)
    deaths_results = accumulate(deaths, countries, deaths_country_index)
    recovered_results = accumulate(recovered, countries, recovered_country_index)

    for country in confirmed_results.keys():
        print(Style.BRIGHT + Fore.GREEN, country, Style.RESET_ALL)
        print(
            Style.BRIGHT,
            'Confirmed:',
            Style.RESET_ALL,
            ' ' * (SPACING - len('Confirmed')),
            confirmed_results[country]
        )
        print(
            Style.BRIGHT,
            'Deaths:',
            Style.RESET_ALL,
            ' ' * (SPACING - len('Deaths')),
            deaths_results[country]
        )
        print(
            Style.BRIGHT,
            'Recovered:',
            Style.RESET_ALL,
            ' ' * (SPACING - len('Recovered')),
            recovered_results[country]
        )
