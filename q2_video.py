import numpy as np
import pandas as pd
import geopandas as gpd
import descartes
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from shapely.geometry import Point, Polygon
from scipy.io import loadmat
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time


rain = loadmat('rain_India.mat')
pet = loadmat('PET_India.mat')
rain = rain['rain']
pet = pet['PET']

crs = { 'init' : 'epsg:4326'}


years = range(1951,2015)
months = ["January","February","March", "April" , "May" , "June" , "July" , "August" , "September" , "October" , "November" , "December"]
start_time = time.time()
for yrs in range(768):
	print("i =",yrs)
	print("Percentage done",yrs*100/768)
	x = [67.5+(r*0.25) for r in range(121)]
	y = [7.5+(r*0.25) for r in range(121)]

	XY=[]
	for xs in x:
		for ys in y:
			XY.append((xs,ys))
	rain_val = []
	for i,xs in enumerate(x):
		for j,ys in enumerate(y):
			rain_val.append(np.mean(rain[i][j][yrs]))
	pet_val = []
	for i,xs in enumerate(x):
		for j,ys in enumerate(y):
			pet_val.append(np.mean(pet[i][j][yrs]))

	aridity_index = []
	# aridity_index = np.array(avg_pet_val)/np.array(avg_rain_val)

	for (a,b) in zip(pet_val,rain_val):
		if b>0:
			aridity_index.append(a/b)
		else:
			aridity_index.append(0)
	fin_index = []
	for ind in aridity_index:
		if ind<12 and ind>=5:
			fin_index.append('Arid')
		elif ind<5 and ind>=2:
			fin_index.append('Semi-Arid')
		elif ind<2 and ind>=0.75:
			fin_index.append('Sub-Humid')
		elif ind<0.75 and ind>=0.375:
			fin_index.append('Humid')
		else:
			fin_index.append('None')
	df = pd.DataFrame(fin_index,columns = ['aridity'])
	s_map = gpd.read_file('./Indian_States.shp')
	fig,ax = plt.subplots(figsize=(10,10))


	geometry = [Point(xy) for xy in XY]

	geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)

	s_map.plot(ax=ax,alpha= 0.4, color='grey')
	# geo_df[geo_df['rain']>geo_df['pet']].plot(ax=ax,markersize=20,color="blue", marker="s", label="rain>pet")
	geo_df[geo_df['aridity']=='Arid'].plot(ax=ax,markersize=20,color="pink", marker="s", label="Arid")
	geo_df[geo_df['aridity']=='Semi-Arid'].plot(ax=ax,markersize=20,color="teal", marker="s", label="Semi-Arid")
	geo_df[geo_df['aridity']=='Sub-Humid'].plot(ax=ax,markersize=20,color="turquoise", marker="s", label="Sub-Humid")
	geo_df[geo_df['aridity']=='Humid'].plot(ax=ax,markersize=20,color="orange", marker="s", label="Humid")
	# geo_df[geo_df['rain']>0 and geo_df['pet']/geo_df['rain'] ].plot(ax=ax,markersize=20,color="red", marker="s", label="rain<pet")
	plt.legend(prop={'size':15})
	plt.title("India's Aridity on "+str(months[yrs%12])+' '+str(years[int(yrs/12)]))

	print("Time Elapsed =",time.time()-start_time, "secs")
	plt.savefig('./aridity/'+str(yrs)+'.png')
	plt.close()
