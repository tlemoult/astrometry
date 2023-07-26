import cv2
import numpy as np
from astropy.io import fits

def load_and_prepare(filepath):

    # Charger l'image FITS
    hdul = fits.open(filepath)
    image = hdul[0].data.astype(np.uint16)  # Convertir en type de données entier non signé 16 bits



    # Appliquer un flou gaussien pour estimer le fond de l'image
    ksize = 31 # Taille du noyau de flou gaussien
    sigma = 0 # Ecart-type du noyau de flou gaussien (0 signifie que la valeur est calculée automatiquement)
    image_blur = cv2.GaussianBlur(image, (ksize, ksize), sigma)

    # Soustraire le fond de l'image pour obtenir l'image corrigée
    image_corrected = cv2.subtract(image, image_blur)

    # Appliquer un filtre médian pour atténuer le bruit
    ksize_median = 3 # Taille du noyau de filtre médian
    image_median = cv2.medianBlur(image_corrected, ksize_median)

    return image_median