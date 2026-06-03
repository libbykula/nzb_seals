from osgeo import gdal
import os
import re
import hazelbean as hb
### USING HAZELBEAN hb.resample_to_match_pyramid in pyramids.py 

# user_dir = os.path.expanduser('~')
inputdir = os.path.join('D:/base_data/seals/static_regressors/300m')
# outputdir = '/projects/standard/jajohns/shared/Files/seals'
outputdir = 'D:/base_data/seals/static_regressors'

ref_raster_path = 'D:/base_data/pyramids/ha_per_cell_1sec_clipped_pyrbb.tif' # need this to be 10sec, if I clip it, does that take care of the below one being clipped? probs not 

# Define bounding box (xmin, ymin, xmax, ymax)
# From your message:
output_bounds = (-74.897665634164, -34.865909314382, -33.060998967497, 7.937424018952)

# # Run GDAL Warp to clip by bounding box
# gdal.Warp(
#     destNameOrDestDS=output_pyr_path,
#     srcDSOrSrcDSTab=input_pyr_path,
#     outputBounds=output_bounds,
#     cropToCutline=False,  # not using a cutline
#     dstNodata=None,       # or set a nodata value, e.g., 0 or -9999
#     creationOptions=[
#         "COMPRESS=LZW",
#         "TILED=YES",
#         "BIGTIFF=YES"
#     ]
# )

# print("✅ Clipped 10sec pyramid raster saved to:", output_pyr_path)


#### resampling regressors

# file_names = ['soil_organic_content',
#               '']

# filenames = sorted(
#     os.path.splitext(f)[0]
#     for f in os.listdir(inputdir)
#     if f.lower().endswith(".tif") and os.path.isfile(os.path.join(inputdir, f))
# )

# filenames = ['strict_pa',
#              'temperature_c',
#              'travel_time_to_market_mins',
#              'wetlands_binary']

filenames = ['wetlands_binary']
for file in filenames:
    print(file)
    path = os.path.join(inputdir, file + '.tif')
    clipped_path = os.path.join(outputdir, file + '_clipped.tif')

    # trying clipping it first 
    # gdal.Warp(
    #     destNameOrDestDS=clipped_path,
    #     srcDSOrSrcDSTab=path,
    #     outputBounds=output_bounds,
    #     cropToCutline=False,  # not using a cutline
    #     dstNodata=None,       # or set a nodata value, e.g., 0 or -9999
    #     creationOptions=[
    #         "COMPRESS=LZW",
    #         "TILED=YES",
    #         "BIGTIFF=YES"
    #     ]
    # )

    # GDAL WARP to clip
    output_path = os.path.join(outputdir, file + '_30m.tif')

    hb.resample_to_match_pyramid(input_path = clipped_path,
                        match_path = ref_raster_path,
                        output_path = output_path,
                        output_data_type = gdal.GDT_Int16) # how can i set it to be whatever this is?
