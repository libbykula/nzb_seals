import netCDF4 as nc
import numpy as np
import hazelbean as hb

# def convert_to_global_grid(input_file, output_file):

#     src = nc.Dataset(input_file)
#     dst = nc.Dataset(output_file, "w")
#     lat = src.variables["latitude"][:]
#     lon = src.variables["longitude"][:]
#     data = src.variables["cell_land_0_5_magclass"][:]

#     classes = [
#         "crop",
#         "past",
#         "forestry",
#         "primforest",
#         "secdforest",
#         "urban",
#         "other",
#     ]

#     n_layers, n_lat, n_lon = data.shape
#     n_classes = len(classes)
#     n_time = n_layers // n_classes

#     data = data.reshape(n_classes, n_time, n_lat, n_lon)

#     years = [1985, 1995, 2000, 2005, 2010, 2015, 2020,
#          2025, 2030, 2035, 2040, 2045, 2050]

#     # GLOBAL 0.5° GRID
#     global_lat = np.arange(-89.75, 90, 0.5)
#     global_lon = np.arange(-179.75, 180, 0.5)

#     dst.createDimension("lat", len(global_lat))
#     dst.createDimension("lon", len(global_lon))
#     dst.createDimension("time", n_time)

#     lat_var = dst.createVariable("lat", "f4", ("lat",))
#     lon_var = dst.createVariable("lon", "f4", ("lon",))
#     time_var = dst.createVariable("time", "i4", ("time",))

#     lat_var[:] = global_lat
#     lon_var[:] = global_lon
#     time_var[:] = years

#     # find index range of Brazil subset
#     lat_start = np.where(np.isclose(global_lat, lat.min(), atol=0.25))[0][0]
#     lat_end = lat_start + n_lat

#     lon_start = np.where(np.isclose(global_lon, lon.min(), atol=0.25))[0][0]
#     lon_end = lon_start + n_lon

#     for i, name in enumerate(classes):

#         var = dst.createVariable(
#             name,
#             "f4",
#             ("time", "lat", "lon"),
#             zlib=True,
#             fill_value=np.nan
#         )

#         global_array = np.full((n_time, 360, 720), np.nan, dtype=np.float32)

#         global_array[:, lat_start:lat_end, lon_start:lon_end] = data[i]

#         var[:] = global_array

#     print(dst)
#     print(dst.variables["time"][:])
#     src.close()
#     dst.close()

#     print("Finished:", output_file)


# convert_to_global_grid(
#     "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc",
#     "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc"
# )


# convert_to_global_grid(
#     "C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_magclass.nc",
#     "C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_magclass_global.nc"
# )

def rename_lat_long(input_file):
    src = nc.Dataset(input_file, 'r+')

    # Get coordinate variable names
    coord_names = list(src.variables.keys())
    
    if 'latitude' in src.dimensions:
        src.renameDimension('latitude', 'lat')
    if 'longitude' in src.dimensions:
        src.renameDimension('longitude', 'lon')

    src.close()
    # dst.close()

# rename_lat_long("C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_magclass.nc")
import netCDF4 as nc
import numpy as np

def make_global_bb(input_file, output_file):

    with nc.Dataset(input_file, 'r') as src:

        # Select first timestep → now becomes (lat, lon)
        data_in = src.variables["cell_land_0_5_magclass"][0, :, :]

        with nc.Dataset(output_file, 'w') as dst:

            dst.createDimension('lat', 180)
            dst.createDimension('lon', 360)

            var = dst.createVariable('data', 'f4', ('lat', 'lon'), fill_value=-9999.)
            var[:] = -9999.

            nlat, nlon = data_in.shape
            var[0:nlat, 0:nlon] = data_in


# make_global_bb("C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_magclass.nc",
#                "C:/Users/kibby/Files/base_data/magpie/NPI/cell_land_0_5_magclass_global.nc")