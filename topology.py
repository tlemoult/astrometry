from mylib.simbad import get_simbad_stars_region,get_coords_by_name
from mylib.vizier import get_gaia_stars_region,get_uca4_stars_region
from astropy import units as u
from astropy.coordinates import SkyCoord

def topo_test(center_coordinate):
# sum of flux ?
    Radius_A = 0.5 
    Radius_B = 7 

    Mag_lim = 21
    
    get_stars = get_simbad_stars_region
    names_A,coords_A,mag_A = get_stars(center_coordinate,size_arc_min=Radius_A,mag_limit = Mag_lim)
    names_B,coords_B,mag_B = get_stars(center_coordinate,size_arc_min=Radius_A,mag_limit = Mag_lim)


    print("coords = {}")
    print(f"{Radius_A=}   star QTY = {len(names_A)}")
    print(f"{Radius_B=}   star QTY = {len(names_B)}")


def main():
    topo_test(SkyCoord.from_name("HD 1001"))

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()