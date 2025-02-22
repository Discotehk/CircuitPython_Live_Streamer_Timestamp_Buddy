import board
import busio
import digitalio
import displayio
import terminalio
import time
import adafruit_displayio_ssd1306
from i2cdisplaybus import I2CDisplayBus
from digitalio import DigitalInOut
from adafruit_debouncer import Debouncer
from adafruit_display_text import label

#  Time setup
start = 0
start_time = time.time()
hour = "0{}".format((time.time() - start_time) // 3600)
minute = "0{}".format((time.time() - start_time) // 60 % 60)
second = "0{}".format((time.time() - start_time) % 60)
timestamp = 0

#  Display setup
displayio.release_displays()

i2c = busio.I2C(board.GP15, board.GP14)
display_bus = I2CDisplayBus(i2c, device_address=0x3c)

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)


# Make the display context
main_group = displayio.Group()
display.root_group = main_group

# create the label
font = terminalio.FONT
text1 = "{}:{}:{}".format(hour, minute, second)
text2 = "{}:{}:{}".format(hour, minute, second)

text_label1 = label.Label(font, text=text1, scale=3)
text_label2 = label.Label(font, text=text2, scale=3)

# set label position on the display
text_label1.anchor_point = (1, 0.5)
text_label1.anchored_position = (128, 16)
text_label2.anchor_point = (1, 0.5)
text_label2.anchored_position = (128, 48)

# add label to group that is showing on display
main_group.append(text_label1)
main_group.append(text_label2)

#  Button to pin assignments and debouncing
switch1 = DigitalInOut(board.GP18)
switch1.switch_to_input(pull=digitalio.Pull.UP)
deb_switch1 = Debouncer(switch1)

switch2 = DigitalInOut(board.GP19)
switch2.switch_to_input(pull=digitalio.Pull.UP)
deb_switch2 = Debouncer(switch2)

switch3 = DigitalInOut(board.GP20)
switch3.switch_to_input(pull=digitalio.Pull.UP)
deb_switch3 = Debouncer(switch3)

switch4 = DigitalInOut(board.GP21)
switch4.switch_to_input(pull=digitalio.Pull.UP)
deb_switch4 = Debouncer(switch4)

def timeupdate():
    global hour
    global minute
    global second
    if (time.time() - start_time) // 3600 <= 9:
        hour = "0{}".format((time.time() - start_time) // 3600)
    else:
        hour = (time.time() - start_time) // 3600
    if (time.time() - start_time) // 60 % 60 <= 0:
        minute = "0{}".format((time.time() - start_time) // 60 % 60)
    else:
        minute = (time.time() - start_time) // 60 % 60
        
    if (time.time() - start_time) % 60 <= 9:
        second = "0{}".format((time.time() - start_time) % 60)
    else:
        second = (time.time() - start_time) % 60    

while True:
    #  Start the stream and the time counter
    deb_switch1.update()
    if deb_switch1.fell:
        start = 1
        start_time = time.time()
        text_label1.text = "{}:{}:{}".format(hour, minute, second)
        print("key 1 press")
        
    deb_switch4.update()
    if deb_switch4.fell:
        start_time = time.time()
        timeupdate()
        text_label1.text = "{}:{}:{}".format(hour, minute, second)
        text_label2.text = "{}:{}:{}".format(hour, minute, second)
        print("key 4 press")
    
    while start == 1:
        timeupdate()
        text_label1.text = "{}:{}:{}".format(hour, minute, second)
    
        #  Stop the stream and reset the time counter
        deb_switch2.update()
        if deb_switch2.fell:
            start = 0
            with open("/Timestamps.txt", 'a') as f:
                f.write(str("Ended Stream @ {}:{}:{}\n".format(hour, minute, second)))
                f.close()
            print("key 2 press")

        #  Write current time to file
        deb_switch3.update()
        if deb_switch3.fell:
            timeupdate()
            text_label2.text = "{}:{}:{}".format(hour, minute, second)
            print(hour, minute, second, sep=":")
            with open("/Timestamps.txt", 'a') as f:
                f.write(str("{}:{}:{}\n".format(hour, minute, second)))
                f.close()
            print("key 3 press")
