import numpy as np
import netCDF4 as nc
import rasterio
import re
import os
import hazelbean as hb

# Mapping from pixel value → variable name
class_map = {
    10: "crop_rainfed",
    11: "crop_rainfed_herb",
    12: "crop_rainfed_tree",
    20: "crop_irrigated",
    30: "crop_natural_mosaic",
    40: "natural_crop_mosaic",
    50: "tree_broadleaved_evergreen",
    60: "tree_broadleaved_deciduous_closed_to_open_15",
    61: "tree_broadleaved_deciduous_closed_40",
    62: "tree_broadleaved_deciduous_open_15_40",
    70: "tree_needleleaved_evergreen_closed_to_open_15",
    71: "tree_needleleaved_evergreen_closed_40",
    72: "tree_needleleaved_evergreen_open_15_40",
    80: "tree_needleleaved_deciduous_closed_to_open_15",
    81: "tree_needleleaved_deciduous_closed_40",
    82: "tree_needleleaved_deciduous_open_15_40",
    90: "tree_mixed_type",
    100: "mosaic_tree_and_shrub_50_herbaceous_cover_50",
    110: "mosaic_herbaceous_cover_50_tree_and_shrub_50",
    120: "othernat",
    121: "evergreen_othernat",
    122: "deciduous_othernat",
    130: "grassland",
    140: "lichens_and_mosses",
    150: "sparse_vegetation_tree_shrub_herbaceous_cover_15",
    151: "sparse_tree_15",
    152: "sparse_shrub_15",
    153: "sparse_herbaceous_cover_15",
    160: "tree_cover_flooded_fresh_or_brakish_water",
    170: "tree_cover_flooded_saline_water",
    180: "shrub_or_herbaceous_cover_flooded_fresh_saline_brakish_water",
    190: "urban_areas",
    200: "bare_areas",
    201: "consolidated_bare_areas",
    202: "unconsolidated_bare_areas",
    210: "water_bodies",
    220: "permanent_snow_and_ice",
}

def tif_to_netcdf_per_class(tif_path, dst_path, year=2050):
    with rasterio.open(tif_path) as src:
        data = src.read(1)
        transform = src.transform
        nodata = src.nodata
        ny, nx = data.shape

        x = np.array([transform.c + (i + 0.5) * transform.a for i in range(nx)])
        y = np.array([transform.f + (j + 0.5) * transform.e for j in range(ny)])

    dst = nc.Dataset(dst_path, "w")

    # Dimensions
    dst.createDimension("time", 1)
    dst.createDimension("lat", ny)
    dst.createDimension("lon", nx)

    # Coordinate variables
    time_var = dst.createVariable("time", "i4", ("time",))
    time_var[:] = [year]
    time_var.units = f"year"

    lat_var = dst.createVariable("lat", "f8", ("lat",))
    lat_var[:] = y
    lat_var.axis = "Y"
    lat_var.units = "degrees_north"
    lat_var.standard_name = "latitude"

    lon_var = dst.createVariable("lon", "f8", ("lon",))
    lon_var[:] = x
    lon_var.axis = "X"
    lon_var.units = "degrees_east"
    lon_var.standard_name = "longitude"

    # One binary variable per class
    nodata_val = int(nodata) if nodata is not None else 255
    unique_vals = np.unique(data)
    print(f"Unique pixel values in source: {unique_vals}")

    for code, name in class_map.items():
        var = dst.createVariable(
            name, "u1",
            ("time", "lat", "lon"),
            zlib=True, complevel=5,
            fill_value=255
        )
        var.long_name = name
        var.class_code = code

        if code in unique_vals:
            var[0, :, :] = (data == code).view(np.uint8)
        else:
            var[0, :, :] = np.zeros((ny, nx), dtype=np.uint8)
            print(f"  code {code:>3} ({name}): not present in source, filled with 0")

    print(f"\nSaved: {dst_path}")
    dst.close()


# root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/'
# tif_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy_esp.tif')

# output_clipped_path = re.sub('.tif', '_pog.tif', tif_file)
# # hb.make_path_pog(tif_file, output_clipped_path, ndv = 255)

# netcdf_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy_per_class_pog_esp.nc')

# tif_to_netcdf_per_class(output_clipped_path, netcdf_file, year=2050)

# baseline_root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/'
# baseline_tif = os.path.join(baseline_root_path, 'lulc_esa_2015_esp.tif')
# baseline_nc = os.path.join(baseline_root_path, 'lulc_esa_2015_esp.nc')
# tif_to_netcdf_per_class(baseline_tif, baseline_nc, year=2015) # do they all have to be in the same netcdf? I don't think so, right?

# rcp85_root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp85/rcp85'
# rcp85_tif = os.path.join(rcp85_root_path, 'lulc_esa_gtap1_rcp85_ssp5_2050_no_policy_esp.tif')
# rcp85_nc = os.path.join(rcp85_root_path, 'lulc_esa_gtap1_rcp85_ssp5_2050_no_policy_esp.nc')
# tif_to_netcdf_per_class(rcp85_tif, rcp85_nc, year=2050) # do they all have to be in the same netcdf? I don't think so, right?

rcp45_root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp45/rcp45'
rcp45_tif = os.path.join(rcp45_root_path, 'lulc_esa_gtap1_rcp45_ssp2_2050_no_policy_esp.tif')
rcp45_nc = os.path.join(rcp45_root_path, 'lulc_esa_gtap1_rcp45_ssp2_2050_no_policy_esp.nc')
tif_to_netcdf_per_class(rcp45_tif, rcp45_nc, year=2050) 