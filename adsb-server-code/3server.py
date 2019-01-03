#!/usr/bin/env python
#rtlserver.py

import os
import time
import datetime
from threading import Thread

def cleartmpfile():
	while True:
		time.sleep(20)
		tmp=open('/tmp/tmp.txt','w')
		tmp.close()

#os.system('sudo sh /root/dump1090/dump1090 --interactive > /tmp/tmp.txt &')
os.system('mkdir /home/pi/adsb-code/data')

t=Thread(target=cleartmpfile)
t.setDaemon(1)
t.start()

f=open('/tmp/tmp.txt','r')

currentPlaneList=[]

while True:
	tmplist=f.readlines()
	# Get planes' information
	if len(tmplist)==0:
		time.sleep(1)
		continue
	while True:
		try:
			tmpstr=tmplist.pop()
		except:
			break
		print tmpstr,1
		if tmpstr.find('-----')!=-1:
			break 		

	if len(tmplist)==0:
		time.sleep(1)
		continue
	while True:
		try:
			tmpstr=tmplist.pop()
		except:
			break
		print tmpstr,
		if tmpstr.find('-----')!=-1:
		    break
		plane=tmpstr.split()
		if len(plane)<3:
		    continue
		planedict=dict(Hex='',Mode='',Squawk='',Flight='',Altitude='',Speed='',Heading='',Latitude='',Longtitute='')
		# if(len(plane)==12 and plane.count('S')==1):        # TODO:optimize
		#   currentPlaneList.append(plane)

		if(plane.count('S')):
		    planedict['Mode']='S'
		    planedict['Hex']=plane[0] if plane[1]=='S' else ''

		for i in xrange(len(plane)):
		    if plane[i][0].isalpha() and plane[i][-1].isdigit():
		        planedict['Flight']=plane[i] 
		    if plane[i].find('.')!=-1 and len(plane[i])==6:
		        planedict['Latitude']=plane[i] 
		    if plane[i].find('.')!=-1 and len(plane[i])==7:
		        planedict['Longtitute']=plane[i] 

		if planedict['Mode']!='' and planedict['Flight']!='':
		    if plane.index(planedict['Mode'])-plane.index(planedict['Flight'])==-2:
		        planedict['Squawk']=plane[plane.index(planedict['Mode'])+1]

		if planedict['Latitude']!='':
		    if plane[plane.index(planedict['Latitude'])-1].isdigit() and int(plane[plane.index(planedict['Latitude'])-1])<=360:
		        planedict['Heading']=plane[plane.index(planedict['Latitude'])-1]

		if planedict['Heading']!='':
		    if plane[plane.index(planedict['Heading'])-1].isdigit() and int(plane[plane.index(planedict['Heading'])-1])<1000:
		        planedict['Speed']=plane[plane.index(planedict['Heading'])-1]

		if planedict['Speed']!='':
		    if plane[plane.index(planedict['Speed'])-1].isdigit():
		        planedict['Altitude']=plane[plane.index(planedict['Speed'])-1]

		if planedict['Latitude']!='' and planedict['Longtitute']!='':
		    currentPlaneList.append(planedict)

	if len(currentPlaneList)==0:
		continue

	# Get current time
	now=(datetime.datetime.now()+datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

	# Save planes' information to currentData.xml
	currentData=open('/var/www/currentData.xml','w')
	currentData.write('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
	currentData.write('<DataFrame>\n')
	currentData.write('\t<Number>%s</Number>\n' % (str(len(currentPlaneList))))
	for i in xrange(len(currentPlaneList)):
		currentData.write('\t<Plane>\n')
		currentData.write('\t\t<Time>%s</Time>\n' % (now))
		currentData.write('\t\t<Hex>%s</Hex>\n' % (currentPlaneList[i]['Hex']))
		currentData.write('\t\t<Mode>%s</Mode>\n' % (currentPlaneList[i]['Mode']))	
		currentData.write('\t\t<Squawk>%s</Squawk>\n' % (currentPlaneList[i]['Squawk']))
		currentData.write('\t\t<Flight>%s</Flight>\n' % (currentPlaneList[i]['Flight']))
		currentData.write('\t\t<Altitude>%s</Altitude>\n' % (currentPlaneList[i]['Altitude']))
		currentData.write('\t\t<Speed>%s</Speed>\n' % (currentPlaneList[i]['Speed']))
		currentData.write('\t\t<Heading>%s</Heading>\n' % (currentPlaneList[i]['Heading']))
		currentData.write('\t\t<Latitude>%s</Latitude>\n' % (currentPlaneList[i]['Latitude']))
		currentData.write('\t\t<Longtitute>%s</Longtitute>\n' % (currentPlaneList[i]['Longtitute']))
		currentData.write('\t</Plane>\n')
	currentData.write('</DataFrame>\n')
	currentData.close()

	print now,len(currentPlaneList)

	# Save planes' information into database
	data=open('/home/pi/adsb-code/data/%s-NJ.xml' % now[:10],'a+')
	data.write('<DataFrame>\n')
	data.write('\t<Number>%s</Number>\n' % (str(len(currentPlaneList))))
	for i in xrange(len(currentPlaneList)):
		data.write('\t<Plane>\n')
		data.write('\t\t<Time>%s</Time>\n' % (now))
		data.write('\t\t<Hex>%s</Hex>\n' % (currentPlaneList[i]['Hex']))
		data.write('\t\t<Mode>%s</Mode>\n' % (currentPlaneList[i]['Mode']))	
		data.write('\t\t<Squawk>%s</Squawk>\n' % (currentPlaneList[i]['Squawk']))
		data.write('\t\t<Flight>%s</Flight>\n' % (currentPlaneList[i]['Flight']))
		data.write('\t\t<Altitude>%s</Altitude>\n' % (currentPlaneList[i]['Altitude']))
		data.write('\t\t<Speed>%s</Speed>\n' % (currentPlaneList[i]['Speed']))
		data.write('\t\t<Heading>%s</Heading>\n' % (currentPlaneList[i]['Heading']))
		data.write('\t\t<Latitude>%s</Latitude>\n' % (currentPlaneList[i]['Latitude']))
		data.write('\t\t<Longtitute>%s</Longtitute>\n' % (currentPlaneList[i]['Longtitute']))
		data.write('\t</Plane>\n')
	data.write('</DataFrame>\n')
	data.close()


	# Initialise
	currentPlaneList=[]
