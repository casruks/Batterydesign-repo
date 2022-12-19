import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest, ParametricFilter
from py3dbp import Packer, Bin, Item     #used for optimal location  
import numpy as np
import math as m
import requests
import json


os.environ['DIGIKEY_CLIENT_ID'] = 'rGRVvZwhTTBu8LZrov7v6CbEoAlbuaRL'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'CEIUIRl5vQ2m4pV6'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Documents\\GitHub\\Batterydesign-repo\\tmp'

# Query product number
# dkpn = '2085-PBLC-3R8/220MA2-ND'
# part = digikey.product_details(dkpn, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')

# Capacitor data
# part.parameters[1].value
# C = part.parameters[12].value
# D = part.parameters[3].value
# L = part.parameters[10].value
# V_n = part.parameters[13].value
# Operating_temp = part.parameters[5].value

search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=20, record_start_position=0, filters=ParametricFilter(parameter_id=46,value_id='21491'))
result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')
#result.products[nth product]
# print(result.products[19].parameters)
# g = result.products[19].parameters.index('{')
print(result.products)

# print(C,D,L,V_n,Operating_temp)
# resultlst = []
# x = int(2104/8)  #2104
# y = 8
# for i in range(1): #54(x) times 39(y) results = 2106
#     search_request = KeywordSearchRequest(keywords='Electric Double Layer Capacitors (EDLC), Supercapacitors', record_count=y, record_start_position=0+i*y, filters=ParametricFilter(parameter_id=2049,value_id='Capacitance'))
#     result = digikey.keyword_search(body=search_request, x_digikey_locale_site='NL', x_digikey_locale_currency='EUR')
#     print(str(i) + '/'+str(x)+' done..')
#     resultlst.append(result)
#     with open('Results\\result' + str(i) + '.txt', 'w') as f:
#         f.write(str(result))
          

# with open('result.txt', 'w') as f:
#     for i in range(len(resultlst)):
#         if i == 0:
#             f.write(str(resultlst[i]))
#         else:
#             f.write('\n'+'###'*24 + '\n' + str(resultlst[i]))
            
# for i in range(len(resultlst)):
#     with open('Results\\result' + str(i) + '.txt', 'w') as f:
#         f.write(str(resultlst[i]))
      

# V_1 = 4.2   #initial voltage
# V_2 = 3     #final voltage

# # Capacitor data PBLC-3R8/220MA2
# C = 220 #F
# D = 16
# L = 25
# V_n = 3.8  #nominal voltage

# # Battery case
# H = 40
# W = 33.8
# L = 35

# def C_req(V_1, V_2):
#     E = 600e-3 * V_n * 3600
#     return 2*E/(V_1**2 - V_2**2)
    
# def pos_config(D, L, C, C_req):
#     V_available = H*W*L  #mm3
#     V = (np.pi*L*D**2)/4    #mm3
#     n_cap = m.ceil(C_req(V_1,V_2)/C)
#     if V_available<(V*n_cap):
#         print('Capacitor provided too large')
#     C_act = n_cap*C
#     return C_act, n_cap

# C_act, n_cap = pos_config(D, L, C, C_req)
# print('C_act =', C_act, 'F')
# print('n_cap =', n_cap)

# my_bin = Bin(name, width, height, depth, max_weight)
# my_item = Item(name, width, height, depth, weight)
# packer = Packer()
# packer.add_bin(Bin('Battery case', H, W, L, 999999))

# for i in range(n_cap):
#     packer.add_item(Item('Capacitor'+str(i+1), D, L, D, 1+i))
    
# packer.pack()
# for b in packer.bins:
#     print(b.string())
#     print("\n FITTED ITEMS:")
#     for item in b.items:
#         print(item.string())
#     print("\n UNFITTED ITEMS:")
#     for item in b.unfitted_items:
#         print(item.string())
