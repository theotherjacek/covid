## Covid

Simple cli tool to fetch latest covid-19 stats.
Uses data endpoints of https://coronavirus.jhu.edu/map.html.

### Install deps

`pip install -r requirements.txt`

### Run

`python covid/covid.py`

To specify displayed countries:

`python covid/covid.py us, poland, united kingdom`

Output:
```
 US 
 Confirmed    2952
 Active       2883
 Deaths       57
 Recovered    12

 Poland 
 Confirmed    103
 Active       100
 Deaths       3
 Recovered    0

 United Kingdom 
 Confirmed    1143
 Active       1103
 Deaths       21
 Recovered    19
```
