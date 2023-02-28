import RPi.GPIO as GPIO
import time, os




pinReset = 21 #pin40 - BCM21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pinReset, GPIO.IN)


print('soft started: ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print('connect pin40 to GND')
# print('connect pin40 to 3.3v')

print('scripter is running')

count_low = 0
count_high = 0

while True:
    curInput = GPIO.input(pinReset)
    
    if curInput == 0:
        count_low = count_low + 1
        if count_low > 10: 
            count_high=0
    else: 
        count_high = count_high + 1
        if count_high > 10: 
            count_low=0
    
    print(curInput,'=== ', count_low,count_high)
    
    
    if count_low>=5 and count_high>=5 and curInput==0: 
        print('i got you, restarting')
        os.system("sudo reboot")
    
    
    time.sleep(1)








