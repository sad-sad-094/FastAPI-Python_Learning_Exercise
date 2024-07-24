import requests

URL = 'https://localhost:8000/reviews'
HEADERS = {'accept': 'application/json'}
QUERYSET = {'page': 2, 'limit': 1}

response = requests.get(URL, headers=HEADERS, params=QUERYSET)

if response.status_code == 200:
    print('Petición exitosa')

    if response.headers.get('content-type') == 'application/json':
        reviews = response.json()
        for review in reviews:
            print(f"score: {review['score']} - {review['review']}")