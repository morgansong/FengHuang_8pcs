#!/usr/bin/python 
#coding: utf-8
import os
import time
import RPi.GPIO as GPIO
import datetime
from Driver_Sensors import SHT3x, SHT4x, SCD4x, SEN4x, I2C_Handler, SFA3x



print("setup GPIO")
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)




class RPI_runSensors():
    def __init__(self):
        self.address_TCA9548 = 0x77
        self.My_Handler = I2C_Handler.I2C_Handler()
        
        self.SHT3x_handler = SHT3x.SHT3x()
        self.SHT4x_handler = SHT4x.SHT4x()
        self.SCD4x_handler = SCD4x.SCD4x()
        self.SEN4x_handler = SEN4x.SEN4x()
        self.SFA3x_handler = SFA3x.SFA3x()
        
        self.now = datetime.datetime.now()
        self.filename = r'/home/pi/DataLog/MultipleSensors_{}_{}_{}_{}_{}_{}.edf'.format(self.now.year, str(self.now.month).zfill(2),str(self.now.day).zfill(2),str(self.now.hour).zfill(2),str(self.now.minute).zfill(2),str(self.now.second).zfill(2))
        
        try: 
            os.mkdir(r"/home/pi/DataLog")
        except Exception as e:
            print("build Failed: ", e)

        self.channel = []
        self.sensor = []
        
        Channel_Sensors = [0,1,2,3,4,5,6,7]
        # Channel_Sensors = [3]
        
        for i in range(len(Channel_Sensors)):
            print("inChannel #{}, detecting".format(Channel_Sensors[i]))
            
            try: 
                time.sleep(1)
                self.OpenChannel_TCA9548(Channel_Sensors[i])
                time.sleep(1)
            except Exception as e: 
                print("write channel error")
                print(e) 
            
            ##SHT3x
            try:
                print("....try SHT30")
                self.SHT3x_handler.SHT3x_Read()
                
                print("channel {}:".format(str(Channel_Sensors[i])),"SHT30 was detected")
                self.channel.append(Channel_Sensors[i])
                self.sensor.append("SHT3x")
                    
            except Exception as e: 
                # print(e) 
                time.sleep(1) #delay if there is an error for next step
                
                ##SFA30
                try:
                    print("....try SFA3x") 
                    self.SFA3x_handler.SFA3x_stop_continuous_measurement()
                    time.sleep(0.01)  
                    self.SFA3x_handler.SFA3x_start_continuous_measurement()
                    time.sleep(0.01) 

                    # print('passed the mode setting') 

                    self.SFA3x_handler.SFA3x_ReadMeasurement() 
                
                    print("channel {}:".format(str(Channel_Sensors[i])),"SFA30 was detected")
                    self.channel.append(Channel_Sensors[i])
                    self.sensor.append("SFA3x") 
                    time.sleep(1) #delay if there is an error for next step
                    
                except:
                    # print(e) 
                    time.sleep(1) #delay if there is an error for next step
                    ##SHT4x
                    try:
                        print("....try SHT4x")
                        self.SHT4x_handler.SHT4x_Read()
                        
                        print("channel {}:".format(str(Channel_Sensors[i])),"SHT4x was detected")
                        self.channel.append(Channel_Sensors[i])
                        self.sensor.append("SHT4x")
                        
                    except Exception as e: 
                        # print(e) 
                        time.sleep(1) #delay if there is an error for next step
                    
                        ##SCD40
                        try:
                            print("....try SCD4x") 
                            self.SCD4x_handler.SCD4x_stop_measurement()
                            time.sleep(0.6) #delay >500ms 
                            self.SCD4x_handler.SCD4x_start_periodic_measurement() 
                            time.sleep(5) 
                            self.SCD4x_handler.SCD4x_ReadMeasurement() 
                        
                            print("channel {}:".format(str(Channel_Sensors[i])),"SCD40 was detected")
                            self.channel.append(Channel_Sensors[i])
                            self.sensor.append("SCD4x") 
                        except:
                            # print(e) 
                            time.sleep(1) #delay if there is an error for next step
                            
                            ##SEN44
                            try: 
                                print("....try SEN44")
                                self.SEN4x_handler.SEN44_stop_measurement()
                                time.sleep(0.05) #delay >20ms
                                self.SEN4x_handler.SEN44_start_measurement()
                                time.sleep(0.01) 
                                
                            except:
                                pass
                                
                            try:
                                self.SEN4x_handler.SEN44_ReadMeasurement() 
                                
                                print("channel {}:".format(str(Channel_Sensors[i])),"SEN44 was detected")
                                self.channel.append(Channel_Sensors[i])
                                self.sensor.append("SEN44")
                            except: 
                                # print(e) 
                                time.sleep(1) #delay if there is an error for next step
                                
        colomn_title = "Epoch_UTC\tLocal_Date_Time"
        subscribe = "# Type=float64,Unit=s,Format=.1f\tType=string"
        
        for k in range(len(self.sensor)): 
            self.OpenChannel_TCA9548(self.channel[k])
            
            if "SHT3" in self.sensor[k]:
                sn = self.SHT3x_handler.SHT3x_SN_Read()
                print(sn)
                colomn_title = colomn_title+"\tT_SHT3x_{}\t".format(sn)+"RH_SHT3x_{}".format(sn)
                subscribe = subscribe + "\tSensorName=SHT3x,Unit=°C,Sensor_Serial_Number={},Signal=Temperature\tSensorName=SHT3x,Unit=%RH,Sensor_Serial_Number={},Signal=Relative_Humidity".format(sn,sn)
                
            if "SHT4" in self.sensor[k]:
                sn = self.SHT4x_handler.SHT4x_SN_Read()
                print(sn)
                colomn_title = colomn_title+"\tT_SHT4x_{}\t".format(sn)+"RH_SHT4x_{}".format(sn)
                subscribe = subscribe + "\tSensorName=SHT4x,Unit=°C,Sensor_Serial_Number={},Signal=Temperature\tSensorName=SHT4x,Unit=%RH,Sensor_Serial_Number={},Signal=Relative_Humidity".format(sn,sn)
                
            if "SCD4" in self.sensor[k]:
                sn = self.SCD4x_handler.SCD4x_SN_Read()
                print(sn)
                colomn_title = colomn_title+"\tCO2_SCD4x_{}\t".format(sn)+"T_SCD4x_{}\t".format(sn)+"RH_SCD4x_{}".format(sn)
                subscribe = subscribe + "\tSensorName=SCD4x,Unit=ppm,Sensor_Serial_Number={},Signal=CO2\tSensorName=SCD4x,Unit=°C,Sensor_Serial_Number={},Signal=Temperature\tSensorName=SCD4x,Unit=%RH,Sensor_Serial_Number={},Signal=Relative_Humidity".format(sn,sn,sn)
            
            if "SEN44" in self.sensor[k]:
                sn = self.SEN4x_handler.SEN44_SN_Read()
                print(sn)
                colomn_title = colomn_title+"\tpm2p5_SEN44_{}\t".format(sn)+"voc_SEN44_{}\t".format(sn)+"T_SEN44_{}\t".format(sn)+"RH_SEN44_{}\t".format(sn)+"voc_raw_SEN44_{}\t".format(sn)+"T_uncomp_SEN44_{}\t".format(sn)+"RH_uncomp_SEN44_{}".format(sn)
                subscribe = subscribe + "\tSensorName=SEN44,Unit=ug/m3,Sensor_Serial_Number={},Signal=pm2p5\tSensorName=SEN44,Unit=index,Sensor_Serial_Number={},Signal=voc\tSensorName=SEN44,Unit=°C,Sensor_Serial_Number={},Signal=Temperature\tSensorName=SEN44,Unit=%RH,Sensor_Serial_Number={},Signal=Relative_Humidity\tSensorName=SEN44,Unit=ticks,Sensor_Serial_Number={},Signal=voc_raw\tSensorName=SEN44,Unit=°C,Sensor_Serial_Number={},Signal=Temperature_uncomp\tSensorName=SEN44,Unit=%RH,Sensor_Serial_Number={},Signal=Relative_Humidity_uncomp".format(sn,sn,sn,sn,sn,sn,sn)
            
        with open(self.filename, 'a+') as f: 
            f.write("#SensorsChannel = 1 is not designed to use"+"\r\n")
            
            f.write("#SensorsConnectedatChannel = "+str(self.channel).replace("[","").replace("]","")+"\r\n")
            
        with open(self.filename, 'a+') as f: 
            f.write(subscribe+"\r\n")
            
        with open(self.filename, 'a+') as f: 
            f.write(colomn_title+"\r\n")
            
        time.sleep(1)
        print(self.sensor)
        print(self.channel)
        
    def OpenChannel_TCA9548(self, channel):
        
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
        
        self.My_Handler.write_data(self.address_TCA9548, [action]) #[] is essential
        
        # GPIO.cleanup()
        
        # time.sleep(0.8)
        
        
        
    def Logging(self):
        print("sensor list is: ", self.sensor)
        print("channel sensor list is: ", self.channel)
        
        if len(self.sensor)>0:
            print("loop stars")
            while True:
                num_SCD40 = 1 #for delaying 5seconds
                SensorCount = 0 
                
                new_data = [] 
                for i in range(len(self.channel)):
                    self.OpenChannel_TCA9548(self.channel[i])
                    
                    try: 
                        if "SHT3" in self.sensor[i]:
                            new_data = new_data + self.SHT3x_handler.SHT3x_Read()
                            SensorCount = SensorCount + 1 
                            
                        if "SHT4" in self.sensor[i]:
                            new_data = new_data + self.SHT4x_handler.SHT4x_Read()
                            SensorCount = SensorCount + 1 
                            
                        if "SCD4" in self.sensor[i]:
                            new_data = new_data + self.SCD4x_handler.SCD4x_ReadMeasurement()
                            
                            num_SCD40 = num_SCD40 +1 
                            
                            SensorCount = SensorCount + 1 
                            
                            
                        if "SEN4" in self.sensor[i]:
                            new_data = new_data + self.SEN4x_handler.SEN44_ReadMeasurement()
                            SensorCount = SensorCount + 1

                        if "SFA3" in self.sensor[i]:
                            new_data = new_data + self.SFA3x_handler.SFA3x_ReadMeasurement()
                            SensorCount = SensorCount + 1 
                            
                    except: 
                        print("channel {} sensor is disconnected".format(str(self.channel[i])))

                # print(new_data)
                # print('SensorCount ', SensorCount, len(self.sensor))

                if SensorCount == len(self.sensor):
                    print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),str(new_data).replace("[","").replace("]",""))
                    
                    with open(self.filename, "a+") as f: 
                        Local_Date_Time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
                        Epoch_UTC = time.mktime(time.strptime(Local_Date_Time, "%Y-%m-%dT%H:%M:%S"))
                        
                        f.write(str(Epoch_UTC)+"\t"+Local_Date_Time+"\t"+str(new_data).replace("[","").replace("]","").replace(" ","").replace(",","\t")+"\r\n")
                
                if num_SCD40>1: # only delay once if more SCD40
                    time.sleep(5-(len(self.sensor))*0.12) #interval of 5 seconds - Channel_Sensors 5seconds for SCD40
                else: 
                    time.sleep(1-(len(self.sensor))*0.12) # interval of 1 second
        else: 
            print("This is no sensor detected")


logger = RPI_runSensors()
logger.Logging()




