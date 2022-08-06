import csv
from urllib.request import Request, urlopen

def prepareRow(row: list) -> list:
    try:
        if len(row) != 6:
            return [-1] * 6
        newRow = [-1] * 6
        newRow[0] = int(row[0])
        newRow[1] = row[1]
        entry: str
        newRow[3:] = [int(entry) if entry.isdigit() else -1 for entry in row[3:]]
        return newRow
    except:
        raise ValueError(f"This row is malformed: {row}")

def getTPData():
    url = 'http://api.gw2tp.com/1/bulk/items.csv'

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    lines = [l.decode('utf-8') for l in response.readlines()]
    rawData = list(csv.reader(lines))

    data = {}

    for row in rawData[1:]:
        row = prepareRow(row)
        data[str(row[1])] = {"id":row[0],
                            "buy":row[2],
                            "sell":row[3],
                            "supply":row[4],
                            "demand":row[5]}
    return data
        
