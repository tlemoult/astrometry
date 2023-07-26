from astroquery.astrometry_net import AstrometryNet
from astropy import wcs
from astropy.io import fits
from astropy import units as u

def astrometrySolve(input_file,ouput_file):
    ast = AstrometryNet()
    scale= 5.77

    print(f"start to solve {input_file}")
    wcs_header = ast.solve_from_image(input_file)

    if wcs_header:
        print(f"Sucess solving, save result in {ouput_file}")
        wcs_header.tofile(ouput_file)

    else:
        print("failed to solve")


def load_wcs_from_file(filename):
    # Load the FITS hdulist using astropy.io.fits
    hdulist = fits.open(filename)

    # Parse the WCS keywords in the primary HDU
    w = wcs.WCS(hdulist[0].header)

    print(f"wcs scales= {wcs.utils.proj_plane_pixel_scales(w)}  with cuint={w.wcs.cunit}")

    return w

    # Print out the "name" of the WCS, as defined in the FITS header
    print(w.wcs.name)

    # Print out all of the settings that were parsed from the header
    w.wcs.print_contents()

def tranfom_pixel_coord_finder_to_guider(w, positions_pixel, guider_spec= 
                                         { 'img_size' : (1200,800), 
                                          'scale_arcsec_per_pixel': 1.8, 
                                          'center_in_finder': (793,503)
                                          } ):
    finder_scale_x,finder_scale_y = wcs.utils.proj_plane_pixel_scales(w)
    # we get scale in deg per pixel,  we transform to arc sec per pixel
    finder_scale_x = finder_scale_x * 3600
    finder_scale_y = finder_scale_y * 3600
    print(f"finder scales: {finder_scale_x=}  {finder_scale_y=}")

    guider_positions = []
    for x,y in positions_pixel:
        nx = (x - guider_spec['center_in_finder'][0]) * (finder_scale_x / guider_spec['scale_arcsec_per_pixel'])
        ny = (y - guider_spec['center_in_finder'][1]) * (finder_scale_y / guider_spec['scale_arcsec_per_pixel'])

        nx = nx + guider_spec['img_size'][0]/2
        ny = ny + guider_spec['img_size'][1]/2

        if ( 0 <= nx < guider_spec['img_size'][0] and 0 <= ny < guider_spec['img_size'][1]):
            guider_positions.append((nx,ny))

    return guider_positions

