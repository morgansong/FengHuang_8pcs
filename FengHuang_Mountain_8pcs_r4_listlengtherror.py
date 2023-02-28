#!/usr/bin/python 
#coding: utf-8
from Driver_Sensors import SFA3x, I2C_Handler,Singleshot_dart_WZS,Singleshot_cubic_CB
import RPi.GPIO as GPIO
from tkinter import *
import numpy as np
import datetime
import threading
import time
import os
import serial
from tkinter import filedialog 
import ast




print("setup GPIO")
# pinReset = 18 #pin12 - BCM18
pinReset = 24 #pin18 - BCM24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinReset, GPIO.OUT)



##Global parameters defination
data_raw_64 = ['n.c']*8  # the value of the output of all ports, in case there is no 64 data for example 1 sensor is not connected 
data_location = [] # record all the location where is data
color_64 = ["green"]*8  # the value of all 64pcs units
string_64 = [] #list of all 64pcs StringVar()
label_64 = [] #list of all 64pcs labels
#label_64_up = [] #list of all 64pcs labels
#label_64_down = [] #list of all 64pcs labels
SN_64 = [] #list the SN of all 64pcs sensor
SN_diff = [] #list of how many different SN of connected sensors
#Location_SameSN = [] #list of location, same SN in one list, data format: [[], [], []].....




class ReadMeasurement_SFA3x():
    def __init__(self):
        self.address_TCA9548 = [0x77]
        # self.address_TCA9548 = [0x77]
        self.My_Handler = I2C_Handler.I2C_Handler()
        
        self.SFA3x_handler = SFA3x.SFA3x()
        
        self.now = datetime.datetime.now()
        self.filename = r'/home/pi/DataLog/FengHuang_{}_{}_{}_{}_{}_{}.json'.format(self.now.year, str(self.now.month).zfill(2),str(self.now.day).zfill(2),str(self.now.hour).zfill(2),str(self.now.minute).zfill(2),str(self.now.second).zfill(2))
        
        self.Flag_SN = True
        
        self.uart = serial.Serial(port="/dev/ttyAMA0", baudrate=9600)
        self.uart_Datasend = {}
        self.uart_SNList = {'flag':'serialnumber'}
        
        
        
        self.DeviceName_list = []
        self.UART_list = []
        self.num_usbDevice = 0
        self.loc = []
        
        port_list = ["/dev/device2", "/dev/device3","/dev/device4", "/dev/device5"]
        
        #start Measurement for USB devices - competitors
        #start Measurement
        for k in range(len(port_list)):
            # print(port_list[k])
            try:
                Prosense = Singleshot_dart_WZS.dart_WZS(port_list[k])
                
                Check = False
                for i in range(3):
                    time.sleep(2)
                    read = Prosense.get_new_measurements()
                    # print('read:',read)
                    if read:
                        Check = True
                        break
                    else:
                        Check = False
                        
                # print('Check1:',Check)
                if Check:
                    print("has found Prosense at ",port_list[k])
                    self.num_usbDevice = self.num_usbDevice + 1
                    self.DeviceName_list.append('Prosense')
                    self.UART_list.append(Prosense)
                    self.uart_SNList[str(64+k)] = 'Prosense'
                    self.loc.append(64+k)
                else:
                    Prosense.close()
                    
                    cubic = Singleshot_cubic_CB.CubicCBHCHO(port_list[k])
                    
                    Check = False
                    for i in range(3):
                        time.sleep(2)
                        read = cubic.get_new_measurements()
                        # print('read:',read)
                        if read:
                            Check = True
                            break
                        else:
                            Check = False
                            
                    # print('Check2:',Check)
                    if Check:
                        print("has found cubic at ",port_list[k])
                        self.num_usbDevice = self.num_usbDevice + 1
                        self.DeviceName_list.append('Cubic')
                        self.UART_list.append(cubic)
                        self.uart_SNList[str(64+k)] = 'Cubic'
                        self.loc.append(64+k)
                        
            except Exception as e:
                print(e)
                print(port_list[k], " has no device")
        
        
        try: 
            os.mkdir(r"/home/pi/DataLog")
        except Exception as e:
            print("build Failed: ", e)
        
        self.Remove_OldFile_1week()
        
        # self.Start_Measurement()
        
    def Remove_OldFile_1week(self):
        ###del the file old than 1weeks
        allFiles = os.listdir(r"/home/pi/DataLog")
        
        for i in range(len(allFiles)):
            if "FengHuang_" in allFiles[i] and ".json" in allFiles[i]:
                inte  = allFiles[i].replace('FengHuang_',"").replace('.json',"").replace('{',"").replace('}',"").split('_')
                
                numberDate = datetime.datetime.strptime("{}-{}-{} {}:{}:{}".format(inte[0],inte[1],inte[2],inte[3],inte[4],inte[5]), "%Y-%m-%d %H:%M:%S")
                if numberDate + datetime.timedelta(days =7) < self.now:  #if older than 7days, delete it
                    # print('time now:', self.now)
                    # print("numberDate:" , numberDate)
                    os.remove(r"/home/pi/DataLog"+'/'+allFiles[i])
                
    def Write_toFile(self, data):
        with open(self.filename, 'a+') as f: 
            f.write(str(data)+'\r\n')
                
    def Start_Measurement(self):
        global SN_64
        SN_64 = []
        ##start the measurement for all sensors
        for kk, address in enumerate(self.address_TCA9548): 
            for channel in range(8):
                
                ## try-except is nessary for there is missing  TCA9845
                try: 
                    self.OpenChannel_TCA9548(address, channel)
                    # print(address, channel)
                    # time.sleep(0.1)
                except Exception as e: 
                    print("write OpenChannel_TCA9548 channel error")
                    # print(e) 
                    pass
                
                # self.SFA3x_handler.SFA3x_start_continuous_measurement()
                # print('SFA3x_start_continuous_measurement')
                # time.sleep(0.01)
                try:
                    self.SFA3x_handler.SFA3x_stop_continuous_measurement()
                    time.sleep(0.01) #delay >5ms very important
                    # print('SFA3x_start_continuous_measurement 1: #',kk*8+channel,self.Flag_SN)
                    # if self.Flag_SN:
                    # self.Write_toFile('#port'+str(kk*8+channel)+' ' +self.SFA3x_handler.SFA3x_SN_Read())
                    
                    sn = self.SFA3x_handler.SFA3x_SN_Read()

                    sn = sn.strip(b'\x00'.decode())    #filter NULL empty string
                    SN_64.append(sn[0:4])
                    
                    # print(sn)
                    self.uart_SNList[str(kk*8+channel)] =  'port'+str(kk*8+channel+1)+'_'+sn
                    
                    self.Write_toFile('#port'+str(kk*8+channel+1)+' ' +sn)

                    self.SFA3x_handler.SFA3x_start_continuous_measurement() 
                    print('SFA3x_start_continuous_measurement 1')


                except Exception as e:
                    # print('1',e,kk*8+channel) 
                    pass
                        
                        
            
    def UpdateValues(self):
        global data_raw_64,data_location
        
        data_raw_64 = [] #everytime need renew the data
        data_location = [] #everytime need renew the data
        
        dataJson = {}
        self.uart_Datasend = {}
        
        self.uart_Datasend ['flag']='data'
        
        dataJson['timestamp']=round(time.time(),1)
        self.uart_Datasend ['timestamp']=round(time.time(),1)
        
        for kk, address in enumerate(self.address_TCA9548): 
            for channel in range(8):
                # print(address, channel)
                
                ## try-except is nessary for there is missing  TCA9845
                try: 
                    self.OpenChannel_TCA9548(address, channel)
                    # time.sleep(0.1)
                except Exception as e: 
                    # print("write channel error")
                    # print(e)
                    pass
                
                try: 
                    read = self.SFA3x_handler.SFA3x_ReadMeasurement()
                    # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()), read)
                    
                    if len(read)==3:
                        data_raw_64.append(round(read[0],1)) #first data is HCHO
                        data_location.append(kk*8+channel) #remember the location where has data
                        
                        dataJson[str(kk*8+channel+1)] = read
                        self.uart_Datasend[str(kk*8+channel)] = read
                except Exception as e:
                    # print(e)
                    pass
                    
        data = {}
        for i in range(len(self.UART_list)):
            try:
                result_dict = self.UART_list[i].get_new_measurements()
                
                # print(result_dict)
                
                if self.DeviceName_list[i] == 'Prosense':
                    if result_dict:
                        data[str(self.loc[i])] = [result_dict[1][1]]
                        
                if self.DeviceName_list[i] == 'Cubic':
                    if result_dict:
                        data[str(self.loc[i])] = [result_dict[0][1],result_dict[4][1],result_dict[3][1]]
            except Exception as e:
                print(e)
                
        if len(data) == self.num_usbDevice and self.num_usbDevice>0:
            # print(data)
            dataJson.update(data)
            self.uart_Datasend.update(data)
            
        self.Write_toFile(dataJson)
        print(self.uart_Datasend)
        print(self.uart_SNList)
        self.uart.write(str(str(self.uart_Datasend)+'\n').encode("gbk"))
        self.uart.write(str(str(self.uart_SNList)+'\n').encode("gbk"))
        
        # print('data_raw_64, data_location', data_raw_64, data_location)
                    
    def OpenChannel_TCA9548(self, address, channel):
        # print("set low")
        GPIO.output(pinReset, GPIO.LOW)
        time.sleep(0.01)
        
        # print("set high")
        GPIO.output(pinReset, GPIO.HIGH)
        
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
        
        self.My_Handler.write_data(address, [action]) #[] is essential
        
        
class GUI_DataShow():
    def __init__(self):
        
        self.ThreadingExample()
        
    def Datachange(self):
        
        S = ReadMeasurement_SFA3x() 

        while True:
            time.sleep(2)
            
            S.Start_Measurement()
            time.sleep(0.5)
                       
            S.Flag_SN = False
            
            S.UpdateValues()

            #test for algorithm
            # SN_64 = ['2123','2124','2125','2124','2123','2124','2125','2124','2125','2123','2125','2125']
            # data_location = [2, 4, 6, 10, 13, 15, 23, 21, 35, 36, 48, 58]
            # data_raw_64 = [150, 25, 67, 22, 88, 145, 53, 27, 0, 38, 84, 58]
            
            time.sleep(0.1)
            
            print("start to category the Serial Number")
            print('SN number:', SN_64, len(SN_64))
            print('data_raw_64:', data_raw_64, len(data_raw_64))
            print('data_location:', data_location, len(data_location))
            
            if(len(SN_64)==len(data_raw_64)): 
                # get SN list
                SN_diff = []
                for i in range(len(SN_64)):
                    if SN_64[i] not in SN_diff:
                        SN_diff.append(SN_64[i])

                Location_SameSN = []
                Data_SameSN = []
                for i in range(len(SN_diff)):
                    Location_SameSN.append([]) 
                    Data_SameSN.append([]) 

                #prepare the list with the same SN in the list
                for k in range(len(SN_diff)):
                    print('now checn SN: ', SN_diff[k])
                    for i in range(len(SN_64)): 
                        if SN_64[i] == SN_diff[k]: 
                            Location_SameSN[k].append(data_location[i])
                            Data_SameSN[k].append(data_raw_64[i])
                    print('This SN in locations: ', Location_SameSN[k])

                # print(data_show)
                print('how many different SN: ', SN_diff)
                print('what location of same SN(one SN one list): ', Location_SameSN)
                print('what output of same SN(one SN one list): ', Data_SameSN)

                # print(len(string_64),len(label_64_up),len(label_64),len(label_64_down))
                # string_64[35].set(100.2) #test label length - window twisted
                
                ##change the text display
                for kk in range(len(label_64)):
                    label_64[kk].configure(bg='white')
                    string_64[kk].set('n.c')
                    
                    for i in range(len(data_location)):
                        if kk == data_location[i]:
                            string_64[kk].set(data_raw_64[i])
                
                ##Change color display
                ##red = data is beyond +/-40% of mean, or +/-50ppb
                if len(data_location)>0: #avoid no any sensor connected 
                    for i in range(len(Location_SameSN)): 
                        middian = np.mean(Data_SameSN[i])
                        for k in range(len(Data_SameSN[i])):
                            if middian <=80:
                                # print('less 80---', Data_SameSN[i][k],middian)

                                if Data_SameSN[i][k] > middian-40 and Data_SameSN[i][k] < middian+40: 
                                    label_64[Location_SameSN[i][k]].configure(bg='lime')
                                else: 
                                    label_64[Location_SameSN[i][k]].configure(bg='red')
                            else: 
                                # print('over 80---', Data_SameSN[i][k],middian, middian*0.6, middian*1.4)

                                if Data_SameSN[i][k] > middian*0.5 and Data_SameSN[i][k] < middian*1.5: 
                                    label_64[Location_SameSN[i][k]].configure(bg='lime')
                                else: 
                                    label_64[Location_SameSN[i][k]].configure(bg='red')

                    ####below code is for version r10
                    # for i in range(len(data_raw_64)):
                    #     # print(data_location[i])
                    #     if middian > 100:
                    #         if data_raw_64[i]>middian*1.2 or data_raw_64[i] <middian*0.8:
                    #             print(round(middian*0.8,1),'---', round(middian*1.2,1),'---', data_raw_64[i])
                                
                    #             # label_64_up[data_location[i]].configure(bg='red')
                    #             label_64[data_location[i]].configure(bg='red')
                    #             # label_64_down[data_location[i]].configure(bg='red')
                    #         else:  
                    #             # label_64_up[data_location[i]].configure(bg='green')
                    #             label_64[data_location[i]].configure(bg='lime')
                    #             # label_64_down[data_location[i]].configure(bg='green')
                    #     else: 
                    #         if data_raw_64[i]>middian + 20 or data_raw_64[i] <middian - 20:
                    #             print(round(middian + 20,1),'---', round(middian - 20,1),'---', data_raw_64[i])
                                
                    #             # label_64_up[data_location[i]].configure(bg='red')
                    #             label_64[data_location[i]].configure(bg='red')
                    #             # label_64_down[data_location[i]].configure(bg='red')
                    #         else:  
                    #             # label_64_up[data_location[i]].configure(bg='green')
                    #             label_64[data_location[i]].configure(bg='lime')
                    #             # label_64_down[data_location[i]].configure(bg='green')
            # print('Change is done')
                
    def ThreadingExample(self):
            # print("thread starts")
            thread = threading.Thread(target=self.Datachange, args=())
            thread.daemon = True
            thread.start()
        
root = Tk()
root.attributes('-fullscreen', True)
# root.overrideredirect(True)  # 去除窗口边框

frameList_Row = []
frame_64 = []
##put 8 raw row 
frame = Frame(root)
frame.pack(fill='both', expand=True)

frameList_Row.append(frame)

##put 8 frame in each row
for j in range(len(frameList_Row)):
    for i in range(8):
        f = Frame(frameList_Row[j])
            
        f.pack(side='left',fill='both', expand=True)
        
        frame_64.append(f)
        
for i in range(len(frame_64)):
    if len(str(i+1))==1:
        Label(frame_64[i], text=" #0{}  ".format(i+1), bg='gray', relief='ridge').pack(fill='both', expand=True) #the blank is to freeze the GUI
    else:
        Label(frame_64[i], text=" #{}  ".format(i+1), bg='gray', relief='ridge').pack(fill='both', expand=True)
    
    # l1 = Label(frame_64[i], bg='green')
    # l1.pack(fill='both', expand=True) #just for UI
    
    my_string_var = StringVar()
    my_string_var.set(data_raw_64[i])
    l = Label(frame_64[i], textvariable= my_string_var,font=(30), relief='ridge', bg='white') #display of values
    l.pack(fill='both', expand=True)
    
    # l2 = Label(frame_64[i], bg='green')
    # l2.pack(fill='both', expand=True) #just for UI
    
    string_64.append(my_string_var)
    # label_64_up.append(l1)
    label_64.append(l)
    # label_64_down.append(l2)
    
##Reading and update the value
GUI_DataShow()


root.mainloop()



##Test sensor without GUI interface
# S = ReadMeasurement_SFA3x()

# while True: 
    # time.sleep(1)
    # S.UpdateValues()
    # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),str(data_raw_64).replace("[","").replace("]",""))



