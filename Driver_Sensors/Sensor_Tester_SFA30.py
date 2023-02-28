import time
import SFA3x


SFA30_handler = SFA3x.SFA3x()


SFA30_handler.SFA3x_stop_continuous_measurement()
time.sleep(1)
SFA30_handler.SFA3x_start_continuous_measurement()



while True:
    time.sleep(1) 
    new_data = SFA30_handler.SFA3x_ReadMeasurement() 
    print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),str(new_data).replace("[","").replace("]",""))