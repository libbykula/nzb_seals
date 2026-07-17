import rasterio
import xarray as xr
import numpy as np
import os

def tif_to_netcdf_compressed(tif_file, netcdf_file, variable_name='data'):
    with rasterio.open(tif_file) as src:
        data = src.read(1)  # Read first band
        transform = src.transform
        ny, nx = data.shape
        x = np.array([transform.c + i*transform.a for i in range(nx)])
        y = np.array([transform.f + j*transform.e for j in range(ny)])

    da = xr.DataArray(data,
                      coords={'y': y, 'x': x},
                      dims=['y', 'x'],
                      name=variable_name)

    # Specify compression options
    encoding = {variable_name: {'zlib': True, 'complevel': 5}}  # zlib compression, level 1–9

    da.to_netcdf(netcdf_file, encoding=encoding)
    print(f"Saved compressed NetCDF file: {netcdf_file}")

# Example usage
root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/'
tif_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.tif')      # replace with your input file
netcdf_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.nc')    # replace with your desired output file

tif_to_netcdf_compressed(tif_file, netcdf_file)