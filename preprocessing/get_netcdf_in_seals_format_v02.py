import numpy as np
import netCDF4 as nc
import rasterio
import re
import os

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
        data = src.read(1)               # shape: (ny, nx), dtype e.g. uint8
        transform = src.transform
        crs = src.crs
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

    # CRS scalar variable (GDAL/QGIS readable)
    crs_var = dst.createVariable("spatial_ref", "i4")
    crs_var.crs_wkt = crs.to_wkt()
    crs_var.GeoTransform = ' '.join(str(v) for v in transform.to_gdal())

    # One binary variable per class — write directly without allocating a full float array
    nodata_val = int(nodata) if nodata is not None else 255
    unique_vals = np.unique(data)
    print(f"Unique pixel values in source: {unique_vals}")

    for code, name in class_map.items():
        var = dst.createVariable(
            name, "u1",                  # uint8: values are just 0/1, saves memory
            ("time", "lat", "lon"),
            zlib=True, complevel=5,
            fill_value=255
        )
        var.grid_mapping = "spatial_ref"
        var.long_name = name
        var.class_code = code

        if code in unique_vals:
            var[0, :, :] = (data == code).view(np.uint8)   # in-place boolean → 0/1, no extra alloc
        else:
            var[0, :, :] = np.zeros((ny, nx), dtype=np.uint8)
            print(f"  code {code:>3} ({name}): not present in source, filled with 0")

    print(f"\nSaved: {dst_path}")
    dst.close()


root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/'
tif_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.tif')
netcdf_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy_per_class.nc')

tif_to_netcdf_per_class(tif_file, netcdf_file, year=2050)