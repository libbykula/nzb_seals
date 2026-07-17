import os 
import hazelbean as hb
import re

user_dir = 'C:/Users/kibby'
extra_dirs = ['Files', 'seals', 'projects']
project_name = 'Brazil_magpie_npi_300m20260407_211228'

project_dir = os.path.join(user_dir, os.sep.join(extra_dirs), project_name)

stitched_lulc_dir = os.path.join(project_dir, 'intermediate', 'stitched_lulc_simplified_scenarios')

for year in ['2030', '2050']:
    # Clipped
    lulc_clipped_path = os.path.join(stitched_lulc_dir, 
                                'lulc_mapbiomas_seals7_ssp5_rcp85_magpie_bau_' + year + '_clipped.tif')
    output_clipped_path = re.sub('.tif', '_pog.tif', lulc_clipped_path)
    hb.make_path_pog(lulc_clipped_path, output_clipped_path, ndv = 255)

    # Unclipped
    lulc_path = os.path.join(stitched_lulc_dir, 
                                'lulc_mapbiomas_seals7_ssp5_rcp85_magpie_bau_' + year + '.tif')
    output_path = re.sub('.tif', '_pog.tif', lulc_path)
    hb.make_path_pog(lulc_path, output_path, ndv = 255)