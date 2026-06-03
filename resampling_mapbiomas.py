import os, sys, shutil, random, math, atexit, time, json

from osgeo import gdal, ogr, osr
import numpy as np

import hazelbean as hb
import hazelbean.geoprocessing_extension

import functools
from functools import reduce
from osgeo import gdal
# gdal.SetConfigOption("IGNORE_COG_LAYOUT_BREAK", "YES") 
# gdal.PushErrorHandler('CPLQuietErrorHandler')
L = hb.get_logger('spatial_projection')

# Define paths
# input_path = "C:/Users/barbara.zimbres/Files/base_data/lulc/mapbiomas/brasil_coverage_2023_30m.tif"
# match_path = "C:/Users/barbara.zimbres/Files/base_data/lulc/esa/lulc_esa_2017.tif"  # Defines target resolution/projection
# output_path = "C:/Users/barbara.zimbres/Files/base_data/lulc/mapbiomas/lulc_mapbiomas_2023.tif"
input_path = 'D:/base_data/lulc/mapbiomas/lulc_mapbiomas_2023_30m.tif'
match_path = 'D:/base_data/lulc/esa/lulc_esa_2017.tif'  # Defines target resolution/projection
output_path = "D:/base_data/lulc/mapbiomas/lulc_mapbiomas_2023_300m_mode.tif"


def resample_to_match(input_path,
                      match_path,
                      output_path,
                      resample_method='mode',
                      output_data_type=None,
                      src_ndv=None,
                      ndv=None,
                      s_srs_wkt=None,
                      compress=True,
                      ensure_fits=False,
                      gtiff_creation_options=hb.globals.DEFAULT_GTIFF_CREATION_OPTIONS,
                      calc_raster_stats=False,
                      add_overviews=False,
                      pixel_size_override=None,
                      target_aligned_pixels=True,
                      bb_override=None,
                      verbose=False,
                      ):
    if pixel_size_override is None:
        target_pixel_size = (hb.get_cell_size_from_uri(match_path), -hb.get_cell_size_from_uri(match_path))
    elif not isinstance(pixel_size_override, (tuple, list)):
        target_pixel_size = (pixel_size_override, -pixel_size_override)

    target_sr_wkt = hb.get_raster_info_hb(match_path)['projection']

    if bb_override is None:
        target_bb = hb.get_raster_info_hb(match_path)['bounding_box']
    else:
        target_bb = bb_override
        
    if output_data_type is None:
        output_data_type = hb.get_datatype_from_uri(match_path)

    if src_ndv is None:
        src_ndv = hb.get_ndv_from_path(input_path)

    if ndv is None:
        dst_ndv = hb.get_ndv_from_path(match_path)
    else:
        dst_ndv = ndv
        # correct_ndv = hb.get_correct_ndv_from_flex(output_data_type, is_id=True)
        # if output_data_type < 5:
        #     dst_ndv = 255
        # else:
        #     dst_ndv = -9999.0

    if ensure_fits:
        # This addition to the core geoprocessing code was to fix the case where the alignment moved the target tif
        # up and to the left, but in a way that then trunkated 1 row/col on the bottom right, causing wrong-shape
        # raster_math errors.z
        pass
        # target_bounding_box = reduce(
        #     functools.partial(hb.merge_bounding_boxes, mode=bounding_box_mode),
        #     [info['bounding_box'] for info in
        #      (raster_info_list + vector_info_list)])
        #
        # if original_bounding_box[2] > target_bounding_box[2]:
        #     target_bounding_box[2] += target_pixel_size[0]
        #
        # if original_bounding_box[3] > target_bounding_box[3]:
        #     target_bounding_box[3] -= target_pixel_size[1]

        target_bb[2] += target_pixel_size[0]
        target_bb[3] += target_pixel_size[1]
    if compress is True or compress == 'ZSTD':
        gtiff_creation_options = (
            'TILED=YES',
            'BIGTIFF=YES',
            'COMPRESS=ZSTD',
            'BLOCKXSIZE=512',
            'BLOCKYSIZE=512',
        )
    elif compress:
        gtiff_creation_options = (
            'TILED=YES',
            'BIGTIFF=YES',
            'BLOCKXSIZE=512',
            'BLOCKYSIZE=512',
            compress.upper(),
        )
    else:
        gtiff_creation_options = (
            'TILED=YES',
            'BIGTIFF=YES',
            'BLOCKXSIZE=512',
            'BLOCKYSIZE=512',
        )
    hb.warp_raster_hb(input_path, target_pixel_size, output_path,
                      resample_method, target_bb=target_bb, base_sr_wkt=s_srs_wkt, target_sr_wkt=target_sr_wkt,
                      gtiff_creation_options=gtiff_creation_options,
                      n_threads=None, vector_mask_options=None,
                      output_data_type=output_data_type,
                      src_ndv=src_ndv,
                      dst_ndv=dst_ndv,
                      calc_raster_stats=calc_raster_stats,
                      add_overviews=add_overviews,
                      target_aligned_pixels=target_aligned_pixels,
    )

resample_to_match(
    input_path=input_path,
    match_path=match_path,
    output_path=output_path
)