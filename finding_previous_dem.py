import numpy as np
import matplotlib.pyplot as plt
import glob

dems = sorted(glob.glob('DEMs/projinfo/*fullextent_???????.tif'))
shapefiles = sorted(glob.glob('landslides_georeferenced/*.shx/*.shp'))

#Scan times
dem_seconds = []
for dem in dems:
    seconds = dem.split('.')[0].split('_')[-1]
    dem_seconds.append(int(seconds))
    #print seconds
    #print dem_seconds
dem_seconds = np.array(dem_seconds)

#shapefile times    
shapefile_seconds = []
for shapefile in shapefiles:
    shp_seconds = shapefile.split('/')[-1].split('.')[0]
    shapefile_seconds.append(int(shp_seconds))
    #print shp_seconds
    #print shapefile_seconds
shapefile_seconds = np.array(shapefile_seconds)

#choose the correct DEM 
previous_dem = []
for i in range(len(shapefile_seconds)):
    dems_before_landslide = dem_seconds < shapefile_seconds[i]
    previous_dem_time = np.max(dem_seconds[dems_before_landslide])
    previous_dem.append(previous_dem_time)
