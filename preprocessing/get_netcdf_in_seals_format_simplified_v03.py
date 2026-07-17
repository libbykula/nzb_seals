import numpy as np
import netCDF4 as nc
import rasterio
import re
import os

# Mapping from pixel value → variable name
class_map = {
    1: 'urban',
    2: 'cropland',
    3: 'grassland',
    4: 'forest',
    5: 'othernat',
    6: 'water',
    7: 'other'
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

# simp_rcp26_root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_simplified_scenarios_rcp26/rcp26/'
# simp_rcp26_tif = os.path.join(simp_rcp26_root_path, 'lulc_seals7_gtap1_rcp26_ssp1_2050_no_policy_esp.tif')
# simp_rcp26_nc = os.path.join(simp_rcp26_root_path, 'lulc_seals7_gtap1_rcp26_ssp1_2050_no_policy_esp.nc')

# baseline_root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/'
# baseline_tif = os.path.join(baseline_root_path, 'lulc_esa_2015_esp.tif')
# baseline_nc = os.path.join(baseline_root_path, 'lulc_esa_2015_esp.nc')

# tif_to_netcdf_per_class(baseline_tif, baseline_nc, year=2015) # do they all have to be in the same netcdf? I don't think so, right?

rcp85_root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_simplified_scenarios_rcp85/rcp85'
rcp85_tif = os.path.join(rcp85_root_path, 'lulc_seals7_gtap1_rcp85_ssp5_2050_no_policy_esp.tif')
rcp85_nc = os.path.join(rcp85_root_path, 'lulc_seals7_gtap1_rcp85_ssp5_2050_no_policy_esp.nc')
tif_to_netcdf_per_class(rcp85_tif, rcp85_nc, year=2050) # do they all have to be in the same netcdf? I don't think so, right?