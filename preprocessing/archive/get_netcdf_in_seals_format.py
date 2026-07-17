import numpy as np
import xarray as xr
import netCDF4 as nc
import re
import os

class_list = ["crop_rainfed",
    "crop_rainfed_herb",
    "crop_rainfed_tree",
    "crop_irrigated",
    "crop_natural_mosaic",
    "natural_crop_mosaic",
    "tree_broadleaved_evergreen",
    "tree_broadleaved_deciduous_closed_to_open_15",
    "tree_broadleaved_deciduous_closed_40",
    "tree_broadleaved_deciduous_open_15_40",
    "tree_needleleaved_deciduous_closed_to_open_15",
    "tree_needleleaved_evergreen_closed_to_open_15_extended",
    "tree_needleleaved_evergreen_open_15_40",
    "tree_needleleaved_deciduous_closed_to_open_15",
    "tree_needleleaved_deciduous_closed_40",
    "tree_needleleaved_deciduous_open_15_40",
    "tree_mixed_type",
    "mosaic_tree_and_shrub_50_herbaceous_cover_50",
    "mosaic_herbaceous_cover_50_tree_and_shrub_50",
    "othernat",
    "evergreen_othernat",
    "deciduous_othernat",
    "grassland",
    "lichens_and_mosses",
    "sparse_vegetation_tree_shrub_herbaceous_cover_15",
    "sparse_tree_15",
    "sparse_shrub_15",
    "sparse_herbaceous_cover_15",
    "tree_cover_flooded_fresh_or_brakish_water",
    "tree_cover_flooded_saline_water",
    "shrub_or_herbaceous_cover_flooded_fresh_saline_brakish_water",
    "urban_areas",
    "bare_areas",
    "consolidated_bare_areas",
    "unconsolidated_bare_areas",
    "water_bodies",
    "permanent_snow_and_ice"]

def add_time_dimension_to_netcdf(src_path, dst_path):
    src = nc.Dataset(src_path)
    dst = nc.Dataset(dst_path, "w")

    classes = class_list
    years = [2050]

    # Create dimensions
    dst.createDimension("lat", src.dimensions['y'].size)
    dst.createDimension("lon", src.dimensions['x'].size)
    dst.createDimension("time", len(years))

    # Copy lat/lon
    lat = dst.createVariable("lat", "f4", ("lat",))
    lon = dst.createVariable("lon", "f4", ("lon",))
    lat[:] = src.variables.get('latitude', src.variables.get('y'))[:]
    lon[:] = src.variables.get('longitude', src.variables.get('x'))[:]

    # Create time variable
    time_var = dst.createVariable("time", "i4", ("time",))
    time_var[:] = years

    # Identify source variable (assume only one 3D variable if not named Band)
    data_vars = [v for v in src.variables if len(src.variables[v].shape) == 2 or len(src.variables[v].shape) == 3]
    # if multiple 3D variables, pick the first non-lat/lon
    data_var_name = [v for v in data_vars if v not in ['lat', 'lon', 'latitude', 'longitude']][0]
    data = src.variables[data_var_name][:]  # shape could be (bands, lat, lon)

    num_years = len(years)
    for i, cls in enumerate(classes):
        var = dst.createVariable(cls, "f4", ("time", "lat", "lon"))
        for t in range(num_years):
            band_index = i * num_years + t  # zero-indexed
            var[t,:,:] = data[band_index,:,:]
    
    print("Saved:", dst_path)

    src.close()
    dst.close()

def run(input_path):
    fixed_path = re.sub('.nc', '_fixed.nc', input_path)
    add_time_dimension_to_netcdf(input_path, fixed_path)


root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/'
netcdf_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy_v03.nc')    # replace with your desired output file

run(
    input_path= netcdf_file,
)