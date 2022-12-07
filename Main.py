import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest
from py3dbp import Packer, Bin, Item     #used for optimal location  
import numpy as np
import math as m

os.environ['DIGIKEY_CLIENT_ID'] = 'lapy0mAhGhAIlaOjNxBrAtrGBKNzF6b0'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'jUwqrqjz87HxqiYf'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Dropbox\\Msc Space Engineering\\Q2\\(AE4S10) Microsat Engineering\\API Digikey tryout'

# Query product number
dkpn = '296-6501-1-ND'
part = digikey.product_details(dkpn)

# Search for parts 
search_request = KeywordSearchRequest(keywords='CRCW080510K0FKEA', record_count=10)
result = digikey.keyword_search(body=search_request)

print(result)

V_1 = 4.2   #initial voltage
V_2 = 3     #final voltage

# Capacitor data PBLC-3R8/220MA2
C = 220 #F
D = 16
L = 25
V_n = 3.8  #nominal voltage

# Battery case
H = 40
W = 33.8
L = 35

def C_req(V_1, V_2):
    E = 600e-3 * V_n * 3600
    return 2*E/(V_1**2 - V_2**2)
    
def pos_config(D, L, C, C_req):
    V_available = H*W*L  #mm3
    V = (np.pi*L*D**2)/4    #mm3
    n_cap = m.ceil(C_req(V_1,V_2)/C)
    if V_available<(V*n_cap):
        print('Capacitor provided too large')
    C_act = n_cap*C
    return C_act, n_cap

C_act, n_cap = pos_config(D, L, C, C_req)
print('C_act =', C_act, 'F')
print('n_cap =', n_cap)

# my_bin = Bin(name, width, height, depth, max_weight)
# my_item = Item(name, width, height, depth, weight)
packer = Packer()
packer.add_bin(Bin('Battery case', H, W, L, 999999))

for i in range(n_cap):
    packer.add_item(Item('Capacitor'+str(i+1), D, L, D, 1+i))
    
packer.pack()
for b in packer.bins:
    print(b.string())
    print("\n FITTED ITEMS:")
    for item in b.items:
        print(item.string())
    print("\n UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print(item.string())