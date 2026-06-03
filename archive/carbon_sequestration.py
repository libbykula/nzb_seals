import os
import sys
import re
import hazelbean as hb
import pandas as pd
import geopandas as gpd
import glob
from osgeo import gdal
import pygeoprocessing as pygeo
import natcap.invest.carbon
import natcap.invest.utils

base_dir = 'C:/Users/kibby/Files/base_data/carbon'

lulc_proj_global_coefs = os.path.join(base_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_clipped_global_coefs.tif')
lulc_proj_1deg_coefs = os.path.join(base_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_clipped_1deg_coefs.tif')

lulc_current = os.path.join(base_dir, 'lulc_mapbiomas_seals7_2023.tif')

paths = [lulc_proj_1deg_coefs, lulc_proj_global_coefs, lulc_current]
linear_paths = []
aligned_paths = []

# for path in paths:
#     linear_path = re.sub('.tif', '_linear.tif', path)
#     gdal.Warp(linear_path, path, 
#               dstSRS='EPSG:5880', xRes=30, yRes=30,
#               resampleAlg=gdal.GRA_NearestNeighbour) 
#     linear_paths.append(linear_path)
    
#     aligned_path = re.sub('.tif', '_aligned.tif', path)
#     aligned_paths.append(aligned_path)


# pygeo.align_and_resize_raster_stack(linear_paths, aligned_paths, resample_method_list = ['near', 'near', 'near'],
#                                     bounding_box_mode = 'intersection',
#                                     target_pixel_size=(30,-30))

# args_1deg = {
#     'calc_sequestration': True,
#     'carbon_pools_path': 'C:\\Users\\kibby\\Files\\base_data\\carbon\\219_carbon_table.csv',
#     'discount_rate': '',
#     'do_redd': False,
#     'do_valuation': False,
#     'lulc_cur_path': 'C:\\Users\\kibby\\Files\\base_data\\carbon\\lulc_mapbiomas_seals7_2023_aligned.tif',
#     'lulc_cur_year': '',
#     'lulc_fut_path': 'C:\\Users\\kibby\\Files\\base_data\\carbon\\lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_clipped_1deg_coefs_aligned.tif',
#     'lulc_fut_year': '',
#     'lulc_redd_path': '',
#     'price_per_metric_ton_of_c': '',
#     'rate_change': '',
#     'results_suffix': '',
#     'workspace_dir': 'C:\\Users\\kibby\\Files\\seals\\carbon\\1deg_coefs',
# }

# if __name__ == '__main__':
#     natcap.invest.carbon.execute(args_1deg)

args_global = {
    'calc_sequestration': True,
    'carbon_pools_path': 'C:\\Users\\kibby\\Files\\base_data\\carbon\\219_carbon_table.csv',
    'discount_rate': '',
    'do_redd': False,
    'do_valuation': False,
    'lulc_bas_path': 'C:\\Users\\kibby\\Files\\base_data\\carbon\\lulc_mapbiomas_seals7_2023_aligned.tif',
    'lulc_cur_year': '',
    'lulc_alt_path': 'C:\\Users\\kibby\\Files\\base_data\\carbon\\lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_clipped_global_coefs_aligned.tif',
    'lulc_fut_year': '',
    'lulc_redd_path': '',
    'price_per_metric_ton_of_c': '',
    'rate_change': '',
    'results_suffix': '',
    'workspace_dir': 'C:\\Users\\kibby\\Files\\seals\\carbon\\global_coefs_py',
}

if __name__ == '__main__':
    natcap.invest.carbon.execute(args_global)