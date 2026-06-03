from osgeo import gdal
import os
import re
import hazelbean as hb

### USING HAZELBEAN hb.resample_to_match_pyramid in pyramids.py 

# user_dir = os.path.expanduser('~')
# inputdir = os.path.join(user_dir, 'Files/base_data/seals/static_regressors/')
# outputdir = '/projects/standard/jajohns/shared/Files/seals'
outputdir = 'C:/Users/kibby/Files/base_data'

# ref_raster_path = os.path.join(outputdir, 'pyramids/ha_per_cell_1sec_clipped_pyrbb.tif') # need this to be 10sec, if I clip it, does that take care of the below one being clipped? probs not 

# Input raster
input_pyr_path = os.path.join(outputdir, 'pyramids/ha_per_cell_10sec.tif')

# Output raster
output_pyr_path = re.sub('.tif', '_clipped_pyrbb.tif', input_pyr_path)

# Define bounding box (xmin, ymin, xmax, ymax)
# From your message:
# -74.8976656341639995,-34.8659093143816534 : -33.0609989674973335,7.9374240189516803
output_bounds = (-74.897665634164, -34.865909314382, -33.060998967497, 7.937424018952)

# Run GDAL Warp to clip by bounding box
gdal.Warp(
    destNameOrDestDS=output_pyr_path,
    srcDSOrSrcDSTab=input_pyr_path,
    outputBounds=output_bounds,
    cropToCutline=False,  # not using a cutline
    dstNodata=None,       # or set a nodata value, e.g., 0 or -9999
    creationOptions=[
        "COMPRESS=LZW",
        "TILED=YES",
        "BIGTIFF=YES"
    ]
)

print("✅ Clipped 10sec pyramid raster saved to:", output_pyr_path)

