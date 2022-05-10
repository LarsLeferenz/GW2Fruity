import gspread
from oauth2client.service_account import ServiceAccountCredentials
from TPAPI import getTPData

data = getTPData()

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(r'C:\\Users\\Lars\\Documents\\guildwars2-fruity-4eab3be354bc.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Guild Wars Gilden Halle Tracking')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

toInsert = []

content = sheet_instance.col_values(2)
for row in content:
    if row in data:
        value = data[row]["buy"]
        if value > 9999:
            text = f"{value//10000}G {(value%10000)//100}S {value%100}K"
        elif value > 99:
            text = f"{(value%10000)//100}S {value%100}K"
        else:
            text = f"{value}K"
        toInsert.append([text])
    elif row == "Material" :
        toInsert.append(["Wert"])
    else:
        toInsert.append([""])
        
sheet_instance.update('E1:E'+str(len(toInsert)), toInsert)



