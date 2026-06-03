from osgeo import gdal
import os
import re
import hazelbean as hb

### USING HAZELBEAN hb.resample_to_match_pyramid in pyramids.py 
user_dir = os.path.expanduser('~')
inputdir = os.path.join(user_dir, 'Files/base_data/')

ref_raster_path = os.path.join(inputdir, 'pyramids/ha_per_cell_10sec.tif')

# Raster
mapbiomas_orig_path = os.path.join(inputdir, 'lulc/mapbiomas/lulc_mapbiomas_2024.tif')

# GDAL WARP to clip
path_300m = re.sub('.tif', '_300m.tif', mapbiomas_orig_path)
# path_300m_pyr = re.sub('.tif', '_300m_pyr.tif', mapbiomas_orig_path)

# Open your reference raster
ref_ds = gdal.Open(ref_raster_path)
ref_gt = ref_ds.GetGeoTransform()
ref_proj = ref_ds.GetProjection()

# Extract info from reference
x_min = ref_gt[0]
y_max = ref_gt[3]
x_res = ref_gt[1]
y_res = ref_gt[5]
x_size = ref_ds.RasterXSize
y_size = ref_ds.RasterYSize

# Compute bounding box from reference transform
x_max = x_min + x_res * x_size
y_min = y_max + y_res * y_size  # y_res is negative

nodata_val = 0

# Warp the source raster to exactly match the reference grid
gdal.Warp(
    destNameOrDestDS=path_300m,
    srcDSOrSrcDSTab=mapbiomas_orig_path,
    xRes=abs(x_res),
    yRes=abs(y_res),
    targetAlignedPixels=True,
    outputBounds=(x_min, y_min, x_max, y_max),
    dstSRS=ref_proj,
    srcNodata=nodata_val, # Treat this value as NoData in source
    dstNodata=nodata_val, # Set this value as NoData in output
    resampleAlg='near',  # 'bilinear' or 'cubic' for continuous data
    creationOptions=[
        "COMPRESS=LZW",
        "TILED=YES",
        "BIGTIFF=YES"
    ]
)


# hb.resample_to_match_pyramid(input_path = path_300m,
#                       match_path = ref_raster_path,
#                       output_path = path_300m_pyr,
#                       resample_method = 'mode',
#                       output_data_type = gdal.GDT_Int16)
