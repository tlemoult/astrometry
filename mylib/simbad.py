from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u

def get_simbad_stars_region(center_coords,size_arc_min=30,mag_limit=10):
    coords_str = center_coords.to_string('hmsdms')
    criteria = 'region(box,'+coords_str+ f', {size_arc_min}m {size_arc_min}m) & Vmag<{mag_limit}'
    print(f"get_stars_region() with {criteria=}")
    Simbad.add_votable_fields("flux(V)", "ra", "dec")
    result_table = Simbad.query_criteria(criteria)
    names = []
    coords = []
    magV = []
    if result_table is not None:
        for row in result_table:
            name = row['MAIN_ID']
            names.append(name)

            result_table = Simbad.query_object(name)
            vmag = result_table["FLUX_V"].data[0]
            magV.append(vmag)

            coords.append(SkyCoord(ra=row['RA'], dec=row['DEC'], unit=(u.hourangle, u.deg)))
    return names,coords,magV

def get_coords_by_name(stars_name):
    coords = []
    for name in stars_name:
        coords.append(SkyCoord.from_name(name))
    return coords