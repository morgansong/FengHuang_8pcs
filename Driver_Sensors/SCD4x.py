from Driver_Sensors import I2C_Handler
import time

class SCD4x():
    def __init__(self):
        # print("SCD4x") 
        self.address_SCD40 = 0x62
        self.My_Handler = I2C_Handler.I2C_Handler()
        
        
    def SCD4x_SN_Read(self):
        try:
            self.My_Handler.write_data(self.address_SCD40,[0x3f,0x86])
            time.sleep(1)
        except:
            print("SCD40 already stops period measurement")
            
        self.My_Handler.write_data(self.address_SCD40,[0x36,0x82])
        
        time.sleep(0.001)
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SCD40, 9)
        
        try:
            self.My_Handler.write_data(self.address_SCD40,[0x21,0xb1])
        except:
            print("SCD40 already starts period measurement")
        
        return str(Data_Get[0])+str(Data_Get[1])+str(Data_Get[3])+str(Data_Get[4])+str(Data_Get[6])+str(Data_Get[7])
        
    def SCD4x_start_periodic_measurement(self):
        self.My_Handler.write_data(self.address_SCD40,[0x21,0xb1])
        
    def SCD4x_stop_measurement(self):
        self.My_Handler.write_data(self.address_SCD40,[0x3f,0x86])
        
    def SCD4x_ReadMeasurement(self):
        # print("SCD40 1")
        self.My_Handler.write_data(self.address_SCD40,[0xec,0x05])
        
        time.sleep(0.001)
        # print("SCD40 2")
        Data_Get = self.My_Handler.read_numbers_bytes(self.address_SCD40, 9)
        
        co2 =int(hex(Data_Get[0]<<8),16)+int(hex(Data_Get[1]),16)
        temp =-45 + 175.0*(int(hex(Data_Get[3]<<8),16)+int(hex(Data_Get[4]),16))/65536.0
        humi =100*(int(hex(Data_Get[6]<<8),16)+int(hex(Data_Get[7]),16))/65536.0
        
        # print(time.strftime("%Y-%m-%d,%H:%M:%S++++++>", time.localtime()),"SCD40 CO2: {}, temperature: {}, humidity: {}".format(round(co2,2),round(temp,2),round(humi,2)))
        
        return [round(co2,2),round(temp,2),round(humi,2)]

