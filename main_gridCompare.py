import numpy as np

nx     = 32
n      = (nx+1)**2
ntiles = 6
names  = [ "XC","YC","DXF","DYF","RAC","XG","YG","DXV", "DYU","RAZ","DXC","DYC","RAW","RAS","DXG","DYG" ]

coordsDiff = []

for tile in range(1, ntiles+1):
    a = np.fromfile( f"state/grid_check/custom/tile{tile:03d}.mitgrid",   dtype=">f8" )
    b = np.fromfile( f"state/grid_check/original/tile{tile:03d}.mitgrid", dtype=">f8" )
    
    absDiff = np.abs(a - b)
    relDiff = np.divide( absDiff, np.abs(b), out = np.zeros_like(a), where = ( b != 0. ) )
    
    coordsDiff.append( { "abs" : absDiff, 
                         "rel" : relDiff } )
    
    print(f"\nTile {tile:03d}")
    print(f"Max absolute error: {absDiff.max():.6e}")
    print(f"Max relative error: {relDiff.max():.6e}")
    
    for i, name in enumerate(names):
        d = absDiff[i*n:(i+1)*n].max()
        r = relDiff[i*n:(i+1)*n].max()
        
        print(f"{name:4s}: {d:.6e}, {r:.6e}")

print('\nAcross all tiles:')

for i, name in enumerate(names):
    d = max( tile["abs"][i*n:(i+1)*n].max() for tile in coordsDiff )
    r = max( tile["rel"][i*n:(i+1)*n].max() for tile in coordsDiff )
    print(f"{name:4s}: {d:.6e}, {r:.6e}")