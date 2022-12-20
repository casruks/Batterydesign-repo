import os
import re
import digikey
import math as m
from itertools import chain
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

def findIndex(i):
    for n in range(len(result.products[i].parameters)):
        if result.products[i].parameters[n].parameter_id == 2049: #capacitance
            i_C = n
        else:
            i_C = 'None found'
        if result.products[i].parameters[n].parameter_id == 46: #size/dim
            i_D = n
        else:
            i_D = 'None found'
        if result.products[i].parameters[n].parameter_id == 1500: #height
            i_H = n
        else:
            i_H = 'None found'
        if result.products[i].parameters[n].parameter_id == 2079: #rated voltage
            i_V = n
        else: 
            i_V = 'None found' #for i = 38 
    return i_C, i_D, i_H, i_V

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
        str_found = '0' #NOTHING FOUND CODE
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

x = int(m.ceil(2104/50))  #2104
y = 50
for i in range(43): #43(x) times (y) results = 2106
    search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y)
    result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')
    ist = i
    for i in range(len(result.products)):
        i_C, i_D, i_H, i_V = findIndex(i)
        if type(i_C) and type(i_D) and type(i_H) and type(i_V) == int():
            C = float(result.products[i].parameters[i_C].value.strip(' mF'))
        
            # D, two values (rectangle) or Diam (cylinder)
            if type(ExtractData_D(result.products[i].parameters[i_D].value)) == tuple:
                L, W = ExtractData_D(result.products[i].parameters[i_D].value)          
            else:
                L = W = ExtractData_D(result.products[i].parameters[i_D].value) #cyl
        
            H = ExtractData_H(result.products[i].parameters[i_H].value)
            V_n = float(result.products[i].parameters[i_V].value.strip(' V'))
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
                if no_fitted == m.ceil(n_req):
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
        else:
            i += 1 
    print(str(ist+1) + '/' + str(x) + ' done..')

print('Total no of capacitors found =',result.products_count)
print('No. of results after filter =', len(Clst))
with open('Filtered_results.txt', 'w') as f:
    for line in filtered_results:
        f.write(f"{line}\n")