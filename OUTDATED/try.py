# import json

# # Data to be written
# with open('json_data.json') as json_file:
#     dictionary = json.load(json_file)
 
# # Serializing json
# json_object = json.dumps(dictionary, indent=10)

# # Writing to sample.json
# with open("sample.json", "w") as outfile:
# 	outfile.write(json_object)

a = '6 F'
b = '1000 mF'

def ExtractData_C(sampleStr):
    if len(sampleStr.strip(' F')) == len(sampleStr.strip(' mF')):
        C = float(sampleStr.strip(' F'))
    else:
        C = float(sampleStr.strip(' mF'))/1000
    return C
        
print(ExtractData_C(a))
print(ExtractData_C(b))
