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
project_dir = 'C:/Users/kibby/Files/seals/projects'

# cz_list = ['207', '216', '217', '218', '219']
# cz_list = ['216', '217', '218', '219']
# cz_list = ['218', '219']
cz_list = ['219']

for cz in cz_list:
    print(cz)
# def run_carbon_by_zone(cz):
    lulc_proj_global_coefs = os.path.join(project_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_global_clipped_mosaic.tif')

    # lulc_proj_1deg_coefs = os.path.join(project_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_2050_1deg_clipped_mosaic.tif')

    lulc_current = os.path.join(base_dir, 'lulc_mapbiomas_seals7_2023.tif')

    all_lookup_table = pd.read_csv(os.path.join(base_dir, 'exhaustive_carbon_table.csv'))
    carbon_zone_gdf = gpd.read_file(os.path.join(base_dir, 'carbon_zones/carbon_zones.shp'))
    carbon_zone_gdf = carbon_zone_gdf[carbon_zone_gdf['REGION'] == 'South America']
    
    # Get the cz's lookup table
    cz_lookup_table = all_lookup_table[all_lookup_table['carbon_zone_id'] == int(cz)]
    cz_lookup_table = cz_lookup_table.T
    cz_lookup_table = cz_lookup_table.reset_index()
    cz_lookup_table.columns = ['lucode', 'c_above']
    cz_lookup_table.drop(index=0, inplace=True)
    
    cz_lookup_table[['c_below', 'c_soil', 'c_dead']] = 0

    cz_lookup_path = os.path.join(base_dir, 'carbon_zones/cz_' + cz + '_lookup.csv')
    cz_lookup_table.to_csv(cz_lookup_path)

    cz_boundary_path = os.path.join(base_dir, 'carbon_zones/carbon_zone_' + cz + '.gpkg')
    cz_boundary = carbon_zone_gdf[carbon_zone_gdf['CODE'] == int(cz)]
    cz_boundary.to_file(cz_boundary_path)
    
    cz_boundary = gpd.read_file(cz_boundary_path)
    
    invalid = cz_boundary[~cz_boundary.is_valid]

    if not invalid.empty:
        print("Invalid geometries found, attempting to fix with buffer(0)...")
        cz_boundary['geometry'] = cz_boundary['geometry'].buffer(0)
        cz_boundary.to_file(cz_boundary_path, driver='GPKG')


    # Clipping, getting in linear units, and aligning
    # paths = [lulc_proj_1deg_coefs, lulc_proj_global_coefs, lulc_current]
    paths = [lulc_proj_global_coefs, lulc_current]
    linear_paths = []
    aligned_paths = []
    clipped_paths = []
    for path in paths:
        clipped_path = re.sub(r'\.tif$', f'_clipped_{cz}.tif', path)
        if os.path.exists(clipped_path) == 0:
            gdal.Warp(clipped_path, path, cutlineDSName=cz_boundary_path, cropToCutline=True)
        clipped_paths.append(clipped_path)
        
        linear_path = re.sub(r'\.tif$', f'_linear_{cz}.tif', path)
        gdal.Warp(linear_path, clipped_path, 
                  dstSRS='EPSG:5880', xRes=30, yRes=30,
                  resampleAlg=gdal.GRA_NearestNeighbour) 
        linear_paths.append(linear_path)
        
        aligned_path = re.sub(r'\.tif$', f'_aligned_{cz}.tif', path)
        aligned_paths.append(aligned_path)

    # aligning for safety
    # pygeo.align_and_resize_raster_stack(linear_paths, aligned_paths, resample_method_list = ['near', 'near', 'near'],
    pygeo.align_and_resize_raster_stack(linear_paths, aligned_paths, resample_method_list = ['near', 'near'],
                                        bounding_box_mode = 'intersection',
                                        target_pixel_size=(30,-30))

    for file in clipped_paths:
        os.remove(file)
    
    for file in linear_paths:
        os.remove(file)

    args_global = {
        'calc_sequestration': True,
        'carbon_pools_path': f'C:\\Users\\kibby\\Files\\base_data\\carbon\\carbon_zones\\cz_{cz}_lookup.csv',
        'discount_rate': '',
        'do_redd': False,
        'do_valuation': False,
        'lulc_bas_path': aligned_paths[1],
        'lulc_cur_year': '',
        'lulc_alt_path': aligned_paths[0],
        'lulc_fut_year': '',
        'lulc_redd_path': '',
        'price_per_metric_ton_of_c': '',
        'rate_change': '',
        'results_suffix': cz,
        'workspace_dir': 'C:\\Users\\kibby\\Files\\seals\\carbon\\global_coefs_py',
    }

    if __name__ == '__main__':
        natcap.invest.carbon.execute(args_global)
    
    # args_1deg = {
    #     'calc_sequestration': True,
    #     'carbon_pools_path': f'C:\\Users\\kibby\\Files\\base_data\\carbon\\carbon_zones\\cz_{cz}_lookup.csv',
    #     'discount_rate': '',
    #     'do_redd': False,
    #     'do_valuation': False,
    #     'lulc_bas_path': aligned_paths[2], # FIX 
    #     'lulc_cur_year': '',
    #     'lulc_alt_path': aligned_paths[0], # FIX
    #     'lulc_fut_year': '',
    #     'lulc_redd_path': '',
    #     'price_per_metric_ton_of_c': '',
    #     'rate_change': '',
    #     'results_suffix': cz,
    #     'workspace_dir': 'C:\\Users\\kibby\\Files\\seals\\carbon\\1deg_coefs_py\\' + cz,
    # }

    # if __name__ == '__main__':
    #     natcap.invest.carbon.execute(args_1deg)
    
    # for file in aligned_paths:
    #     os.remove(file)
    