import datetime,time,os

now = datetime.datetime.now()


filename = r'/home/pi/DataLog/Test1_{}_{}_{}_{}_{}_{}.json'.format(now.year, str(now.month).zfill(2),str(now.day).zfill(2),str(now.hour).zfill(2),str(now.minute).zfill(2),str(now.second).zfill(2))

try: 
    os.mkdir(r"/home/pi/DataLog")
except Exception as e:
    print("build Failed: ", e)

while True:
    with open(filename, 'a+') as f: 
        f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'\r\n')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    time.sleep(3)




