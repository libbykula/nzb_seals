# import netCDF4
# import numpy as np

# def add_time_dimension_to_netcdf(src_path, dst_path):

#     src = netCDF4.Dataset(src_path)
#     dst = netCDF4.Dataset(dst_path, "w")
#     print(src)

#     # Define your classes and years
#     classes = ['crop', 'past', 'forestry', 'primforest', 'secdforest', 'urban', 'other']
#     years = [1985, 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050]  # adjust to match your bands

#     # Create dimensions
#     dst.createDimension("lat", src.dimensions['lat'].size)
#     dst.createDimension("lon", src.dimensions['lon'].size)
#     dst.createDimension("time", len(years))

#     # Copy lat/lon
#     lat = dst.createVariable("lat", "f4", ("lat",))
#     lon = dst.createVariable("lon", "f4", ("lon",))

#     if 'latitude' in src.variables:
#         lat[:] = src.variables['latitude'][:]
#     if 'longitude' in src.variables:
#         lon[:] = src.variables['longitude'][:]
#     if 'lat' in src.variables:
#         lat[:] = src.variables['lat'][:]
#     if 'lon' in src.variables:
#         lon[:] = src.variables['lon'][:]


#     # Create time variable
#     time_var = dst.createVariable("time", "i4", ("time",))
#     time_var[:] = years

#     # Assign each class variable
#     num_years = len(years)
#     for i, cls in enumerate(classes):
#         var = dst.createVariable(cls, "f4", ("time", "lat", "lon"))
#         for t in range(num_years):
#             band_index = i * num_years + t + 1 # because bands are stacked by class then year
#             var[t,:,:] = src.variables[f"Band{band_index}"][:]

#     src.close()
#     dst.close()

import netCDF4
import numpy as np

def add_time_dimension_to_netcdf(src_path, dst_path):
    src = netCDF4.Dataset(src_path)
    dst = netCDF4.Dataset(dst_path, "w")

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

    src.close()
    dst.close()


# add_time_dimension_to_netcdf(src_path='C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5.nc',
#                              dst_path='C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_fixed.nc')

# add_time_dimension_to_netcdf(src_path='C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc',
#                              dst_path='C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_working.nc')

add_time_dimension_to_netcdf(src_path='C:/Users/kibby/Files/base_data/magpie/NPI/magpie_working.nc',
                             dst_path='C:/Users/kibby/Files/base_data/magpie/NPI/magpie_working_fixed.nc')