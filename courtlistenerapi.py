import requests
import json 
import pandas as pd

BASE_URL = 'https://www.courtlistener.com/api/rest/v3/search/?page='
PARAMETERS = '&q=artificial%20intelligence&type=r'
results = []
for page in range(1, 1000):
    print(page)
    url = BASE_URL + str(page) + PARAMETERS
    res = requests.get(url)
    print(res.text)
    try:
        results.extend(res.json()['results'])
    except:
        print(res.text)

with open('data.json', 'w') as f:
    print(len(results))
    json.dump(results, f)
#with open("response.json", "w") as f:
#    f.write(res.text)

with open('data.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('csvfile.csv', encoding='utf-8', index=False)