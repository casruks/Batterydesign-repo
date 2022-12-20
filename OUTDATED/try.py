# import json

# # Data to be written
# with open('json_data.json') as json_file:
#     dictionary = json.load(json_file)
 
# # Serializing json
# json_object = json.dumps(dictionary, indent=10)

# # Writing to sample.json
# with open("sample.json", "w") as outfile:
# 	outfile.write(json_object)

# a = '6 F'
# b = '1000 mF'

# def ExtractData_C(sampleStr):
#     if len(sampleStr.strip(' F')) == len(sampleStr.strip(' mF')):
#         C = float(sampleStr.strip(' F'))
#     else:
#         C = float(sampleStr.strip(' mF'))/1000
#     return C
        
# print(ExtractData_C(a))
# print(ExtractData_C(b))
from py3dbp import Packer, Bin, Item 
import math as m
H_box = 42       #[mm]
W_box = 34      #[mm]
L_box = 34     #[mm]

C = 0.0115

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
        n_reqlst.append(n_req) 
        C_reqlst.append(C_req) 
        filtered_results.append(Clst)  
        filtered_results.append(Llst) 
        filtered_results.append(Vlst) 
        filtered_results.append(dkpnlst) 
        filtered_results.append(n_reqlst) 
        filtered_results.append(C_reqlst)