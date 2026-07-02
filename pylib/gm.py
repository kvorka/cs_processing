import numpy
import pygmt

def max_in_list(data):
    return numpy.max( [ numpy.max( numpy.abs( data[t] ) ) for t in range( len(data) ) ] )

def data_to_fig(x, y, z, proj, frame, outf, cpallete, maxmin, namefig):
    fig = pygmt.Figure()
    
    pygmt.config( MAP_FRAME_PEN='1.0p,black' )
    pygmt.config( MAP_GRID_PEN='0.5p,gray60')

    if ( maxmin is not None ):
        pygmt.makecpt( cmap = cpallete, 
                       series = [-maxmin, maxmin],
                       background = True )
    else:
        pygmt.makecpt( cmap = cpallete, 
                    series = [-numpy.max( numpy.abs(z) ), +numpy.max( numpy.abs(z) )],
                    background = True )
    
    region = [ x.min(), x.max(),
               y.min(), y.max() ]
    
    spacing = [ numpy.abs( x[1,0] - x[0,0] ),
                numpy.abs( y[0,1] - y[0,0] ) ]
    
    grid = pygmt.xyz2grd( x = numpy.ravel(x),
                          y = numpy.ravel(y),
                          z = numpy.ravel(z),
                          spacing = spacing,
                          region = region )
    
    fig.colorbar( position='JMR+w6c/0.4c+v+o-2c/-4.5c', frame=['a', '+lcm/s'] )
    
    fig.grdimage( region = region,
                  projection = proj,
                  frame = frame,
                  grid = grid )
    
    if ( namefig is not None ):
        fig.savefig( namefig )
    else:
        fig.show()

def gmt_LL(grid_LL, data_LL, maxmin=None, namefig=None):
    x, y = numpy.meshgrid( grid_LL['lon']+180,
                           grid_LL['lat'], indexing='ij')
    
    z = numpy.nan_to_num( numpy.transpose(data_LL), nan=0 )
    
    data_to_fig( x=x,
                 y=y,
                 z=z,
                 proj='W180/12',
                 frame=['WSne+t '+namefig, 'g30', 'ya30'],
                 outf='gmtplot.pdf',
                 cpallete='vik',
                 maxmin=maxmin,
                 namefig=namefig )