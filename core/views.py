import cv2
import imutils
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from core.forms import DocumentForm
from core.models import Document


def home(request):
    """

    Parameters
    ----------
    request

    Returns
    -------

    """
    documents = Document.objects.all()

    return render(request, 'core/home.html', {'documents': documents})


def simple_upload(request):
    """

    Parameters:
        file, file_url,
        image, size_image,
        average_color_image,
        count_object_on_image,
    ----------
    request:
        Methods, Files


    Returns
        html doc,
        image, image url
        size image, average color image,
        number of coins, amount of money
    -------

    """
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # _________________________
        im = cv2.imread(filename)
        h, w = im.shape[0], im.shape[1]
        avg_color_per_row = np.average(im, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        bl_col = avg_color[0]
        gr_col = avg_color[1]
        red_col = avg_color[2]

        im = cv2.resize(im, (960, 1280))
        output = im.copy()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        # detect circles in the image
        circles = cv2.HoughCircles(
            image=gray,
            method=cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=10,
            param1=None,
            param2=110
        )
        amount_money = 0
        radius_cir = []
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
                radius_cir.append(r)
                number_obj += 1
            # show the output image
            gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 13, 15, 15)
            canny = cv2.Canny(gray, 150, 175)

            contours_c = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
            contours_c = imutils.grab_contours(contours_c)
            contours_c = sorted(contours_c, key=cv2.contourArea, reverse=True)

            # loop over the contours
            for c in contours_c:
                # approximate the contour
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)
            cv2.imwrite(filename, output)

            for i in radius_cir:
                if i < 40:
                    radius_cir.remove(i)
            radius_cir = sorted(radius_cir)
            i = number_obj - 1
            while i > -1:

                if radius_cir[i] >= 54:
                    amount_money += 5
                if (radius_cir[i] >= 49) and (radius_cir[i] < 54):
                    amount_money += 2
                if (radius_cir[i] >= 47) and (radius_cir[i] <= 48):
                    amount_money += 10
                if (radius_cir[i] >= 41) and (radius_cir[i] < 47):
                    amount_money += 1
                i -= 1

        # _________________________

        return render(request, 'core/simple_upload.html', {
            'red': red_col,
            'green': gr_col,
            'blue': bl_col,
            'uploaded_file_url': uploaded_file_url,
            'height': h,
            'width': w,
            'number_of_coins': number_obj,
            'image': uploaded_file_url,
            'amount_of_money': amount_money
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
