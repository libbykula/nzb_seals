from osgeo import gdal

raster_path = "D:/base_data/pyramids/ha_per_cell_1sec.tif"

ds = gdal.Open(raster_path)
if ds is None:
    print("Raster could not be opened (possibly corrupted).")
else:
    print("Driver:", ds.GetDriver().ShortName)
    print("Size:", ds.RasterXSize, ds.RasterYSize)
    print("Bands:", ds.RasterCount)
    print("Projection:", ds.GetProjection())
    
    band = ds.GetRasterBand(1)
    stats = band.GetStatistics(True, True)
    print("Band 1 statistics:", stats)  # [min, max, mean, stddev]
    ds = None
