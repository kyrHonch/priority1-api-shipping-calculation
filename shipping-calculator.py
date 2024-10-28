import os
from dotenv import load_dotenv
import requests
import time
import datetime
import math

# https://api.priority1.com/docs/index.html <- Swagger
pallet_info = {
    "totalPallets": 1,  # Количество паллет
    "palletDetails": [  # Список паллет
        {
            "doorsCount": 7,  # Количество дверей
            "height": 112,  # Высота паллеты
            "price": 95,  # Цена паллеты
            "pallet": {  # Информация за паллету
                "externalWidth": 1016,  # Внешняя ширина
                "externalLength": 2489,  # Внешняя длина
                "internalWidth": 965,  # Внутреняя ширина
                "internalLength": 2438,  # Внутреняя длина
                "price": 95  # Цена паллеты
            },
            "weight": "100.02"  # Вес паллеты
        }
    ]
}

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = f"https://dev-api.priority1.com/v2/ltl/quotes/rates"

# перевожу все размеры из мм в дюймы. я округляю вверх всё.
pallet_width = math.ceil(pallet_info["palletDetails"][0]["pallet"]["externalWidth"] / 25.4)  # ширина палета
pallet_length = math.ceil(pallet_info["palletDetails"][0]["pallet"]["externalLength"] / 25.4)  # длина палета

'''
Я не уверен это в мм или же в см. 112 немного высоко в см и недостаточно высоко в мм.
я рассчитываю как мм и добавляю 8 инчей как высота палета самого
'''
pallet_height = math.ceil(8 + (pallet_info["palletDetails"][0]["height"] / 25.4))    # Высота палета.

'''
чтобы получить 12 lb/ft^3. 0.006944 lb/in^3 = 12 lb/ft^3 поскольку я в инчах работаю
'''
pallet_weight = pallet_width*pallet_height*pallet_length * 0.006944

print(f"width: {pallet_width}\nlength: {pallet_length}\nheight: {pallet_height}\nweight: {pallet_weight}\n")

payload = {
    "originZipCode": "07644",  # зип код откуда палет заберают
    "destinationZipCode": "90210",  # зип код куда палет идет
    "pickupDate": str(datetime.datetime.now()),  # Важно поставить дату нынешнюю. Почему то он очень сильно цену завышает если дата не сегодня
    "items": [
        {
            "freightClass": "110",  # класс всегда будет 110
            "packagingType": "Pallet",  # мы отправляем палет
            "units": 1,  # один палет отправлять будем обычно
            "totalWeight": pallet_weight,  # высота палета
            "length": pallet_length,  # длина палета
            "width": pallet_width,  # ширина палета
            "height": pallet_height,  # высота палета
            "isStackable": False,  # всегда false
            "isHazardous": False,  # всегда false
            "isUsed": False,  # всегда false
            "isMachinery": False  # всегда false
        }
    ],
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
    exit()
else:
    print("Success:", response.status_code)

print(f'It took {time_end - time_start} whole seconds to complete the request! Insane!!')

# the api responds with a RateQuoteResponse object, which contains all the carriers that provided their rates
# we are mostly interested in the rateQuotes->carrierName(to validate that it's one of the providers that we use) and rateQuotes->total

a = response.json()
rateQuotes = a['rateQuotes']

for i in rateQuotes:
    print(f"{i['carrierName']} -- {i['rateQuoteDetail']['total']}")
