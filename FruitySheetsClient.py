import time
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
        ### Erstes Sheet
        sheetInstance = sheet.worksheet("Schenke")
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

        ### Zweites Sheet
        sheetInstance = sheet.worksheet("Ausrüstungs Farm")
        content = sheetInstance.col_values(3)
        toInsert = []
        for row in content:
            if row in self._data:
                value = self._data[row]["sell"]
                toInsert.append([value])
            elif row == "Englisch" :
                toInsert.append(["Preis (Sell)"])
            elif row == "Exoctic Weapon" :
                toInsert.append(["5473"])
            else:
                toInsert.append([""])
        
        sheetInstance.update(f'F1:F{len(toInsert)}', toInsert)
        time.sleep(1)
        
        profit = sheetInstance.acell('J22').value
        
        history = sheetInstance.col_values(13)
        dates = sheetInstance.col_values(14)
        
        history = [[h] for h in history]
        dates = [[d] for d in dates]
        history.append([profit[:-1]])
        dates.append([time.strftime("%d.%m.%Y %H:%M:%S")])
        sheetInstance.update(f'M1:M{len(history)}', history, value_input_option='USER_ENTERED')
        sheetInstance.update(f'N1:N{len(dates)}', dates,value_input_option='USER_ENTERED')
        
        
        
        

