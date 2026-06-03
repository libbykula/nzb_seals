import netCDF4 as nc
import numpy as np

def adjust_netcdf(input_file, output_file):

    src = nc.Dataset(input_file)
    dst = nc.Dataset(output_file, "w")

    lat = src.variables["latitude"][:]
    lon = src.variables["longitude"][:]

    data = src.variables["magpie_landclasses"][:]  
    # shape: (layers, lat, lon)

    n_layers, n_lat, n_lon = data.shape

    classes = [
        "crop",
        "past",
        "forestry",
        "primforest",
        "secdforest",
        "urban",
        "other",
    ]

    n_classes = len(classes)
    n_time = n_layers // n_classes

    data = data.reshape(n_classes, n_time, n_lat, n_lon)

    dst.createDimension("lat", n_lat)
    dst.createDimension("lon", n_lon)
    dst.createDimension("time", n_time)

    lat_var = dst.createVariable("lat", "f4", ("lat",))
    lon_var = dst.createVariable("lon", "f4", ("lon",))
    time_var = dst.createVariable("time", "i4", ("time",))

    lat_var[:] = lat[::-1].astype(np.float32)
    lon_var[:] = lon.astype(np.float32)

    time_var[:] = np.arange(n_time)

    for i, name in enumerate(classes):

        var = dst.createVariable(
            name,
            "f4",
            ("time","lat","lon"),
            zlib=True
        )

        # original shape: (time, lat, lon)
        arr = data[i]

        # flip north/south
        arr = arr[:, ::-1, :]

        # ensure correct orientation
        arr = np.transpose(arr, (0, 1, 2))

        var[:] = arr.astype(np.float32)

    print(src)
    print(dst)
    src.close()
    dst.close()

    print("Finished writing:", output_file)


adjust_netcdf(
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc",
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc"
)
