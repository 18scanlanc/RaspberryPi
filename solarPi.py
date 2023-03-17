import time
import RPi.GPIO as rpi
import json
from RPLCD import CharLCD



values = open("/home/bluecoat/Documents/solarPi/lightValues.json", "r")
values.close()




rpi.setmode(rpi.BOARD)
rpi.setwarnings(False)


xPins = [31, 33, 35, 37]
yPins = [29, 23, 21, 19]
arduinoPin = [12,16,18,22,24,26,32,36,38,40]
rButton = 8
bButton = 10
LCDPins = [11, 7, 5, 3]





lcd = CharLCD(pin_rs = 15, cols = 16, rows = 2,  pin_e = 13, pins_data = LCDPins, numbering_mode = rpi.BOARD)

time.sleep(1)
lcd.clear()
lcd.write_string('Loading...')



for pin in arduinoPin:
    rpi.setup(pin, rpi.IN)

lightPin = 12
rpi.setup(lightPin, rpi.IN)


for pin in xPins:
    rpi.setup(pin, rpi.OUT)
    rpi.output(pin, 0)
    
for pin in yPins:
    rpi.setup(pin, rpi.OUT)
    rpi.output(pin, 0)
    
    
rpi.setup(rButton, rpi.IN, pull_up_down = rpi.PUD_DOWN)
rpi.setup(bButton, rpi.IN, pull_up_down = rpi.PUD_DOWN)


    
    
seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1],
    ]


     

     
     
     
        

def turn(revs, direction, motorPins):
    if direction == -1:
        for i in range(revs):
            for halfstep in range(8):
                for pin in range(4):
                    rpi.output(motorPins[pin], seq[halfstep][pin])
                time.sleep(0.001)
    elif direction == 1:
        for i in range(revs):
            for halfstep in range(8):
                for pin in range(4):
                    rpi.output(motorPins[pin], seq[7 - halfstep][pin])
                time.sleep(0.001)
        


def convert(degrees):
    turns = degrees * (512/360)
    turns = round(turns,0)
    turns = int(turns)
    return turns

def convertToDeg(turns):
    degrees = turns * (360/512)
    degrees = round(degrees,1)
    degrees = float(degrees)
    return degrees





def measure():
    LI = readArduino(arduinoPin)
    print(LI)
    return LI



hours = 6
timeInterval = 5
testTime = 21600





currentAngle = 0
currentAngleX = 0
currentAngleY = 0


startingAngleX = 0
startingAngleY = 0








def main1():
    global values
    values = open("lightValues.json", "w")
    global currentAngle
    jsonData = {"data": []}
    for i in range(hours):
        hour = "hour " + str(i)
        hourData = {hour: []}
        for i in range(angles):
            lightIntensity = measure()
            angle = "Angle " + str(i)
            angleData = {angle: {"angleX": [], "lightIntensity": []}}    
            angleData[angle]["angleX"].append(currentAngle)
            angleData[angle]["lightIntensity"].append(lightIntensity)
            hourData[hour].append(angleData)
            
            
            turn(turnInterval, 1, xPins)
            currentAngle += turnInterval
            time.sleep(timeInterval)
        turn(turnInterval * angles, -1, xPins)
        time.sleep(timeInterval)
        jsonData["data"].append(hourData)

    json.dump(jsonData, values, indent = 4)
    
 
 
   
def main2():
    global values
    values = open("lightValues.json", "w")
    global currentAngleX
    global currentAngleY
    jsonData = {"data": []}
    for i in range(hours):
        hour = "hour " + str(i)
        hourData = {hour: []}
        for y in range (anglesY):
            for x in range(anglesX):
                lightIntensity = measure()
                angle = "Angle " + str(x) + "," + str(y) 
                angleData = {angle: {"angleX": [], "angleY": [], "lightIntensity": []}}    
                angleData[angle]["angleX"].append(currentAngleX)
                angleData[angle]["angleY"].append(currentAngleY)
                angleData[angle]["lightIntensity"].append(lightIntensity)
                hourData[hour].append(angleData)
                
                
                turn(turnIntervalX, 1, xPins)
                currentAngleX += turnIntervalX
                time.sleep(timeInterval)
                
            
            turn(turnIntervalX * anglesX, -1, xPins)
            currentAngleX -= turnIntervalX * anglesX
                
            turn(turnIntervalY, 1, yPins)
            currentAngleY += turnIntervalY
            
            time.sleep(timeInterval)
            
        turn(turnIntervalY * anglesY, -1, yPins)
        currentAngleY -= turnIntervalY * anglesY
        time.sleep(timeInterval)
        
        jsonData["data"].append(hourData)
    json.dump(jsonData, values, indent = 4)





def main3():
    global values
    values = open("lightValues.json", "w")
    global currentAngleX
    global currentAngleY
    jsonData = {"data": []}
    global optimums
    optimums = []
    
    for i in range(hours):
        hour = "hour " + str(i)
        hourData = {hour: []}
        for y in range (anglesY):
            for x in range(anglesX):
                lightIntensity = measure()
                angle = "Angle " + str(x) + "," + str(y) 
                angleData = {angle: {"angleX": [], "angleY": [], "lightIntensity": []}}    
                angleData[angle]["angleX"].append(currentAngleX)
                angleData[angle]["angleY"].append(currentAngleY)
                angleData[angle]["lightIntensity"].append(lightIntensity)
                hourData[hour].append(angleData)
                
                
                turn(turnIntervalX, 1, xPins)
                currentAngleX += turnIntervalX
                time.sleep(timeInterval)
                    
            turn(turnIntervalX * anglesX, -1, xPins)
            currentAngleX -= turnIntervalX * anglesX
                
            turn(turnIntervalY, 1, yPins)
            currentAngleY += turnIntervalY
            time.sleep(timeInterval)
            
        turn(turnIntervalY * anglesX, -1, yPins)
        currentAngleY -= turnIntervalY * anglesY
        time.sleep(timeInterval)
        
        jsonData["data"].append(hourData)
        
        highest = {"Angle -1,-1": {"angleX": [-1], "angleY": [-1], "lightIntensity": [0]}}
        highAngle = "Angle -1,-1"

       
        for a in range (anglesX * anglesY):
            
           
            if hourData[hour][a]["Angle " + str((a) % anglesX) + "," + str(a // anglesY)]["lightIntensity"][0] > highest[highAngle]["lightIntensity"][0]:
                highest = hourData[hour][a]
                highAngle = "Angle " + str((a) % anglesX) + "," + str(a // anglesY)
        
 
                
        optimum = [highAngle, highest[highAngle]["angleX"][0], highest[highAngle]["angleY"][0], highest[highAngle]["lightIntensity"][0]]
        print(optimum)
        optimums.append(optimum)
        lcd.clear()
        lcd.write_string("X: " + str(convertToDeg(optimum[1])) + "\n\r" + "Y: " + str(convertToDeg(optimum[2])))
            
        

        
        
        
    json.dump(optimums, values)
    
    
    
    

def calculate1():
    global values
    values.close()
    values = open("lightValues.json", "r")
    data = json.load(values)["data"]

    
    averages = []
    
    for i in range(angles):
        angleValues = []
        angle = "Angle " + str(i)
        for h in range(hours):
            hour = "hour " + str(h)
            angleValues.append(int(data[h][hour][i][angle]["lightIntensity"][0]))
        average = sum(angleValues) / hours
        averages.append([str(i), int(data[h][hour][i][angle]["angleX"][0]), average])
        
        
        
    highest = ["-1", 0, 0]
    for average in averages:
        if average[2] > highest[2]:
            highest = average
    return highest
        
        
        
def calculate2():
    global values                             

    
    
    values.close()
    values = open("lightValues.json", "r")
    data = json.load(values)["data"]

    
    averages = []
    
    for y in range(anglesY):
        for x in range(anglesX):
            angleValues = []
            angle = "Angle " + str(x) + "," + str(y)
            for h in range(hours):
                hour = "hour " + str(h)
                angleValues.append(int(data[h][hour][anglesY * y + x][angle]["lightIntensity"][0]))
            average = sum(angleValues) / hours
            averages.append([str(x) + "," + str(y), int(data[h][hour][anglesY * y + x][angle]["angleX"][0]),int(data[h][hour][anglesY * y + x][angle]["angleY"][0]) , average])
            
    highest = ["-1", 0, 0, 0]
    for average in averages:
        if average[3] > highest[3]:
            highest = average
    return highest


def calculate3():
    global values
    values.close()
    values = open("lightValues.json", "r")
    optimums = json.load(values)
    
    for optimum in optimums:
        print(optimum)
        lcd.clear()
        time.sleep(0.1)
        lcd.write_string("X: " + str(convertToDeg(optimum[1])) + "\n\r" + "Y: " + str(convertToDeg(optimum[2])))
        time.sleep(10)

    


def binaryToDenary(binaryVal):
    total = 0
    for i in range(10,0,-1):
        if binaryVal[10 - i] == 1:
            total += 2 ** (i - 1)
    return total







def readArduino(arduino_Pin):
    binLight = []
    for pin in arduino_Pin:
        intensityVal = rpi.input(pin)
        binLight.append(intensityVal)
    return binaryToDenary(binLight)
        
    
def runI():
    main3()
    values.close()
    

    
def runRS():
    main1()
    lcd.clear()
    lcd.write_string("X: " + str(convertToDeg(calculate1()[1])))
    
    
def runRP():
    main2()
    lcd.clear()
    lcd.write_string("X: " + str(convertToDeg(calculate2()[1])) + "\n\rY: " + str(convertToDeg(calculate2()[2])))
    

def setTimes():
    global sleeps1
    global sleeps2
    global sleeps3
    
    global turnTime1
    global turnTime1
    global turnTime3
    
    global difference1
    global difference2
    global difference3
    
    
    sleeps1 = angles*hours+hours
    sleeps2 = anglesX*anglesY*hours+anglesY*hours+hours
    sleeps3 = anglesX*anglesY*hours+anglesY*hours+hours

    turnTime1 = angles*hours*turnInterval*0.008 + hours*turnInterval*angles*0.008
    turnTime2 = anglesX*anglesY*hours*turnIntervalX*0.008 + anglesY*hours*turnIntervalY*0.008 + anglesY*hours*turnIntervalY*anglesY*0.008 + hours*turnIntervalY*anglesY*0.008 
    turnTime3 = anglesX*anglesY*hours*turnIntervalX*0.008 + anglesY*hours*turnIntervalY*0.008 + anglesY*hours*turnIntervalY*anglesY*0.008 + hours*turnIntervalY*anglesY*0.008 

    difference1 = turnTime1 / sleeps1
    difference2 = turnTime2 / sleeps2
    difference3 = turnTime3 / sleeps3



def modeSelect():
    
    time.sleep(2)
    done = False
    global timeInterval
    global startingAngleX
    global startingAngleY
    global turnIntervalX
    global turnIntervalY
    global anglesX
    global anglesY
    global currentAngleX
    global currentAngleY
    
    global angles
    global turnInterval
    
    angles = 0
    turnInterval = 0
    
    
    
    

    
    while done == False:
        
        isRan = False
        
        
        
        lcd.clear()
        lcd.write_string("Red: Residential" + "\n\r" + "Blue: Industrial")
        selection = "none"
        
        isRan = False
        
        
        while selection == "none":

            if rpi.input(rButton) == 1:
                selection = "R"
            elif rpi.input(bButton) == 1:
                selection = "I"
                
        time.sleep(2)
            
        if selection == "R":
            lcd.clear()
            lcd.write_string("Red: Standard\n\rBlue: Plus")
            while selection == "R":
                if rpi.input(rButton) == 1:
                    selection = "RS"
                elif rpi.input(bButton) == 1:
                    selection = "RP"
                    
        elif selection == "I":
            lcd.clear()
            lcd.write_string("Red: Optimise\n\rBlue: Output")
            while selection == "I":
                if rpi.input(rButton) == 1:
                    selection = "IOP"
                elif rpi.input(bButton) == 1:
                    selection = "IOU"
        
                  
        time.sleep(2)
                  
        
        lcd.clear()
        lcd.write_string("Red: Confirm\n\rBlue: Back")
                
                
        while isRan == False:
            if rpi.input(rButton) == 1:
                lcd.clear()
                lcd.write_string("Calculating...")
                if selection == "RS":
                    angles = 5
                    turnInterval = 20
                    anglesX = 0
                    turnIntervalX = 0
                    anglesY = 0
                    turnIntervalY = 0
                    setTimes()
                    timeInterval = testTime/sleeps1
                    timeInterval -= difference1
                    runRS()
                    isRan = True
                    done = True
                elif selection == "RP":
                    turnIntervalX = 2   #2 1.6deg
                    turnIntervalY = 2   #2 1.6deg
                    anglesX = 21        #21    
                    anglesY = 21        #21
                    setTimes()
                    timeInterval = testTime/sleeps2
                    timeInterval -= difference2
                    
                    startingAngleX = 43
                    startingAngleY = 107
                    turn(startingAngleX, 1, xPins)
                    turn(startingAngleY, 1, yPins)
                    currentAngleX += startingAngleX
                    currentAngleY += startingAngleY
                    
                    
                    
                    
                    runRP()
                    isRan = True
                    done = True
                    turn(startingAngleX, -1, xPins)
                    turn(startingAngleY, -1, yPins)
                    currentAngleX -= startingAngleX
                    currentAngleY -= startingAngleY
                elif selection == "IOP":
                    turnIntervalX = 16    #16 10deg
                    turnIntervalY = 16    #16 10deg
                    anglesX = 9           #9
                    anglesY = 9           #9
                    setTimes()
                    timeInterval = testTime/sleeps3
                    timeInterval -= difference3
                    
                    
                    startingAngleX = 0
                    startingAngleY = 0
                    turn(startingAngleX, 1, xPins)
                    turn(startingAngleY, 1, yPins)
                    currentAngleX += startingAngleX
                    currentAngleY += startingAngleY
                    
                    runI()
                    isRan = True
                    done = True
                    turn(startingAngleX, -1, xPins)
                    turn(startingAngleY, -1, yPins)
                    currentAngleX -= startingAngleX
                    currentAngleY -= startingAngleY
                elif selection == "IOU":
                    calculate3()
                    isRan = True
                    done = True
            
            elif rpi.input(bButton) == 1:
                isRan = True
                time.sleep(2)
                
    
        
                
       
            







modeSelect()
                


#turn(convert(180), -1, yPins)






print("done")










values.close()
rpi.cleanup()









