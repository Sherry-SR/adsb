#/usr/bin/python

import os,time,datetime

LOCATION='NJ'

FILE_NAME = (datetime.datetime.now()+datetime.timedelta(hours=8-24)).strftime('%Y-%m-%d %H:%M:%S')[:10]+'-'+LOCATION+'.xml'
PATH = '/home/pi/adsb-code/data' 

cmd = 'mv '+PATH+FILE_NAME+' '+'/tmp/'
print cmd
#os.system(cmd)
cmd = 'cd /tmp && python /home/pi/adsb-code/bypy/bypy.py upload'
print cmd
#os.system(cmd)

#time.sleep(900)

#os.system(cmd)



#clear
cmd = 'cd /tmp && rm -f '+FILE_NAME
print cmd
#os.system(cmd)
