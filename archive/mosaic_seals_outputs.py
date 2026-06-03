import os
import sys

import hazelbean as hb
import pandas as pd
import geopandas as gpd
import glob
from osgeo import gdal
import pygeoprocessing as pygeo


tifs_list = []
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

    tif_files = glob.glob(os.path.join(tif_dir, '*_clipped.tif'))
    
    tifs_list.extend(tif_files)

print(tifs_list)
# pygeo.stitch_rasters()
