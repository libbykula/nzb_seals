# update: renaming latitude and longitude lat/lon here too 
import numpy as np
import xarray as xr
import netCDF4 as nc
import re


def convert_to_global_grid(input_path, output_path):

    ds = xr.open_dataset(input_path, decode_times=False)

    # Rename dimensions/coordinates if needed
    rename_dict = {}
    if "latitude" in ds.dims:
        rename_dict["latitude"] = "lat"
    if "longitude" in ds.dims:
        rename_dict["longitude"] = "lon"

    if rename_dict:
        ds = ds.rename(rename_dict)

    # Create global 0.5° grid
    new_lat = np.arange(-89.75, 90, 0.5)
    new_lon = np.arange(-179.75, 180, 0.5)

    ds_global = ds.reindex(
        lat=new_lat,
        lon=new_lon,
        fill_value=np.nan
    )

    ds_global.to_netcdf(output_path)

    print("Saved:", output_path)


def add_time_dimension_to_netcdf(src_path, dst_path):
    src = nc.Dataset(src_path)
    dst = nc.Dataset(dst_path, "w")

    classes = ['crop', 'past', 'forestry', 'primforest', 'secdforest', 'urban', 'other']
    years = [1985, 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050]

    # Create dimensions
    dst.createDimension("lat", src.dimensions['lat'].size)
    dst.createDimension("lon", src.dimensions['lon'].size)
    dst.createDimension("time", len(years))

    # Copy lat/lon
    lat = dst.createVariable("lat", "f4", ("lat",))
    lon = dst.createVariable("lon", "f4", ("lon",))
    lat[:] = src.variables.get('latitude', src.variables.get('lat'))[:]
    lon[:] = src.variables.get('longitude', src.variables.get('lon'))[:]

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
    global_path = re.sub('.nc', '_global.nc', input_path)
    convert_to_global_grid(input_path, global_path)
    
    fixed_path = re.sub('.nc', '_global_fixed.nc', input_path)
    add_time_dimension_to_netcdf(global_path, fixed_path)

run(
    input_path= "C:/Users/kibby/Files/base_data/magpie/NPI/magpie.nc",
)