from astroquery.vizier import Vizier
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np

def get_gaia_stars_region(coordinates, radius=20 * u.arcmin, mag_limit=16.):
    def v_mag(gaia):
        G=gaia['phot_g_mean_mag']
        Gbp_Grp=gaia['bp_rp']
        V=G+0.02704-0.01424*(Gbp_Grp)+0.2156*pow(Gbp_Grp,2)-0.01426*pow(Gbp_Grp,3)
        return V
    # Set up the query to the Gaia catalog
    Gaia.ROW_LIMIT = 8000

    gaia_data = Gaia.cone_search(coordinates, radius)
    gaia_data = gaia_data.get_results()
    print(f"Gaia found {len(gaia_data)} stars")

    p = np.where(gaia_data['phot_g_mean_mag'] <= mag_limit)[0]
    gaia_data = gaia_data[p]

    gaia_data.sort('phot_g_mean_mag')
    print(f"Gaia with limited magnitude {mag_limit} is {len(gaia_data)} stars")

    names = []
    coords = []
    mag_G = []
    mag_V = []
    for row in gaia_data:
        names.append(row['source_id'])
        coords.append(SkyCoord(ra=row['ra'], dec=row['dec'], unit=(u.deg, u.deg)))
        #mag_G.append(row['phot_g_mean_mag'])
        mag_V.append(v_mag(row))
    return names,coords,mag_V

def get_uca4_stars_region(coordinates, radius=20 * u.arcmin, mag_limit=16.):
    # Set up the query to the UCAC4 catalog
    v = Vizier(columns=['UCAC4', '_RAJ2000', '_DEJ2000', 'Bmag', 'Rmag', 'Imag'], row_limit=-1)
    v.ROW_LIMIT = -1
    ucac4 = v.query_region(coordinates, radius=radius, catalog='I/322A/out')
    ucac4 = ucac4[0]
    ucac4.sort('Bmag')

    p = np.where(ucac4['Bmag'] <= mag_limit)[0]
    ucac4 = ucac4[p]

    names = []
    coords = []
    mag_G = []
    for row in ucac4:
        names.append(row['UCAC4'])
        coords.append(SkyCoord(ra=row['_RAJ2000'], dec=row['_DEJ2000'], unit=(u.deg, u.deg)))
        mag_G.append(row['Bmag'])

    return names,coords,mag_G


def topo_test(center_coordinate):
# sum of flux ?
    Radius_A = 1 * u.arcmin
    Radius_B = 5 * u.arcmin

    Mag_lim = 17
    
    names_A,coords_A,mag_A = get_uca4_stars_region(center_coordinate,radius=Radius_A,mag_limit = Mag_lim)
    names_B,coords_B,mag_B = get_uca4_stars_region(center_coordinate,radius=Radius_A,mag_limit = Mag_lim)

    print("coords = {}")
    print(f"{Radius_A=}   star QTY = {len(names_A)}")
    print(f"{Radius_B=}   star QTY = {len(names_B)}")

def main_A():

    # Define the field size
    search_radius = 5 * u.arcmin

    # Convert the target coordinates to a SkyCoord object
    target_name = "TYC 2717-453-1"
    target_coord = SkyCoord.from_name(target_name)
    target_ra = target_coord.ra.deg
    target_dec = target_coord.dec.deg


    print(f'Target: Name={target_name} RA={target_ra:.4f} deg, Dec={target_dec:.4f} deg')
    print(f'Search radius: {search_radius:.2f}')
    print('============================')

    names,coords,mags_B = get_uca4_stars_region(target_coord, radius=search_radius, mag_limit=15.)
    print(f"UCAC4  we found {len(names)} stars")
    print('============================')
    print("NAME    RA(J2000)  DEC(J2000)  Bmag")
    for name,coord,mag_B in zip(names,coords,mags_B):
        print(f"{name:<20} | {coord.ra:<20} | {coord.dec:<20} | mag={mag_B:<20}")


    names,coords,mags_G = get_gaia_stars_region(target_coord, radius=search_radius, mag_limit=16.)
    print('============================')
    print(f"Found {len(names)} source in Gaia catalog")
    print('============================')
    print("NAME    RA(J2000)  DEC(J2000)  Bmag")
    for name,coord,mag_G in zip(names,coords,mags_G):
        print(f"{name:<20} | {coord.ra:<20} | {coord.dec:<20} | mag={mag_G:<20}")


def main():

    topo_test(SkyCoord.from_name("HD 1001"))




if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()