import os
import sys

import hazelbean as hb
import pandas as pd
import geopandas as gpd
import glob
from osgeo import gdal
import pygeoprocessing as pygeo
import re


def compress_tifs(path):
    #Open the input raster
    input_raster_path = path
    output_raster_path = re.sub('.tif', '_compress.tif', path)

    # Open the dataset
    src_ds = gdal.Open(input_raster_path)

    # Define the output options, including compression
    creation_options = ["COMPRESS=LZW", "TILED=YES", "BIGTIFF=IF_SAFER"]

    # Use gdal.Translate to apply the compression
    gdal.Translate(output_raster_path, src_ds, creationOptions=creation_options)

    # Close the dataset
    src_ds = None
    
    os.remove(input_raster_path)

tif_dict = {}

for year in range(2030, 2055, 5):
# for year in [2035]:
    tif_dict[year] = []

    for i in range(0, 12):        
        p = hb.ProjectFlow()

        # Assign project-level attributes to the p object (such as in p.base_data_dir = ... below)
        # including where the project_dir and base_data are located.
        # The project_name is used to name the project directory below. If the directory exists, each task will not recreate
        # files that already exist.
        p.user_dir = os.path.expanduser('~')
        p.ext_drive = 'D:/'
        p.extra_dirs = ['Files', 'seals', 'projects']
        p.project_name = 'Brazil_magpie_mapbiomas_policy6_30m_hb_pyr_chunks_near_' + str(i)

        tif_dir = os.path.join(p.user_dir, os.sep.join(p.extra_dirs), p.project_name, 'intermediate/stitched_lulc_simplified_scenarios/')
        tif_path = os.path.join(tif_dir, 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_' + str(year) + '_clipped.tif')
        tif_dict[year].append((tif_path, 1))

    # Make a raster to stitch into 
    output_path = os.path.join(p.user_dir, os.sep.join(p.extra_dirs), 'lulc_mapbiomas_seals7_ssp5_rcp85_luh2-magpie_bau_' + str(year) + '_clipped_mosaic.tif')
    base_path = os.path.join(p.ext_drive, 'base_data/lulc/mapbiomas/lulc_mapbiomas_2023_30m_hb_pyr_int_near.tif')

    pygeo.new_raster_from_base(
        base_path, target_path=output_path, datatype=gdal.GDT_UInt16, band_nodata_list = [0])

    # Mosaic
    pygeo.stitch_rasters(tif_dict[year],
                         resample_method_list=['mode']*len(tif_dict[year]),
                         target_stitch_raster_path_band=(output_path, 1)
    )
    
    # compress_tifs(output_path)

