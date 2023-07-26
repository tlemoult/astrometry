def display_image(image,title='',etoiles=[],colored = False,gamma = 1,rectangle=False,rect_size=(100,100),rect_center=(150,150)):
    import matplotlib.pyplot as plt
    import numpy as np

    # Appliquer une correction gamma à l'image
    image_corr = np.power(image, gamma)

    # Afficher l'image corrigée à l'aide de Matplotlib
    plt.imshow(image_corr, cmap='gray')

    croix_x = [etoile[0] for etoile in etoiles]
    croix_y = [etoile[1] for etoile in etoiles]
    
    #
    if colored:
        intensites = [etoile[2] for etoile in etoiles]
        plt.scatter(croix_x, croix_y, marker='+',  s=100, c=intensites, cmap='viridis')
    else:
        plt.scatter(croix_x, croix_y, marker='+',  s=100, color='red')

    if rectangle:
        # Ajouter un rectangle superposé à l'image
        size_x, size_y = rect_size
        rect_top = (rect_center[0]-size_x/2 , rect_center[1]-size_y/2)
        rectangle = plt.Rectangle(rect_top, size_x, size_y, linewidth=2, edgecolor='blue', facecolor='none')
        plt.gca().add_patch(rectangle)

    plt.axis('off')
    plt.title(title)
    plt.show()