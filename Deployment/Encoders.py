class encoding:
    
    def __init__(self):
        pass
    
    def lot_shape (self , input) :
        lot_map={
        'Irregular':0,
        "Moderately Irregular":1,
        'Slightly Irregular':2,
        'Regular':3
        }
        
        
        return input.map(lot_map)
    
    def neighborhood(self,encoder,input):
        return encoder.transform(input)
    
    def foundation_type(self,encoder,input):
        return encoder.transform(input)
    
    def basement_quality(self,input):
        
        basement_map = {
        "No Basement":-1,
        "Poor":0,
        "Fair":1,
        'Typical':2,
        'Good':3,
        'Excellent':4
        }
        
        return input.map(basement_map)
        
    def basement_exposure(self,input):
        base_expo = {
        "No Basement":-1,
        "No Exposure":0,
        "Mimimum Exposure":1,
        'Average Exposure':2,
        'Good Exposure':3
        }
        return input.map(base_expo)

    
    def garage_location(self,input):
        garage_loc = {
        "No Garage":-1,
        "Detached From Home":1,
        'Car Port':2,
        'Built-In':3,
        'Basement Garage':4,
        'Attached To Home':5,
        '2 Types':6
        }
        
        return input.map(garage_loc)
    
    def garage_finish(self,input):
        
        garage_fin = {
        "No Garage":-1,
        "Un Finished":0,
        'Rough Finished':1,
        'Finished':2,
        }   
        
        return input.map(garage_fin)
    