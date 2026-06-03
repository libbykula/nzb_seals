import os
import geopandas as gpd
import numpy as np
from shapely.geometry import box


# base_dir = 'D:/base_data/cartographic/ee'
base_dir = 'C:/Users/kibby/Files/base_data/cartographic/ee'

aoi = gpd.read_file(os.path.join(base_dir, "aoi_BRA_clipped_forreal.gpkg"))
bbox = aoi.total_bounds  # [minx, miny, maxx, maxy]
minx, miny, maxx, maxy = bbox

# --- Load AOI (Brazil polygon) ---
# aoi = gpd.read_file("brazil.gpkg").to_crs("EPSG:4674")   # SIRGAS / latlon
aoi = aoi.to_crs("EPSG:4674")   # SIRGAS / latlon
# A projected CRS for area calculation
AREA_CRS = "EPSG:5880"   # South America Albers Equal Area

# --- Snap bounding box to 0.25° grid ---
def snap_floor(v, step=0.25): return np.floor(v/step)*step
def snap_ceil(v, step=0.25):  return np.ceil(v/step)*step

minx, miny, maxx, maxy = aoi.total_bounds
minx = snap_floor(minx)
maxx = snap_ceil(maxx)
miny = snap_floor(miny)
maxy = snap_ceil(maxy)

# --- Parameters ---
N = 12  # number of land-equal tiles; adjust 10–20 for your needs

# --- Total land area in equal-area CRS ---
aoi_area = aoi.to_crs(AREA_CRS).area.sum()
target = aoi_area / N


# --- Build lat grid ---
lat_steps = np.arange(miny, maxy, 0.25)

tiles = []
current_ymin = miny
acc = 0

for y in lat_steps:
    y0 = y
    y1 = y + 0.25

    # Rectangular strip
    strip_rect = box(minx, y0, maxx, y1)
    strip_rect_gdf = gpd.GeoDataFrame(geometry=[strip_rect], crs="EPSG:4674")

    # Clip to Brazil land
    clipped = gpd.overlay(strip_rect_gdf, aoi, how="intersection")

    if clipped.empty:
        continue

    # Compute land area in this strip
    strip_area = clipped.to_crs(AREA_CRS).area.sum()
    acc += strip_area

    # If the accumulated area reaches target → create a tile
    if acc >= target:
        tile_rect = box(minx, current_ymin, maxx, y1)
        tiles.append(tile_rect)
        current_ymin = y1
        acc = 0

# Add final tile if needed
if current_ymin < maxy:
    tiles.append(box(minx, current_ymin, maxx, maxy))

# --- Save ---
gdf_tiles = gpd.GeoDataFrame(
    {"tile_id": range(len(tiles))},
    geometry=tiles,
    crs="EPSG:4674"
)

gdf_clipped = gpd.overlay(gdf_tiles, aoi, how="intersection")
gdf_clipped.to_file(os.path.join(base_dir, "brazil_equal_land_tiles.gpkg"), driver="GPKG")
