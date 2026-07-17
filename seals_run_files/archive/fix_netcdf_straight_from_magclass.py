import netCDF4
import numpy as np

def add_time_dimension_to_netcdf(src_path, dst_path):

    src = netCDF4.Dataset(src_path)
    dst = netCDF4.Dataset(dst_path, "w")

    print(src)
    # Define your classes and years
    # classes = ['crop', 'past', 'forestry', 'primforest', 'secdforest', 'urban', 'other']
    years = [1985, 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050]  # adjust to match your bands

    # # Create dimensions
    # dst.createDimension("lat", src.dimensions['latitude'].size)
    # dst.createDimension("lon", src.dimensions['longitude'].size)
    # dst.createDimension("time", src.dimensions['time'].size)

    # # Copy lat/lon
    # lat = dst.createVariable("lat", "f4", ("lat",))
    # lon = dst.createVariable("lon", "f4", ("lon",))
    # lat[:] = src.variables['lat'][:]
    # lon[:] = src.variables['lon'][:]

    # # Create time variable
    # time_var = dst.createVariable("time", "i4", ("time",))
    # time_var[:] = years

    # # Assign each class variable
    # num_years = len(years)
    # for i, cls in enumerate(classes):
    #     var = dst.createVariable(cls, "f4", ("time", "lat", "lon"))
    #     for t in range(num_years):
    #         band_index = i * num_years + t + 1 # because bands are stacked by class then year
    #         var[t,:,:] = src.variables[f"Band{band_index}"][:]

    # src.close()
    # dst.close()


# add_time_dimension_to_netcdf(src_path='C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5.nc',
                            #  dst_path='C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_fixed.nc')

add_time_dimension_to_netcdf(src_path='C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc',
                             dst_path='C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_magclass_fixed.nc')