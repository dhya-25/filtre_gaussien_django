from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
import cv2

  
def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        # Enregistre l'image dans le système de fichiers
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # Ouvre l'image avec PIL
        im = Image.open('media/' + filename)

        # Applique le filtre gaussien
        im_array = np.array(im)
        im_filtered = cv2.GaussianBlur(im_array, (5,5), 0)

        # Convertit le tableau NumPy en image PIL
        im_filtered_pil = Image.fromarray(im_filtered)

        # Enregistre l'image filtrée dans le système de fichiers
        filtered_filename = 'filtered_' + filename
        im_filtered_pil.save('media/' + filtered_filename)

        # Transmet les informations de l'image uploadée et de l'image filtrée (si elle existe) au modèle HTML
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'filtered_file_url': fs.url(filtered_filename) if fs.exists(filtered_filename) else None
        })

    # Affiche le formulaire d'upload
    return render(request, 'upload.html')