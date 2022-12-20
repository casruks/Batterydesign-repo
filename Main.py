import os
import re
import time
import digikey
import math as m
from digikey.v3.productinformation import KeywordSearchRequest
from py3dbp import Packer, Bin, Item 

### Battery Parameters ###
H_box = 42                      #[mm]
W_box = 34                      #[mm]
L_box = 34                      #[mm]
V_box = H_box * W_box * L_box   #[mm3]
Ah = 600e-3                     #[Ah]
V = 3.7                         #[V]
s = 3600                        #[sec]
E = Ah*V*s                      #[J]

os.environ['DIGIKEY_CLIENT_ID'] = 'rGRVvZwhTTBu8LZrov7v6CbEoAlbuaRL'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'CEIUIRl5vQ2m4pV6'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Documents\\GitHub\\Batterydesign-repo\\tmp'

def findIndex(i):
    i_Cint, i_Dint, i_Hint, i_Vint = ('x' for i in range(4))
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
    if i_Cint and i_Dint and i_Hint and i_Vint != 'x': 
        i_C = i_Cint
        i_D = i_Dint
        i_H = i_Hint
        i_V = i_Vint
    return i_C, i_D, i_H, i_V

def ExtractData_C(sampleStr):
    if sampleStr.find('µ') != -1:
        C = float(sampleStr.strip(' µF'))*1e-6
    elif sampleStr.find('m') != -1:
        C = float(sampleStr.strip(' mF'))*1e-3
    else:
        C = float(sampleStr.strip(' F'))
    return C

#Definiton to extract string from data (applicable for D and L)
def ExtractData_H(sampleStr):
    try:
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
    start_time = time.time()
    api_limit = {}
    search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y)
    result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR', api_limits=api_limit)
    ist = i
    for i in range(len(result.products)):
        i_C, i_D, i_H, i_V = findIndex(i)
        print(i_C, i_D, i_H, i_V)
        if type(i_C) == type(1) and type(i_D) == type(1) and type(i_H) == type(1) and type(i_V) == type(1):
            C = ExtractData_C(result.products[i].parameters[i_C].value) ###### FIX Req
            print(C)
            if result.products[i].parameters[i_D].value != '-':
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
            if m.ceil(n_req)*(L*W*H) <= (V_box) and m.ceil(n_req) < 20:
                packer = Packer()
                packer.add_bin(Bin('Battery case', H_box, W_box, L_box, 999999))
                for i in range(m.ceil(n_req)):
                    packer.add_item(Item('Capacitor' + str(i+1), H, W, L, 1+i))
            
                packer.pack()
                for i in packer.bins:
                    no_fitted = len(i.items)
                    no_unfitted = len(i.unfitted_items)
                    if no_fitted >= m.ceil(n_req):
                        Clst.append(C)
                        Hlst.append(H)
                        Wlst.append(W)
                        Llst.append(L)
                        Vlst.append(V_n)
                        dkpnlst.append(dkpn)
                        n_reqlst.append(m.ceil(n_req))
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
    print("--- %s minutes ---" % round((time.time() - start_time)/60,2))
    print('Total estimated time required .. %s minutes' % round(x*(time.time() - start_time)/60,2))
    print(api_limit)

print('Total no. of capacitors found =',result.products_count)
print('No. of results after filter =', len(Clst))
with open('Filtered_results.txt', 'w') as f:
    for line in filtered_results:
        f.write(f"{line}\n")