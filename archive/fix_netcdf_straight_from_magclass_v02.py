import netCDF4 as nc
import numpy as np

def add_time_dimension_to_netcdf(input_file, output_file):

    src = nc.Dataset(input_file)
    dst = nc.Dataset(output_file, "w")
    # print(src)
    # print(src.variables)


    # --- read coordinates ---
    lat = src.variables["latitude"][:]
    lon = src.variables["longitude"][:]
    time = src.variables["time"][:]

    # --- create dimensions ---
    dst.createDimension("lat", len(lat))
    dst.createDimension("lon", len(lon))
    dst.createDimension("time", len(time))

    # --- create coordinate variables ---
    lat_var = dst.createVariable("lat", "f4", ("lat",))
    lon_var = dst.createVariable("lon", "f4", ("lon",))
    time_var = dst.createVariable("time", "i4", ("time",))

    lat_var[:] = lat.astype(np.float32)
    lon_var[:] = lon.astype(np.float32)
    time_var[:] = np.arange(len(time))

    # --- land class names ---
    classes = [
        "crop",
        "past",
        "forestry",
        "primforest",
        "secdforest",
        "urban",
        "other",
    ]

    # --- read MAGCLASS data ---
    data = src.variables["magpie_landclasses"][:]

    # MAGCLASS layout is usually:
    # (time, lat, lon, class)
    # adjust if needed
    if data.ndim == 4:

        for i, name in enumerate(classes):

            var = dst.createVariable(
                name,
                "f4",
                ("time", "lat", "lon"),
                zlib=True,
            )

            var[:] = data[:, :, :, i].astype(np.float32)

    else:
        raise ValueError("Unexpected MAGCLASS dimensions")

    src.close()
    dst.close()

    print("Finished writing:", output_file)

add_time_dimension_to_netcdf('C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc',
                             'C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc')