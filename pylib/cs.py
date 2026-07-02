import gc
import numpy
import netCDF4

def build_CS_grid(path):
    grid_CS  = []
    
    for i in range(6):
        grid = netCDF4.Dataset( f'{path}grid.t00{i+1}.nc', 'r' )
        
        grid_CS.append( 
            { 
                'lon'     : numpy.ma.filled( grid['XC'][:,:], numpy.nan ).astype( numpy.float32 ),
                'lat'     : numpy.ma.filled( grid['YC'][:,:], numpy.nan ).astype( numpy.float32 ),
                'lon_b'   : numpy.ma.filled( grid['XG'][:,:], numpy.nan ).astype( numpy.float32 ),
                'lat_b'   : numpy.ma.filled( grid['YG'][:,:], numpy.nan ).astype( numpy.float32 ),
                'angleCS' : numpy.ma.filled( grid['AngleCS'][:,:], numpy.nan ).astype( numpy.float32 ),
                'angleSN' : numpy.ma.filled( grid['AngleSN'][:,:], numpy.nan ).astype( numpy.float32 ),
                'hfac'    : numpy.ma.filled( grid['HFacC'][:,:], numpy.nan ).astype( numpy.float32 ) 
            }
        )
    
    gc.collect(); return grid_CS

def load_CS_data(path, var, time, level=None):
    data_CS = []
    
    for i in range(6):
        with netCDF4.Dataset(path+'state.0000000000.t00'+str(i+1)+'.nc', 'r') as ds:
            if level is None:
                arr = numpy.ma.filled( ds[var][time,:,:], numpy.nan ).astype( numpy.float32 )
            else:
                arr = numpy.ma.filled( ds[var][time,level,:,:], numpy.nan ).astype( numpy.float32 )
        
        data_CS.append( arr )
    
    gc.collect(); return data_CS

def rotate_CS_data(u_CS, v_CS, grid_CS):
    u_East  = []
    v_North = []
    
    for i in range(6):
        u_C = ( u_CS[i][:,:-1] + u_CS[i][:,1:] ) / 2
        v_C = ( v_CS[i][:-1,:] + v_CS[i][1:,:] ) / 2
        
        u_East.append( grid_CS[i]['angleCS'] * u_C - grid_CS[i]['angleSN'] * v_C )
        v_North.append( grid_CS[i]['angleSN'] * u_C + grid_CS[i]['angleCS'] * v_C )
    
    gc.collect(); return u_East, v_North

def mask_CS_data(level, grid_CS, *args):
    masks = [ ( grid['hfac'][level] == 0 ) for grid in grid_CS ]
    
    for i, mask in enumerate( masks ):
        for f in args:
            f[i][mask] = numpy.nan