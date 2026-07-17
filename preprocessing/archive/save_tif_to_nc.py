# Python code

# Necessary imports
import rasterio
import xarray as xr
import numpy as np

# Function to convert GeoTIFF to NetCDF
def tif_to_netcdf(tif_file, netcdf_file, variable_name='data'):
    """
    Reads a GeoTIFF file and saves it as a NetCDF file.

    Parameters:
        tif_file (str): Path to input GeoTIFF
        netcdf_file (str): Path to output NetCDF file
        variable_name (str): Variable name for NetCDF
    """

    # Open the GeoTIFF using rasterio
    with rasterio.open(tif_file) as src:
        # Read the first band
        data = src.read(1)
        
        # Create coordinate arrays from transform
        transform = src.transform
        ny, nx = data.shape
        x = np.array([transform.c + i*transform.a for i in range(nx)])
        y = np.array([transform.f + j*transform.e for j in range(ny)])

    # Create an xarray DataArray
    da = xr.DataArray(data,
                      coords={'y': y, 'x': x},
                      dims=['y', 'x'],
                      name=variable_name)
    
    # Save as NetCDF
    da.to_netcdf(netcdf_file)
    print(f"Saved NetCDF file: {netcdf_file}")

# Example usage
tif_file = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.tif'      # replace with your input file
netcdf_file = 'C:/Users/kibby/Files/base_data/lulc_esa_gtap1/stitched_lulc_esa_scenarios_rcp26/rcp26/lulc_esa_gtap1_rcp26_ssp1_2050_no_policy.nc'    # replace with your desired output file
tif_to_netcdf(tif_file, netcdf_file)