import warnings
warnings.filterwarnings( 'ignore', message='.*ESMF and ESMPy.*' )

import os
import gc
import numpy
import xesmf

def build_regridder(grid_CS, grid_LL, path, use_weights, method):
    regridders  = []
    weights_dir = f'{path}xesmfweights'
    
    os.makedirs( weights_dir, exist_ok=True )
    reuse_weights = use_weights and all( os.path.exists(f'{weights_dir}/wght.t00{i+1}.nc') for i in range(6) )
    
    for i in range(6):
        regridders.append( 
            xesmf.Regridder( 
                ds_in=grid_CS[i],
                ds_out=grid_LL,
                method=method,
                unmapped_to_nan=True,
                filename=f'{weights_dir}/wght.t00{i+1}.nc',
                reuse_weights=reuse_weights 
            ) 
        )
    
    return regridders

def regrid(regridder, data_CS, grid_LL):
    data_out = numpy.full( ( grid_LL['lat'].size, 
                             grid_LL['lon'].size), numpy.nan, dtype=numpy.float32 )
    
    for i in range(6):
        data = regridder[i]( data_CS[i], skipna=True )
        mask = ~numpy.isnan( data )
        data_out[mask] = data[mask]
    
    gc.collect(); return data_out