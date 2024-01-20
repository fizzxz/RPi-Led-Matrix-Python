from USB_Temper.temper import Temper, USBList
import json
import time
t = Temper()

def init():
    global roomTemp
    roomTemp = "0.00°C"

def updateTempThread():
    global roomTemp
    while True:
        roomTemp = updateRoomTemp()     
        print("Updated shared value:", roomTemp)
        time.sleep(60)

def updateRoomTemp():
    usblist = USBList()
    t.usb_devices = usblist.get_usb_devices()
    result = json.dumps(t.read(), indent=2)

    dataResult = json.loads(result)
    # requires sudo password?
    # print(dataResult)
    # with open("./data.json", "w") as file:
    #     json.dump(result,file,indent=2)
    # with open("./data.json", "r") as file:
    #     rawData = file.read()
    
    thermometerData = dataResult
    roomTemp = str(thermometerData[0]["external temperature"])
    roomTemp = "%.2f" % float(roomTemp)
    roomTemp = roomTemp + "°C"
    return roomTemp