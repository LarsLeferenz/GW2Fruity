import csv
from urllib.request import Request, urlopen


def getTPData():
    url = 'http://api.gw2tp.com/1/bulk/items.csv'

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    lines = [l.decode('utf-8') for l in response.readlines()]
    rawData = list(csv.reader(lines))

    data = {}

    for row in rawData[1:]:
        data[str(row[1])] = {"id":int(row[0]),
                            "buy":int(row[2]),
                            "sell":int(row[3]),
                            "supply":int(row[4]),
                            "demand":int(row[5])}
    return data
        