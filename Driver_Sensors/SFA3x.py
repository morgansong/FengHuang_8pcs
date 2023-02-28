from Driver_Sensors import I2C_Handler
# import I2C_Handler
import time

class SFA3x():
    def __init__(self):
        # print("SFA3x") 
        self.address_SFA3x = 0x5D
        self.My_Handler = I2C_Handler.I2C_Handler()
        
    def SFA3x_SN_Read(self):
        try:
            self.My_Handler.write_data(self.address_SFA3x,[0x01,0x04])
            time.sleep(0.01) #delay >5ms very important
        except:
            # print("SFA3x already stops period measurement")
            pass
            
        self.My_Handler.write_data(self.address_SFA3x,[0xD0,0x60])
        
        time.sleep(0.01) #delay >5ms very important
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SFA3x, 48)
        
        try:
            self.My_Handler.write_data(self.address_SFA3x,[0x00,0x06])
        except:
            # print("SFA3x already starts period measurement")
            pass
        
        SerialNumber = ''
        for i in range(len(Data_Get)):
            if (i+1)%3!=0:
                SerialNumber = SerialNumber + chr(Data_Get[i])
        
        return SerialNumber
        
    def SFA3x_start_continuous_measurement(self):
        self.My_Handler.write_data(self.address_SFA3x,[0x00,0x06])
        
    def SFA3x_stop_continuous_measurement(self):
        self.My_Handler.write_data(self.address_SFA3x,[0x01,0x04])
        
    def SFA3x_ReadMeasurement(self):
        # print("SFA3x 1")
        self.My_Handler.write_data(self.address_SFA3x,[0x03,0x27])
        
        time.sleep(0.01)
        # print("SFA3x 2")
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SFA3x, 9)
        
        HCHO =(int(hex(Data_Get[0]<<8),16)+int(hex(Data_Get[1]),16))/5.0
        humi =(int(hex(Data_Get[3]<<8),16)+int(hex(Data_Get[4]),16))/100.0
        temp =(int(hex(Data_Get[6]<<8),16)+int(hex(Data_Get[7]),16))/200.0
        
        # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),"SFA3x HCHO: {}, humidity: {}, temperature: {}".format(round(HCHO,2),round(humi,2),round(temp,2)))
        
        return [round(HCHO,2),round(humi,2),round(temp,2)]