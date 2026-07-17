import rasterio
import xarray as xr
import numpy as np
import os

def tif_to_netcdf_compressed(tif_file, netcdf_file, variable_name='data'):
    with rasterio.open(tif_file) as src:
        data = src.read(1)
        transform = src.transform
        crs = src.crs                    # <-- capture CRS
        ny, nx = data.shape
        x = np.array([transform.c + i * transform.a for i in range(nx)])
        y = np.array([transform.f + j * transform.e for j in range(ny)])

    da = xr.DataArray(
        data,
        coords={'y': y, 'x': x},
        dims=['y', 'x'],
        name=variable_name
    )

    # Write CF-convention attributes so QGIS can interpret the grid
    da.attrs['grid_mapping'] = 'spatial_ref'
    da['x'].attrs.update({'axis': 'X', 'long_name': 'longitude', 'units': 'degrees_east'})
    da['y'].attrs.update({'axis': 'Y', 'long_name': 'latitude',  'units': 'degrees_north'})

    ds = da.to_dataset()

    # Attach the CRS as a scalar coordinate variable (CF convention)
    import pyproj
    crs_wkt = crs.to_wkt()
    ds['spatial_ref'] = xr.DataArray(0)   # scalar placeholder
    ds['spatial_ref'].attrs['crs_wkt']         = crs_wkt
    ds['spatial_ref'].attrs['spatial_ref']     = crs_wkt   # GDAL also reads this
    ds['spatial_ref'].attrs['grid_mapping_name'] = pyproj.CRS(crs_wkt).to_cf()['grid_mapping_name']

    encoding = {variable_name: {'zlib': True, 'complevel': 5}}
    ds.to_netcdf(netcdf_file, encoding=encoding)
    print(f"Saved compressed NetCDF: {netcdf_file}")

root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/'
tif_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.tif')      # replace with your input file
netcdf_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy_v02.nc')    # replace with your desired output file

tif_to_netcdf_compressed(tif_file, netcdf_file)