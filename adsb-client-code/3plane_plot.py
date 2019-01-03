#!/usr/bin/python
#-*- coding:UTF-8 -*-

import xml.sax

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys

FILE_NAME = "2015-04-26.xml"
FACTOR = 1
LONS = []
LATS = []

class PlaneDataHandler( xml.sax.ContentHandler ):
	def __init__(self,factor):
		self.plane_list = []
		self.CurrentData = ""
		self.DataFrameCounter = 0
		self.PlaneCounter = 0
		self.factor = factor

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

	def endDocument(self):
		print self.PlaneCounter,"points have been analysed."

	def startElement(self, tag, attributes):
		self.CurrentData = tag

	def endElement(self, tag):
		if tag == "Plane":
			# print "endElement,Plane",self.Time,self.Hex
			self.PlaneCounter += 1
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
			LONS.append(float(plane_dict["Longitude"]))
			LATS.append(float(plane_dict["Latitude"]))

		elif tag == "DataFrame":
			if self.DataFrameCounter % self.factor == 0:
				print "endElement,DataFrame",self.plane_list[0]["Time"],self.DataFrameCounter
				self.dataAnalyse()
			self.DataFrameCounter += 1
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

	def dataAnalyse(self):
		pass
		# for plane in self.plane_list:
		# 	x, y = m(float(plane["Longitude"]),float(plane["Latitude"]))
		# 	m.scatter(x,y,s=0.05,marker='o',color='#FF5600')

def analyse():


	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
	handler = PlaneDataHandler(FACTOR)
	parser.setContentHandler(handler)

	parser.parse(FILE_NAME)

	#save or update it
	output = open('plane_plot.pkl','wb')
	pickle.dump(LONS,output)
	pickle.dump(LATS,output)
	print "Analyse success and save it to plane_plot.pkl"



def plot():
	plt.figure(figsize=(20,15))
	#============================================# read data

	names = []
	pops  = []
	lats  = []
	lons  = []
	for line in file("major_city"):
		info = line.split()
		names.append(info[0])
		pops.append(float(info[1]))
		lat  = float(info[2][:-1])
		if info[2][-1] == 'S': 
			lat = -lat
		lats.append(lat)
		lon  = float(info[3][:-1])
		if info[3][-1] == 'W': 
			lon = -lon + 360.0
		lons.append(lon)


	#============================================
	# set up map projection with
	# use low resolution coastlines.

	# map = Basemap(llcrnrlon=0.,llcrnrlat=0.,urcrnrlon=-20.,urcrnrlat=57.,
	#             projection='lcc',lat_0=35,lon_0=120,
	#             resolution ='l')

	m = Basemap(projection='merc',lat_0 = 31.7, lon_0 = 119.5,area_thresh = 0.1,
		llcrnrlon=109,llcrnrlat=25,urcrnrlon=125,urcrnrlat=40,resolution='l')
	# draw coastlines, country boundaries, fill continents.
	m.drawcoastlines(linewidth=0.25)
	m.drawcountries(linewidth=0.25)
	# draw the edge of the map projection region (the projection limb)
	m.drawmapboundary(fill_color='#689CD2')
	# draw lat/lon grid lines every 30 degrees.
	m.drawmeridians(np.arange(0,360,30))
	m.drawparallels(np.arange(-90,90,30))
	# Fill continent wit a different color
	m.fillcontinents(color='gray',lake_color='#689CD2',zorder=0)
	# compute native map projection coordinates of lat/lon grid.

	# x, y = m(lons, lats)
	# for i,j,name in zip(x,y,names):
	#     cs = m.scatter(i,j,s=80,marker='o',color='#FF5600')
	#     plt.text(i,j,name,rotation=30,fontsize=10)

	max_pop = max(pops)
	size_factor = 80.0
	y_offset    = 15.0
	rotation    = 30
	print lons,lats
	x, y = m(lons, lats)
	for i,j,k,name in zip(x,y,pops,names):
		size = size_factor*k/max_pop
		cs = m.scatter(i,j,s=size,marker='o',color='#FF5600')
		plt.text(i,j+y_offset,name,rotation=rotation,fontsize=10)

	plt.title('Major Cities in Asia & Population')


	# plt.show()

	# load the data from pkl file.
	pkl_file = open('plane_plot.pkl','rb')
	LONS = pickle.load(pkl_file)
	LATS = pickle.load(pkl_file)

	x,y = m(LONS, LATS)
	# m.plot(x, y, 'ro', markersize=0.05,color='#FF5600')
	m.scatter(x,y,s=0.005,marker='o',color='#FF5600')
	# m.plot(x,y,'o',markersize=0.05,color='red')
	# plt.savefig(FILE_NAME[:-3]+'jpg',dpi=240)

	m.plot(x,y,'o',markersize=0.05,color='red')
	# plt.savefig(FILE_NAME[:-3]+'png',dpi=240)

	plt.show()


	# plt.savefig('/tmp/fff.eps',dpi=120)
	# plt.savefig('/tmp/fff.svg',dpi=120)

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print \
	'''
	usage: python filename.py [analyse | plot]
	'''
	elif len(sys.argv) == 2:
		if sys.argv[1] == "analyse":
			analyse()
		if sys.argv[1] == "plot":
			plot()