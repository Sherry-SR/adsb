#!/usr/bin/python
#-*- coding:UTF-8 -*-

import xml.sax
import serial
import time,os

FILE_NAME = "currentData.xml"
OLD_FILE_NAME = "currentData.xml.1"
DEVICE    = "/dev/ttyUSB0"


gl_planes = []
gl_num    = 0

class PlaneDataHandler( xml.sax.ContentHandler ):
	def __init__(self):
		self.plane_list = []

		self.Number = 0
		self.Time   = ""
		self.Hex    = ""
		self.Mode   = ""
		self.Squawk = ""
		self.Flight = ""
		self.Altitude = ""
		self.Speed  = ""
		self.Heading = ""
		self.Latitude = ""
		self.Longitude = ""

		self.CurrentData = ""
	
	def startElement(self, tag, attributes):
		self.CurrentData = tag

	def endElement(self, tag):
		if tag == "Plane":
			# print "endElement,Plane",self.Time,self.Hex
			plane_dict=dict(
				Time=self.Time,
				Hex=self.Hex,
				Mode=self.Mode,
				Squawk=self.Squawk,
				Flight=self.Flight,
				Altitude=self.Altitude,
				Speed=self.Speed,
				Heading=self.Heading,
				Latitude=self.Latitude,
				Longitude=self.Longitude
			)
			self.plane_list.append(plane_dict)

		elif tag == "DataFrame":
			# print "endElement,DataFrame",self.plane_list
			# print 'len self.plane_list',len(self.plane_list)
			global gl_planes
			gl_planes = self.plane_list
			global gl_num
			gl_num = self.Number
			# print 'len gl_planes',len(gl_planes)
			self.plane_list = []
		self.CurrentData = ""

	def characters(self, content):
		if self.CurrentData == "Number":
			self.Number = content
		elif self.CurrentData == "Time":
			self.Time = content
		elif self.CurrentData == "Hex":
			self.Hex = content
		elif self.CurrentData == "Mode":
			self.Mode = content
		elif self.CurrentData == "Squawk":
			self.Squawk = content
		elif self.CurrentData == "Flight":
			self.Flight = content
		elif self.CurrentData == "Altitude":
			self.Altitude = content
		elif self.CurrentData == "Speed":
			self.Speed = content
		elif self.CurrentData == "Heading":
			self.Heading = content
		elif self.CurrentData == "Latitude":
			self.Latitude = content
		elif self.CurrentData == "Longtitute":
			self.Longitude = content
		else:
			pass

def parseXML():
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	handler = PlaneDataHandler()
	parser.setContentHandler(handler)	
	with open(FILE_NAME) as f:
		data = f.read()
		if len(data) < 50:
			print "[ERROR] %s is too short, replace it with an old file."%FILE_NAME
			cmd = []
			cmd.append('cp')
			cmd.append(OLD_FILE_NAME)
			cmd.append(FILE_NAME)
			os.system(' '.join(cmd))
	parser.parse(FILE_NAME)
	return [gl_num,gl_planes]

def initSerial(dev):
	while True:
		try:
			s = serial.Serial(dev,19200)
			print "[INFO] Serial init SUCCESS"
			return s
		except:
			time.sleep(10)
			print "[ERROR] Serial init FAILE, please plug in the usb serial device, another try will begin in 10 seconds."

def getXMLFromInternet():
	os.system("rm -f currentData.xml")
	os.system("wget www.laputa.pub/currentData.xml > /dev/null 2>&1")
	print "[INFO] get this file from the Internet"

if __name__ == "__main__":

	s = initSerial(DEVICE)

	while True:
		final_string_list = []
		print "[INFO] wait for a client"
		command = s.read(1)
		if command == 'A':
			
			info = parseXML()
			if len(info) == 2 and len(info[1]) != 0:   #determine if info has enough information to generate the string
				final_string_list.append(info[0])
				final_string_list.append(info[1][0]["Time"])
			else:
				print "[ERROR] xml file is too short, RESET"
				continue
			send_string = ','.join(final_string_list)
			send_string = str(send_string)
			print "[INFO] begin to send num and date",send_string
			s.write(send_string)

			for i in xrange(len(info[1])):
				command = s.read(1)
				if command != 'B':
					print "[INFO] command is not valid, RESET"
					s.write('R')
					continue

				final_string_list = []
				final_string_list.append(info[1][i]["Flight"])
				final_string_list.append(info[1][i]["Longitude"])
				final_string_list.append(info[1][i]["Latitude"])
				final_string_list.append(info[1][i]["Altitude"])
				final_string_list.append(info[1][i]["Speed"])
				send_string = ','.join(final_string_list)
				send_string = str(send_string)
				s.write(send_string)
				print "[INFO] send a message",i+1
			time.sleep(2)
			getXMLFromInternet()
		else:
			print "[INFO] command is not valid, RESET"
			s.write("R")
			print command
			continue
