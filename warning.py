#import files still need to be implemented


#function to check if danger conditions are met and set warnings to true if they are
def warn(temp, humidity, rainfall):
    if temp > temp_threshold:
        tempwarning = True
    
    if humidity > high_humidity:
        humiditywarning = True
    if rainfall = True:
        rainfallwarning = True
    if humidity = 100:
        humidityDanger = True
     return tempwarning, humiditywarning, rainfallwarning, humidityDanger
 

#While loops to push warnings to flask if conditions are met
while tempwarning or humiditywarning:
           print("Amber")
           

while rainfallwarning or humidityDanger:
           print("Red")


