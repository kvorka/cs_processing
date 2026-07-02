import gc
import numpy

def build_LL_grid(res):
    lon_b = numpy.arange(-180.0, 180.0+res, res).astype( numpy.float32 )
    lat_b = numpy.arange(-90.0,   90.0+res, res).astype( numpy.float32 )
    
    lon = ( lon_b[:-1] + lon_b[1:] ) / 2
    lat = ( lat_b[:-1] + lat_b[1:] ) / 2
    
    lon2d, lat2d = numpy.meshgrid( lon, lat )
    
    gc.collect(); return { 'lon'   : lon,
                           'lat'   : lat,
                           'lon_b' : lon_b,
                           'lat_b' : lat_b,
                           'lon2d' : lon2d,
                           'lat2d' : lat2d }