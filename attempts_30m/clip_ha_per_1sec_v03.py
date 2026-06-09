import os
from osgeo import gdal
import re

# Base directories
user_dir = os.path.expanduser('~')
inputdir = os.path.join(user_dir, 'Files/base_data/')

# Input raster
raster_path = os.path.join(inputdir, 'pyramids/ha_per_cell_1sec.tif')

# Output raster
output_path = re.sub(r'\.tif$', '_clipped_pyrbb.tif', raster_path)

# Define bounding box (xmin, ymin, xmax, ymax)
# From your message:
# -74.8976656341639995,-34.8659093143816534 : -33.0609989674973335,7.9374240189516803
output_bounds = (-74.897665634164, -34.865909314382, -33.060998967497, 7.937424018952)

# Run GDAL Warp to clip by bounding box
gdal.Warp(
    destNameOrDestDS=output_path,
    srcDSOrSrcDSTab=raster_path,
    outputBounds=output_bounds,
    cropToCutline=False,  # not using a cutline
    dstNodata=None,       # or set a nodata value, e.g., 0 or -9999
    creationOptions=[
        "COMPRESS=LZW",
        "TILED=YES",
        "BIGTIFF=YES"
    ]
)

print("✅ Clipped raster saved to:", output_path)
