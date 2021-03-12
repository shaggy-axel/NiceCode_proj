from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

import os

from core.models import Document
from core.forms import DocumentForm

import numpy as np
import cv2


def home(request):
    documents = Document.objects.all()

    return render(request, 'core/home.html', {'documents': documents})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # _________________________
        im = cv2.imread(filename)

        avg_color_per_row = np.average(im, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        red_col = avg_color[0]
        gr_col = avg_color[1]
        bl_col = avg_color[2]

        height, width = im.shape[0], im.shape[1]
        output = im.copy()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # detect circles in the image
        circles = cv2.HoughCircles(
            image=gray,
            method=cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=10,
            param1=None,
            param2=155
        )
        number_obj = 0
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                number_obj += 1
            # show the output image

            cv2.imwrite(filename, output)
        # _________________________

        return render(request, 'core/simple_upload.html', {
            'red': red_col,
            'green' : gr_col,
            'blue': bl_col,
            'uploaded_file_url': uploaded_file_url,
            'height': height,
            'width': width,
            'number_of_coins': number_obj,
            'image': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
