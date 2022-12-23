import os
import re
import csv
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

os.environ['DIGIKEY_CLIENT_ID'] = 'client id here'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'client secret here'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = '~\\GitHub\\Batterydesign-repo\\tmp'

def findIndex(i):
    i_Cint, i_Dint, i_Hint, i_Vint, i_Tint = ('x' for i in range(5))
    for n in range(len(result.products[i].parameters)):
        if result.products[i].parameters[n].parameter_id == 2049:   #capacitance
            i_Cint = n
        else:
            i_C = 'None found'
        if result.products[i].parameters[n].parameter_id == 46:     #size/dim
            i_Dint = n
        else:
            i_D = 'None found'
        if result.products[i].parameters[n].parameter_id == 1500:   #height
            i_Hint = n
        else:
            i_H = 'None found'
        if result.products[i].parameters[n].parameter_id == 2079:   #rated voltage
            i_Vint = n
        else: 
            i_V = 'None found' #for i = 38 
        if result.products[i].parameters[n].parameter_id == 252:     #operating Temperature
            i_Tint = n
        else:
            i_T = 'None found'
    if i_Cint and i_Dint and i_Hint and i_Vint and i_Tint != 'x': 
        i_C = i_Cint
        i_D = i_Dint
        i_H = i_Hint
        i_V = i_Vint
        i_T = i_Tint
    return i_C, i_D, i_H, i_V, i_T

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

x = int(m.ceil(2104/50))  #2104
y = 50

filtered_results = []

for i in range(43): #43(x) times (y) results = 2106
    start_time = time.time()
    api_limit = {}
    search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y)
    result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR', api_limits=api_limit)
    ist = i
    for i in range(len(result.products)):
        i_C, i_D, i_H, i_V, i_T = findIndex(i)
        if type(i_C) == type(1) and type(i_D) == type(1) and type(i_H) == type(1) and type(i_V) == type(1):
            C = ExtractData_C(result.products[i].parameters[i_C].value)
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
            URL = result.products[i].product_url
            tmpRange = result.products[i].parameters[i_T].value
            if m.ceil(n_req)*(L*W*H) <= (V_box) and m.ceil(n_req) < 20:
                packer = Packer()
                packer.add_bin(Bin('Battery case', H_box, W_box, L_box, 999999))
                for j in range(m.ceil(n_req)):
                    packer.add_item(Item('Capacitor' + str(j+1), H, W, L, 1+j))
            
                packer.pack()
                for k in packer.bins:
                    no_fitted = len(k.items)
                    no_unfitted = len(k.unfitted_items)
                if no_fitted >= m.ceil(n_req):
                    lst = [C, H, W, L, V_n, dkpn, m.ceil(n_req), C_req, tmpRange, URL]
                    data_lst = []
                    for l in lst:
                        data_lst.append(l)
                    filtered_results.append(data_lst)
        else:
            i += 1
    with open('filtered_results.txt', 'w') as f:
        f.write(f"{filtered_results}\n")        
    print(str(ist+1) + '/' + str(x) + ' done..')
    print("---", round((time.time() - start_time),2) ,"sec --- est. time req:", round((x-ist)*(time.time() - start_time),2), "sec ---")
    print(api_limit)
with open("filtered_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Capacitance [F]', 'Height [mm]', 'Width [mm]', 'Length [mm]', 'Voltage - Rated', 'digi-key part number', 'no. of capacitors req.', 'Capacitance req. [F]', 'Operating Temperature', 'Product URL'])
    writer.writerows(filtered_results)

print('Total no. of capacitors found =',result.products_count)
print('No. of results after filter =', len(filtered_results))