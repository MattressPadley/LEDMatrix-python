import os
from PIL import Image
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

def pixelMap(width, height, frame):

   pixelTarget = 0
   columnNum = 0
   mappedFrame = []

   for i in range(1, frame):

      #if PixTarget is too high go to the next row
      if pixelTarget == (columnNum + (LED_COUNT - (width - 1)) and (columnNum % 2) == 0):
         columnNum += 1
         pixelTarget += 1

      elif pixelTarget == columnNum and (columnNum % 2) != 0:
         columnNum += 1
         pixelTarget += 1

      else:

         #Odd Columns count up & Even count down
         if (columnNum % 2) == 0:
            pixelTarget += width

         else:
            pixelTarget -= width

         mappedFrame[pixelTarget] = frame[i]

   return mappedFrame


# Fill matrix with solid color
def fillAll(r, g, b):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Draw the animation at givien path
def drawAnim(path):

    frameNum = 0
    anim = []
    LEDnum = 1
    files = os.listdir('/home/pi/anim/' + path)

    for file in sorted(files):
        img = Image.open('/home/pi/anim/' + path + '/' + file)
        rgbImg = img.convert('RGB')
        imgWidth = img.size[0]
        imgHeight = img.size[1]
        frame = []


        for i in range(0, imgHeight):
            for j in range(0, imgWidth):
                xy = (j, i)
                px = rgbImg.getpixel(xy)
                frame.append(px)
        anim.append(frame)

    for frame in anim:
   
      mappedFrame = pixelMap(7, 7, frame)

      for i in mappedFrame:
         strip.setPixelColor(i, Color(r, g, b))

      strip.show()
      time.sleep(.10)

"""
def chase(speed, width, delta):
	
	for i in range(strip.numPixels()):
"""		
		
drawAnim('anim1')
	
