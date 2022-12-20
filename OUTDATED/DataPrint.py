import pickle

# load data received 
class MyClass():
    def __init__(self, param):
        self.param = param
        
def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)
        
obj = load_object("data.pickle")
# print(obj.param)
# print(isinstance(obj, MyClass))


L = obj.parameters[10].value
print(L)