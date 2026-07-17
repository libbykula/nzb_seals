import numpy as np
import xarray as xr


def convert_to_global_grid(input_path, output_path):

    ds = xr.open_dataset(input_path, decode_times=False)

    # define global 0.5° grid
    new_lat = np.arange(-89.75, 90, 0.5)
    new_lon = np.arange(-179.75, 180, 0.5)

    ds_global = ds.reindex(
        latitude=new_lat,
        longitude=new_lon,
        method=None,
        fill_value=np.nan
    )

    ds_global.to_netcdf(output_path)

    print("Saved:", output_path)


convert_to_global_grid(
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc",
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc"
)


