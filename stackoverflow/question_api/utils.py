import requests
from requests.exceptions import HTTPError
from django.conf import settings
import json

class GetStackExchange:
    EP = 'https://api.stackexchange.com/2.2/{}'  # endpoint for Stackexchange API

    
    def search(self, page, tagged, order="desc", sort="activity", site="stackoverflow"):
        param={
            "tagged" : tagged,
            "page": page,
            "order": order,
            "sort" : sort,
            "site" : "stackoverflow"
        }
        try:
            response = requests.get(self.EP.format('search'), params=param)
            json_response = response.json()
            populatedb.delay(tagged,json_response)
            return response.json()
            response.raise_for_status()
        except Exception as err:
            print(f'Other error occurred: {err}')