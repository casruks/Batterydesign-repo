op2=>operation: import os
op4=>operation: import re
op6=>operation: import csv
op8=>operation: import time
op10=>operation: import digikey
op12=>operation: import math as m
op14=>operation: from digikey.v3.productinformation import KeywordSearchRequest
op16=>operation: from py3dbp import Packer, Bin, Item
op18=>operation: H_box = 42
op20=>operation: W_box = 34
op22=>operation: L_box = 34
op24=>operation: V_box = ((H_box * W_box) * L_box)
op26=>operation: Ah = 0.6
op28=>operation: V = 3.7
op30=>operation: s = 3600
op32=>operation: E = ((Ah * V) * s)
op34=>operation: os.environ['DIGIKEY_CLIENT_ID'] = 'KAnyJA8SFWx30kxCstFM6cAKNF5HFSCx'
op36=>operation: os.environ['DIGIKEY_CLIENT_SECRET'] = 'AmnYGhMUfE08wm9M'
op38=>operation: os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
op40=>operation: os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\casru\\Documents\\GitHub\\Batterydesign-repo\\tmp'
st43=>start: start findIndex
io45=>inputoutput: input: i
op48=>operation: (i_Cint, i_Dint, i_Hint, i_Vint) = ('x' for i in range(4))
cond51=>condition: for n in range(len(result.products[i].parameters))
cond105=>condition: if (result.products[i].parameters[n].parameter_id == 2049)
op109=>operation: i_Cint = n
cond117=>condition: if (result.products[i].parameters[n].parameter_id == 46)
op121=>operation: i_Dint = n
cond129=>condition: if (result.products[i].parameters[n].parameter_id == 1500)
op133=>operation: i_Hint = n
cond141=>condition: if (result.products[i].parameters[n].parameter_id == 2079)
op145=>operation: i_Vint = n
op149=>operation: i_V = 'None found'
op137=>operation: i_H = 'None found'
op125=>operation: i_D = 'None found'
op113=>operation: i_C = 'None found'
cond155=>condition: if (i_Cint and i_Dint and i_Hint and (i_Vint != 'x'))
op159=>operation: i_C = i_Cint
op161=>operation: i_D = i_Dint
op163=>operation: i_H = i_Hint
op165=>operation: i_V = i_Vint
io173=>inputoutput: output:  (i_C, i_D, i_H, i_V)
e171=>end: end function return

op2->op4
op4->op6
op6->op8
op8->op10
op10->op12
op12->op14
op14->op16
op16->op18
op18->op20
op20->op22
op22->op24
op24->op26
op26->op28
op28->op30
op30->op32
op32->op34
op34->op36
op36->op38
op38->op40
op40->st43
st43->io45
io45->op48
op48->cond51
cond51(yes)->cond105
cond105(yes)->op109
op109->cond117
cond117(yes)->op121
op121->cond129
cond129(yes)->op133
op133->cond141
cond141(yes)->op145
op145->cond51
cond141(no)->op149
op149->cond51
cond129(no)->op137
op137->cond141
cond117(no)->op125
op125->cond129
cond105(no)->op113
op113->cond117
cond51(no)->cond155
cond155(yes)->op159
op159->op161
op161->op163
op163->op165
op165->io173
io173->e171
cond155(no)->io173