import numpy
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
	print("Time Elapsed =",time.time()-start_time, "secs")
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
			rain_val.append(rain[i][j][yrs])
	pet_val = []
	for i,xs in enumerate(x):
		for j,ys in enumerate(y):
			pet_val.append(pet[i][j][yrs])

	list_tup = list(zip(rain_val,pet_val))

	df = pd.DataFrame(list_tup,columns = ['rain','pet'])
	s_map = gpd.read_file('./Indian_States.shp')
	fig,ax = plt.subplots(figsize=(10,10))


	geometry = [Point(xy) for xy in XY]

	geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)

	s_map.plot(ax=ax,alpha= 0.4, color='grey')
	geo_df[geo_df['rain']>geo_df['pet']].plot(ax=ax,markersize=20,color="blue", marker="s", label="rain>pet")
	geo_df[geo_df['rain']<geo_df['pet']].plot(ax=ax,markersize=20,color="red", marker="s", label="rain<pet")
	plt.legend(prop={'size':15})
	plt.title(str(months[yrs%12])+' '+str(years[int(yrs/12)]))

	plt.savefig('./images/'+str(yrs)+'.png')
	plt.close()

# plt.show()
