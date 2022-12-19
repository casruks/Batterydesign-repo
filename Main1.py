import os
import re
import digikey
import math as m
from digikey.v3.productinformation import KeywordSearchRequest
from py3dbp import Packer, Bin, Item     #used for optimal location  

### Battery Dimensions in [mm] ###
H_box = 42 
W_box = 34
L_box = 33.8
Ah = 600e-3
V = 3.7
s = 3600
E = Ah*V*s

os.environ['DIGIKEY_CLIENT_ID'] = 'rGRVvZwhTTBu8LZrov7v6CbEoAlbuaRL'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'CEIUIRl5vQ2m4pV6'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Documents\\GitHub\\Batterydesign-repo\\tmp'

#Definiton to extract string from data (applicable for D and L)
def ExtractData_H(sampleStr): 
    try :
        # here ( and ) are our two markers  #'1.654" (42.00mm)' -> 42.00mm
        # in which string can be found. 
        marker1 = '\('
        marker2 = '\)'
        regexPattern = marker1 + '(.+?)' + marker2
        str_found = re.search(regexPattern, sampleStr).group(1)
    except AttributeError:
        # Attribute error is expected if string 
        # is not found between given markers
        str_found = 'Nothing found between two markers'
    return float(str_found.strip('mm')) 

def ExtractData_D(sampleStr): 
    if len(sampleStr.replace('x','')) < len(sampleStr):
        # here ( and ) are our two markers  #'1.654" (42.00mm)' -> 42.00mm
        # in which string can be found. 
        marker1 = '\('
        marker2 = ' x'
        regexPattern = marker1 + '(.+?)' + marker2
        L = re.search(regexPattern, sampleStr).group(1) 
        marker3 = 'mm x '
        marker4 = '\)'
        regexPattern1 = marker3 + '(.+?)' + marker4
        W = re.search(regexPattern1, sampleStr).group(1) 
        outp = float(L.strip('mm')), float(W.strip('mm')) 
    else:
        # here ( and ) are our two markers  #'1.654" (42.00mm)' -> 42.00mm
        # in which string can be found. 
        marker1 = '\(' 
        marker2 = '\)'
        regexPattern = marker1 + '(.+?)' + marker2
        str_found = re.search(regexPattern, sampleStr).group(1)
        outp = float(str_found.strip('mm'))
    return outp

Clst, Hlst, Wlst, Llst, Vlst, dkpnlst, n_reqlst, C_reqlst, filtered_results = ([] for i in range(9))

x = int(2104/50)+1  #2104
y = 50
for i in range(6,43): #43(x) times (y) results = 2106
    search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y)
    result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')
    print(str(i) + '/' + str(x) + ' done..')
    for i in range(x):
        C = float(result.products[i].parameters[12].value.strip(' mF'))
        
        # D, two values (rectangle) or Diam (cylinder)
        if type(ExtractData_D(result.products[i].parameters[3].value)) == tuple:
            L, W = ExtractData_D(result.products[i].parameters[3].value)          
        else:
            L = W = ExtractData_D(result.products[i].parameters[3].value) #cyl
        
        H = ExtractData_H(result.products[i].parameters[10].value)
        V_n = float(result.products[i].parameters[13].value.strip(' V'))
        dkpn = result.products[i].digi_key_part_number
        C_req = 2*(E)/V_n**2
        n_req = C_req / C
        packer = Packer()
        packer.add_bin(Bin('Battery case', H_box, W_box, L_box, 999999))
        for i in range(m.ceil(n_req)):
            packer.add_item(Item('Capacitor' + str(i+1), H, W, L, 1+i))
        
        # packer.pack()
        for i in packer.bins:
            no_fitted = len(i.items)
            no_unfitted = len(i.unfitted_items)
            if no_fitted == n_req:
                Clst.append(C)
                Hlst.append(H)
                Wlst.append(W)
                Llst.append(L)
                Vlst.append(V_n)
                dkpnlst.append(dkpn)
                n_reqlst.append(n_req) 
                C_reqlst.append(C_req) 
                filtered_results.append(Clst)  
                filtered_results.append(Llst) 
                filtered_results.append(Vlst) 
                filtered_results.append(dkpnlst) 
                filtered_results.append(n_reqlst) 
                filtered_results.append(C_reqlst)

with open('Filtered_results.txt', 'w') as f:
    for line in filtered_results:
        f.write(f"{line}\n")