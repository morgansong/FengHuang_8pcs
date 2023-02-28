import RPi.GPIO as GPIO
import time
import SFA3x_TCA9845, I2C_Handler


##setup GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

time.sleep(1)

My_Handler = I2C_Handler.I2C_Handler()




##Setup TCA9845
address_TCA9548 = 0x77
channel = 0 


def OpenChannel_TCA9548(channel):
    
    # print("set low")
    GPIO.output(18, GPIO.LOW)
    time.sleep(0.1)
    
    # print("set high")
    GPIO.output(18, GPIO.HIGH)
   
    # print("cleanup")
    # GPIO.cleanup()
    
    # time.sleep(1.0)
    
    if (channel == 0):
        action = 0x01
    elif (channel == 1):
        action = 0x02
    elif (channel == 2):
        action = 0x04
    elif (channel == 3):
        action = 0x08
    elif (channel == 4):
        action = 0x10
    elif (channel == 5):
        action = 0x20
    elif (channel == 6):
        action = 0x40
    elif (channel == 7):
        action = 0x80
    else:
        action = 0x00
    
    My_Handler.write_data(address_TCA9548, [action]) #[] is essential




##open TCA9845 channel
OpenChannel_TCA9548(channel)

print('open TCA9845 channel')



SFA30_handler = SFA3x_TCA9845.SFA3x()


SFA30_handler.SFA3x_stop_continuous_measurement()
time.sleep(1)
SFA30_handler.SFA3x_start_continuous_measurement()
print('SFA3x_start_continuous_measurement')



while True:
    time.sleep(1) 
    new_data = SFA30_handler.SFA3x_ReadMeasurement() 
    time.sleep(1) 
    print(SFA30_handler.SFA3x_SN_Read())
    print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),str(new_data).replace("[","").replace("]",""))
    
    
    
    
    