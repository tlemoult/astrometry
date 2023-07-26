import cv2
import numpy as np
from astropy.io import fits

from mylib.display import display_image
from mylib.process import load_and_prepare

def extract_stars(image_input,threshold=18):
        # Normaliser l'image pour améliorer le contraste
    image = cv2.normalize(image_input, None, 0, 255, cv2.NORM_MINMAX)

    # Appliquer un filtre de seuillage pour détecter les étoiles
    _, thresholded = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Convertir l'image en type de données uint8
    thresholded = cv2.convertScaleAbs(thresholded, alpha=(255.0/65535.0))

    # Trouver les contours des étoiles
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extraire les coordonnées et l'intensité des étoiles
    etoiles = []
    for contour in contours:
        M = cv2.moments(contour)
        if M['m00'] > 0:
            float_precision = 2
            cx = round(M['m10'] / M['m00'],float_precision)
            cy = round(M['m01'] / M['m00'],float_precision)
            intensity = np.max(image_input[int(cy-2):int(cy+2), int(cx-2):int(cx+2)])  # Extraire l'intensité de l'étoile
            etoiles.append((cx, cy, intensity))

    return etoiles

############# main ##########"
input_file = './img/FIELD-1.fits'
#input_file = './img/FINDER-1.fits'
image = load_and_prepare(input_file)

display_image(image,'image pretraite',gamma=0.5)

etoiles = extract_stars(image)

display_image(image,title='avec les etoiles',etoiles = etoiles,gamma=0.5)

# Afficher les coordonnées et l'intensité des étoiles
for i, (cx, cy, intensity) in enumerate(etoiles):
    print(f"Étoile {i}: Coordonnées = ({cx}, {cy}), Intensité = {intensity}")

