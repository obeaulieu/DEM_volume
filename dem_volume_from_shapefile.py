import shapefile
import numpy as np
import matplotlib.pyplot as plt
import glob
import fnmatch
import os
import gdal
from scipy.optimize import curve_fit
from scipy.special import gamma
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
plt.ion()

# Run inside root dir for each experiment

dems = sorted(glob.glob('DEMs/projinfo/*fullextent_???????.tif'))
landslides = sorted(glob.glob('landslides_georeferenced/*.shx/*.shp'))

#Scan times
dem_seconds = []
for dem in dems:
    seconds = dem.split('.')[0].split('_')[-1]
    dem_seconds.append(int(seconds))
dem_seconds = np.array(dem_seconds)

#shapefile times    
landslide_seconds = []
for landslide in landslides:
    shp_seconds = landslide.split('/')[-1].split('.')[0]
    landslide_seconds.append(int(shp_seconds))
landslide_seconds = np.array(landslide_seconds)


#choose the correct DEM 
previous_dem = []
for i in range(len(landslide_seconds)):
    dems_before_landslide = dem_seconds < landslide_seconds[i]
    previous_dem_time = np.max(dem_seconds[dems_before_landslide])
    previous_dem.append(previous_dem_time)


# Finding volume for shapefile from DEM
def recursive_glob(rootdir='.', pattern='*'):
	"""Search recursively for files matching a specified pattern.
	
	Adapted from http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
	"""

	matches = []
	for root, dirnames, filenames in os.walk(rootdir):
	  for filename in fnmatch.filter(filenames, pattern):
		  matches.append(os.path.join(root, filename))

	return matches

files = sorted(recursive_glob(pattern='*.shp'))

for filename in files:
    sf = shapefile.Reader(filename)
    print filename
    shapes = sf.shapes()
# GeoTIFF
ds = gdal.Open(previous_dem)
for previous in previous_dem:   
DEM = ds.ReadAsArray() #..... (from previous time)
outarray = np.zeros(DEM.shape)
nY, nX = np.array(DEM.shape)
Y = np.arange(0, nY, 1)[::-1]/1000.
X = np.arange(0, nX, 1)/1000.
for shape in shapes:
    bbox = np.ceil(np.array(shape.bbox)*1E3)/1E3
    poly = Polygon(shape.points)
    x = np.round(np.arange(bbox[0], bbox[2], 0.001), 3)
    y = np.round(np.arange(bbox[1], bbox[3], 0.001), 3)
    #X, Y = np.meshgrid(x, y)
    #for xi in range(len(x)):
    #    for yi in range(len(y)):
    for xi in x:
        for yi in y:
            if poly.contains(Point(xi, yi)):
                # Export the height above the minimum cell
                # in the y-direiction at that x-location
                # Should be lowest cell in valley
                outarray[Y == yi, X == xi] = DEM[Y == yi, X == xi] - np.nanmin(DEM[:, X == xi])
    volume = np.nansum(outarray)/1E6 # mm cells to m, check DEM height
