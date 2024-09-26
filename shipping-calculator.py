import os
from dotenv import load_dotenv
import requests
import time

# https://api.priority1.com/docs/index.html <- Swagger

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = f"https://dev-api.priority1.com/v2/ltl/quotes/rates"
payload = {
    "originZipCode": "07644",
    "destinationZipCode": "90210",
    "pickupDate": "2024-09-27T00:00:00",
    "items": [
        {
            "freightClass": "150",
            "packagingType": "Pallet",
            "units": 1,
            "pieces": 1,
            "totalWeight": 275,
            "length": 48,
            "width": 40,
            "height": 25,
            "isStackable": False,
            "isHazardous": False,
            "isUsed": False,
            "isMachinery": False
        }
    ],
    "enhancedHandlingUnits": [
        {
            "handlingUnitType": "Pallet",
            "units": 1,
            "handlingUnitLength": 48,
            "handlingUnitWidth": 40,
            "handlingUnitHeight": 25,
            "isStackable": False,
            "isMachinery": False,
            "packages": [
                {
                    "packageFreightClass": "50",
                    "weightPerPackage": 275,
                    "quantity": 1,
                    "pieces": 1,
                    "packagingType": "Pallet",
                    "packageLength": 48,
                    "packageWidth": 40,
                    "packageHeight": 25,
                    "packageIsHazardous": False,
                    "packageIsUsed": False,
                    "packageIsMachinery": False,
                    "packageNmfcItemCode": "12345",
                    "packageNmfcSubCode": "08"
                }
            ]
        }
    ],
    "accessorialServices": [
        {"code": "LGPU"},
        {"code": "APPT"}
    ]
}

headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

time_start = time.time()
response = requests.post(url, headers=headers, json=payload)
time_end = time.time()

if response.status_code != 200:
    print(f"Error {response.status_code}: {response.text}")
else:
    print("Success:", response.status_code)


print(f'It took {time_end - time_start} whole seconds to complete the request! Insane!!')


# the api responds with a RateQuoteResponse object, which contains all the carriers that provided their rates
# we are mostly interested in the rateQuotes->carrierName(to validate that it's one of the providers that we use) and rateQuotes->total

a=response.json()
rateQuotes = a['rateQuotes']

for i in rateQuotes:
    print(f"{i['carrierName']} -- {i['rateQuoteDetail']['total']}")