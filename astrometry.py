from astroquery.astrometry_net import AstrometryNet
from astropy.coordinates import SkyCoord
from astropy import wcs
from mylib.display import display_image
from mylib.process import load_and_prepare

from mylib.astrometry import astrometrySolve,load_wcs_from_file
from mylib.simbad import get_simbad_stars_region,get_coords_by_name

fixStars = False
if fixStars:
    stars_name = ["BD+29 4467",  "TYC 2717-453-1",'BD+30 4492','BD+29 4460']
    stars_coord = get_coords_by_name(stars_name)
else:
    center_star_name = "TYC 2717-453-1"
    print(f"{center_star_name=}")
    center_coords = SkyCoord.from_name(center_star_name)
    stars_name , stars_coord, stars_mag = get_simbad_stars_region(center_coords,size_arc_min=10,Vmag=13.5)
    print(f"{stars_name=}")

# astrometrySolve('./img/FINDER-1.fits','wcs.fits')
w = load_wcs_from_file('wcs.fits')

stars_pix = []

for name,star_coord in zip(stars_name,stars_coord):
    star_pix = w.all_world2pix(star_coord.ra,star_coord.dec,0)
    stars_pix.append(star_pix)
    print(f"{name=} , {star_coord=} , {star_pix=} ")

filepath = './img/FINDER-1.fits'
image_corrected = load_and_prepare(filepath)

# pepare field rectangle of the spectrograph
field_pixel_center = (793,503)
field_x_arcmin = 12
field_y_arcmin = 10
scalex,scaley = wcs.utils.proj_plane_pixel_scales(w)
field_pixel_size = (field_x_arcmin/60/scalex , field_y_arcmin/60/scaley)


display_image(image_corrected,etoiles=stars_pix,gamma=0.5,
              rectangle=True,rect_center=field_pixel_center, rect_size=field_pixel_size)
