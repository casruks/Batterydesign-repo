import pickle
import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest, ParametricFilter  


os.environ['DIGIKEY_CLIENT_ID'] = 'rGRVvZwhTTBu8LZrov7v6CbEoAlbuaRL'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'CEIUIRl5vQ2m4pV6'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Documents\\GitHub\\Batterydesign-repo\\tmp'

# store data received 
class MyClass():
    def __init__(self, param):
        self.param = param
        
def save_object(obj):
    try:
        with open("data.pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)

resultlst = []
x = int(2104/8)  #2104
y = 8
for i in range(1): #54(x) times 39(y) results = 2106
    search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y, filters=ParametricFilter(parameter_id=2049,value_id='Capacitance'))
    result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')
    print(str(i) + '/'+str(x)+' done..')
    resultlst.append(result)
    with open('Results\\result' + str(i) + '.txt', 'w') as f:
        f.write(str(result))

obj = MyClass(result)
save_object(obj)