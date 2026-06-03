import netCDF4 as nc
import numpy as np

def convert_to_global_grid(input_file, output_file):

    src = nc.Dataset(input_file)
    dst = nc.Dataset(output_file, "w")

    lat = src.variables["latitude"][:]
    lon = src.variables["longitude"][:]
    data = src.variables["magpie_landclasses"][:]

    classes = [
        "crop",
        "past",
        "forestry",
        "primforest",
        "secdforest",
        "urban",
        "other",
    ]

    n_layers, n_lat, n_lon = data.shape
    n_classes = len(classes)
    n_time = n_layers // n_classes

    data = data.reshape(n_classes, n_time, n_lat, n_lon)

    years = [1985, 1995, 2000, 2005, 2010, 2015, 2020,
         2025, 2030, 2035, 2040, 2045, 2050]

    # GLOBAL 0.5° GRID
    global_lat = np.arange(-89.75, 90, 0.5)
    global_lon = np.arange(-179.75, 180, 0.5)

    dst.createDimension("lat", len(global_lat))
    dst.createDimension("lon", len(global_lon))
    dst.createDimension("time", n_time)

    lat_var = dst.createVariable("lat", "f4", ("lat",))
    lon_var = dst.createVariable("lon", "f4", ("lon",))
    time_var = dst.createVariable("time", "i4", ("time",))

    lat_var[:] = global_lat
    lon_var[:] = global_lon
    time_var[:] = years

    # find index range of Brazil subset
    lat_start = np.where(np.isclose(global_lat, lat.min(), atol=0.25))[0][0]
    lat_end = lat_start + n_lat

    lon_start = np.where(np.isclose(global_lon, lon.min(), atol=0.25))[0][0]
    lon_end = lon_start + n_lon

    for i, name in enumerate(classes):

        var = dst.createVariable(
            name,
            "f4",
            ("time", "lat", "lon"),
            zlib=True,
            fill_value=np.nan
        )

        global_array = np.full((n_time, 360, 720), np.nan, dtype=np.float32)

        global_array[:, lat_start:lat_end, lon_start:lon_end] = data[i]

        var[:] = global_array

    print(dst)
    print(dst.variables["time"][:])
    src.close()
    dst.close()

    print("Finished:", output_file)


convert_to_global_grid(
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc",
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc"
)
