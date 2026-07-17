import rasterio
import xarray as xr
import numpy as np
import pyproj
import os

def tif_to_netcdf_compressed(tif_file, netcdf_file, variable_name='data'):
    with rasterio.open(tif_file) as src:
        data = src.read(1)
        transform = src.transform
        crs = src.crs
        nodata = src.nodata
        dtype = src.dtypes[0]
        ny, nx = data.shape

        x = np.array([transform.c + (i + 0.5) * transform.a for i in range(nx)])
        y = np.array([transform.f + (j + 0.5) * transform.e for j in range(ny)])

    # Only replace with NaN if dtype is float AND nodata is not representable as-is
    # For integer dtypes (like uint8 with nodata=255), just leave the values alone —
    # _FillValue in the encoding tells readers which value means "no data"
    if nodata is not None and np.issubdtype(np.dtype(dtype), np.floating):
        # In-place replacement to avoid allocating a second full array
        data[data == nodata] = np.nan

    da = xr.DataArray(
        data,                        # no .astype() — already the right dtype from rasterio
        coords={'y': y, 'x': x},
        dims=['y', 'x'],
        name=variable_name
    )

    da['x'].attrs.update({'axis': 'X', 'long_name': 'longitude', 'units': 'degrees_east',  'standard_name': 'longitude'})
    da['y'].attrs.update({'axis': 'Y', 'long_name': 'latitude',  'units': 'degrees_north', 'standard_name': 'latitude'})
    da.attrs['grid_mapping'] = 'spatial_ref'

    if nodata is not None:
        da.attrs['missing_value'] = nodata

    ds = da.to_dataset()

    crs_wkt = crs.to_wkt()
    ds['spatial_ref'] = xr.DataArray(0)
    ds['spatial_ref'].attrs['crs_wkt']           = crs_wkt
    ds['spatial_ref'].attrs['spatial_ref']       = crs_wkt
    ds['spatial_ref'].attrs['GeoTransform']      = ' '.join(str(v) for v in transform.to_gdal())
    ds['spatial_ref'].attrs['grid_mapping_name'] = pyproj.CRS(crs_wkt).to_cf()['grid_mapping_name']

    encoding = {
        variable_name: {
            'zlib': True,
            'complevel': 5,
            'dtype': dtype,
            '_FillValue': int(nodata) if nodata is not None and np.issubdtype(np.dtype(dtype), np.integer) else nodata
        }
    }

    ds.to_netcdf(netcdf_file, encoding=encoding)
    print(f"Saved compressed NetCDF: {netcdf_file}")
    print(f"  Pixel size : {transform.a:.6f} x {transform.e:.6f}")
    print(f"  Origin     : ({transform.c:.6f}, {transform.f:.6f})")
    print(f"  NoData     : {nodata}")
    print(f"  Dtype      : {dtype}")
    print(f"  Shape      : {ny} rows x {nx} cols")

root_path = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/'
tif_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.tif')      # replace with your input file
netcdf_file = os.path.join(root_path, 'lulc_esa_gtap1_rcp26_ssp1_2050_no_policy_v03.nc')    # replace with your desired output file

tif_to_netcdf_compressed(tif_file, netcdf_file)