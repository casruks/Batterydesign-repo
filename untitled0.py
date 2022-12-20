import os
import digikey
import math as m
from digikey.v3.productinformation import KeywordSearchRequest


os.environ['DIGIKEY_CLIENT_ID'] = 'rGRVvZwhTTBu8LZrov7v6CbEoAlbuaRL'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'CEIUIRl5vQ2m4pV6'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Documents\\GitHub\\Batterydesign-repo\\tmp'

def findIndex(i):
    i_Cint, i_Dint, i_Hint, i_Vint = (-1 for i in range(4))
    for n in range(len(result.products[i].parameters)):
        if result.products[i].parameters[n].parameter_id == 2049: #capacitance
            i_Cint = n
        else:
            i_C = 'None found'
        if result.products[i].parameters[n].parameter_id == 46: #size/dim
            i_Dint = n
        else:
            i_D = 'None found'
        if result.products[i].parameters[n].parameter_id == 1500: #height
            i_Hint = n
        else:
            i_H = 'None found'
        if result.products[i].parameters[n].parameter_id == 2079: #rated voltage
            i_Vint = n
        else: 
            i_V = 'None found' #for i = 38 
    if i_Cint and i_Dint and i_Hint and i_Vint != -1: 
        i_C = i_Cint
        i_D = i_Dint
        i_H = i_Hint
        i_V = i_Vint
    return i_C, i_D, i_H, i_V

x = int(m.ceil(2104/50))  
y = 50
with open('TestA.txt', 'w') as f:
    for i in range(1): 
        search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y)
        result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')
        f.write(f"{result}\n")
        print(str(i) + '/43 done..')
        for i in range(len(result.products)):
            i_C, i_D, i_H, i_V = findIndex(i)
            print(i_C, i_D, i_H, i_V)
            if type(i_C) and type(i_D) and type(i_H) and type(i_V) == int(): ############
                C = float(result.products[i].parameters[i_C].value.strip(' mF'))
                
                
