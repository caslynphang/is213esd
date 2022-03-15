
import requests
from datetime import date, timedelta
# yesterday / today->(api may not update that quickly :|)
# yesterday = str(date.today() - timedelta(days=1))
today = str(date.today())

# get all the stocks trade volume (USE YOUR OWN KEYS LOL[i only hv 5 req/min]-- polygon.io)
r = requests.get('https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/'+today +'?adjusted=true&apiKey=')
results = r.json()['results']
trade_volume_list = []

# get top 20 stocks trade volume in order
for result in results:
    trade_volume_list.append(result['v'])
trade_volume_list.sort()
top20_volume_list = trade_volume_list[-20:]
print(top20_volume_list)
 
for a in top20_volume_list:
    for result in results:
        if result['v'] == a:
            print("Ticker: "+str(result['T'])+"; Trade Volume: "+ str(result['v']))


