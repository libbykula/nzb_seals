# update: renaming latitude and longitude lat/lon here too 
import numpy as np
import xarray as xr


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


convert_to_global_grid(
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses.nc",
    "C:/Users/kibby/Files/base_data/magpie/NPI/magpie_landclasses_fixed.nc"
)
