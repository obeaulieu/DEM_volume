import numpy as np
import matplotlib.pyplot as plt
import glob

dems = sorted(glob.glob('*.tif')
shapefiles = sorted(glob.glob('*.shp')

#Scan times
dem_seconds = []
for dem in dems:
    seconds = dem.split('fullextent_')[-1].split('.')[0]
    dem_seconds.append(int(seconds))
    print seconds
    print dem_seconds

#shapefile times    
shapefile_seconds = []
for shapefile in shapefiles:
    shp_seconds = shapefile.split('.')[0]
    shapefile_seconds.append(int(shp_seconds))
    print shp_seconds
    print shapefile_seconds

#choose the correct DEM 
previous_dem = []
correct_dem = []
for i in range(dem_seconds):
    previous_dem = all(int(dem_seconds) < int(shp_seconds))
    correct_dem = max(previous_dem)
    
#find volume from shapefile and preceding DEM
