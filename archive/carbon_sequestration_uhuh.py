import os
import sys
import re
import hazelbean as hb
import pandas as pd
import geopandas as gpd
import glob
from osgeo import gdal
import pygeoprocessing as pygeo

base_dir = 'C:/Users/kibby/Files/base_data/carbon'

lulc_proj_global_coefs = os.path.join(base_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_clipped.tif')
lulc_proj_1deg_coefs = os.path.join(base_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_clipped_1deg_coefs.tif')

lulc_current = os.path.join(base_dir, 'lulc_mapbiomas_seals7_2023.tif')

paths = [lulc_proj_1deg_coefs, lulc_proj_global_coefs, lulc_current]
aligned_paths = []

for path in paths:
    aligned_path = re.sub('.tif', '_aligned_v02.tif', path)
    aligned_paths.append(aligned_path)


pygeo.align_and_resize_raster_stack(paths, aligned_paths, resample_method_list = ['near', 'near', 'near'],
                                    bounding_box_mode = 'intersection',
                                    target_pixel_size=(30,-30))