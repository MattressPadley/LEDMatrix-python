import pickle
import os
import time
from PIL import Image
from socket import *
from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_COUNT = 49        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

# Fill matrix with solid color
def fillMatrix(r, g, b):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Draw the animation at givien path
def drawAnim(path):

    frameNum = 0
    animRGB = []
    LEDnum = 1
    files = os.listdir(path)

    for file in sorted(files):
        img = Image.open(path + '/' + file)
        rgbImg = img.convert('RGB')
        imgWidth = img.size[0]
        imgHeight = img.size[1]
        frameRGB = []


        for i in range(0, imgHeight):
            for j in range(0, imgWidth):
                xy = (j, i)
                pxRGB = rgbImg.getpixel(xy)
                frameRGB.append(pxRGB)
        animRGB.append(frameRGB)

    for frame in animRGB:
        frameNum += 1
        print('Frame #' + str(frameNum))
        time.sleep(.10)

        pixelTarget = 0
        columnNum = 0

        for i in range(strip.numPixels()):

            g = frame[pixelTarget][0]
            r = frame[pixelTarget][1]
            b = frame[pixelTarget][2]

            strip.setPixelColor(i, Color(r, g, b))

            #print(str(i) + ' | ' + str(pixelTarget) + ' | ' + str(r) + str(g) + str(b))
                
            #if PixTarget is too high go to the next row
            if pixelTarget == (columnNum + 42) and (columnNum % 2) == 0:
                columnNum += 1
                pixelTarget += 1

            elif pixelTarget == columnNum and (columnNum % 2) != 0:
                columnNum += 1
                pixelTarget += 1
            
            else:
                #Odd Columns count up & Even count down
                if (columnNum % 2) == 0:
                    pixelTarget += 7

                else:
                    pixelTarget -= 7   
        strip.show()           

host = ""
port = 14000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

fillMatrix(1, 1, 1)
print("Waiting to receive messages...")

#Websocket Connection loop
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    rgb = pickle.loads(data)
    if rgb == "anim":
        loop = 0
        while True:
            loop += 1
            drawAnim('anim2')
            if loop > 5:
                break

    elif rgb == "exit":
        break
    else:         
        fillMatrix(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        print(rgb[0], rgb[1], rgb[2])



UDPSock.close()
os._exit(0)


