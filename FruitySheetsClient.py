import gspread
from oauth2client.service_account import ServiceAccountCredentials
from TPAPI import getTPData


class FruitySheetsClient():
    
    _data = {}
    
    def __init__(self, APIKeyPath : str) -> None:
        
        self._scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self._creds = ServiceAccountCredentials.from_json_keyfile_name(APIKeyPath, self._scope)
        self._client = gspread.authorize(self._creds)

    def updateData(self):
        self._data = getTPData()

    def updateSheets(self):

        sheet = self._client.open('Guild Wars Gilden Halle Tracking')
        sheetInstance = sheet.get_worksheet(0)
        content = sheetInstance.col_values(2)
        toInsert = []
        for row in content:
            if row in self._data:
                value = self._data[row]["buy"]
                toInsert.append([value/10000])
            elif row == "Material" :
                toInsert.append(["Wert (einzeln)"])
            else:
                toInsert.append([""])
                
        sheetInstance.update(f'E1:E{len(toInsert)}', toInsert)



