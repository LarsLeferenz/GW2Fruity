import itertools
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
        self.sheet = self._client.open('Guild Wars Gilden Halle Tracking') #Test

    def updateData(self):
        self._data = getTPData()
        
    def updateProfits(self):
        ### Zweites Sheet
        sheetInstance = self.sheet.worksheet("Ausrüstungs Farm")
        content = sheetInstance.col_values(3)
        oldValues = sheetInstance.col_values(6)
        toInsert = []
        for index, cell in enumerate(content):
            if cell in self._data:
                value = self._data[cell]["sell"]
                toInsert.append([value])
            elif cell == "Englisch" :
                toInsert.append(["Preis (Sell)"])
            elif cell == "Exoctic Weapon" :
                toInsert.append(["5473"])
            else:
                toInsert.append([oldValues[index]])
        
        sheetInstance.update(f'F1:F{len(toInsert)}', toInsert)
        time.sleep(1)
        
        profit = sheetInstance.acell('J22').value
        history = sheetInstance.col_values(13)
        dates = sheetInstance.col_values(14)
        
        profit = float(profit.replace(",", ".")[:-1])
        lastValue = float(history[-1].replace(",", "."))
        profit = max(profit, lastValue-20)
        profit = min(profit, lastValue+20)
        
        sheetInstance.update(f'M{len(history)+1}:M{len(history)+1}',[[str(profit).replace(".",",")]], value_input_option='USER_ENTERED')
        sheetInstance.update(f'N{len(dates)+1}:N{len(dates)+1}', [[time.strftime("%d.%m.%Y %H:%M:%S")]] ,value_input_option='USER_ENTERED')
        

    def updateSheets(self):
         
        #test
        for tab in ["Schänke", "Mine","Werkstatt","Markt","Lagezentrum","Arena","Crafting"]:
            sheetInstance = self.sheet.worksheet(tab)
            content = sheetInstance.col_values(2)
            oldValues = sheetInstance.col_values(5)
            toInsert = []
            material : str; oldValue : str
            for material, oldValue in itertools.zip_longest(content,oldValues, fillvalue=""):
                if (not material.startswith("#")) and material in self._data:
                    value = self._data[material]["buy"]
                    toInsert.append([value/10000])
                elif material == "Material" :
                    toInsert.append(["Wert (einzeln)"])
                else:
                    toInsert.append([oldValue])
                    
            sheetInstance.update(f'E1:E{len(toInsert)}', toInsert)

        
        
        
        

