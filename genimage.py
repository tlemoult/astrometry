from mylib.simbad import get_simbad_stars_region,get_coords_by_name
from mylib.vizier import get_gaia_stars_region,get_uca4_stars_region
from mylib.astrometry import load_wcs_from_file,tranfom_pixel_coord_finder_to_guider
from mylib.display import display_image
from mylib.process import load_and_prepare
import numpy as np
from astropy import units as u
import astroalign as aa

center_star_name = "TYC 2717-453-1"
print(f"{center_star_name=}")
center_coords = get_coords_by_name([center_star_name])[0]
#stars_name , stars_coord, stars_magV = get_simbad_stars_region(center_coords,size_arc_min=10,mag_limit=15)
#stars_name , stars_coord, stars_magV = get_uca4_stars_region(center_coords,radius=10* u.arcmin,mag_limit=15)
stars_name , stars_coord, stars_magV = get_gaia_stars_region(center_coords,radius=7* u.arcmin,mag_limit=13.5)
print(f"Found {len(stars_name)} stars")

#for names,coord,mag in zip(stars_name,stars_coord,stars_magV):
#    print(f"{names=}  {coord.ra.hms=} {coord.dec.dms=}  {mag=}")

# get position of stars in finder 
w = load_wcs_from_file('wcs.fits')
stars_finder_pix = []
for coord, mag in zip(stars_coord, stars_magV):
    star_finder_pix = w.all_world2pix(coord.ra,coord.dec,0)
    stars_finder_pix.append(star_finder_pix)

#generate guider image
guider_spec=  { 'img_size' : (752,580), 
                 'scale_arcsec_per_pixel': 0.9, 
                  'center_in_finder': (793,503)
            }
stars_guider_pix = tranfom_pixel_coord_finder_to_guider(w,stars_finder_pix,guider_spec=guider_spec)
print(f"We have {len(stars_guider_pix)} stars inside the field")

img_shape = guider_spec['img_size']
img = np.zeros((img_shape[1],img_shape[0]))


for star_guider_pix, mag in zip(stars_guider_pix, stars_magV):
    img[int(star_guider_pix[1]),int(star_guider_pix[0])] = pow(10,mag/2.5)

from scipy.ndimage import gaussian_filter
img = gaussian_filter(img, sigma=2.0, mode='constant')
display_image(img,title='generated field',gamma=0.2)

img_real = load_and_prepare('./img/FIELD-1.fits')
display_image(img_real,title='observed field',gamma=0.5)

#img_aligned, footprint = aa.register( img_real,img)

