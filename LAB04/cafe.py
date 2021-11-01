#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scipy import ndimage
# import imutils
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from skimage.segmentation import watershed


# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)


# In[ ]:


def segmentation(image):
    shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)

    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=5)

    thresh = cv2.bitwise_not(thresh)

    segmented = cv2.bitwise_and(image, image, mask=thresh)

    return gray, thresh, segmented


# In[ ]:


def find_segments(thresh):
    # compute the exact Euclidean distance from every binary
    # pixel to the nearest zero pixel, then find peaks in this
    # distance map
    D = ndimage.distance_transform_edt(thresh)
    localMax = peak_local_max(D, indices=False, min_distance=20, labels=thresh)

    # perform a connected component analysis on the local peaks,
    # using 8-connectivity, then appy the Watershed algorithm
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask=thresh)
    # print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

    # loop over the unique labels returned by the Watershed
    # algorithm
    contours_area = []
    contours_list = []
    for label in np.unique(labels):
        # if the label is zero, we are examining the 'background'
        # so simply ignore it
        if label == 0:
            continue

        # otherwise, allocate memory for the label region and draw
        # it on the mask
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[labels == label] = 255

        # detect contours in the mask and grab the largest one
        # cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts,hier = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        contours_area.append(cv2.contourArea(c))
        contours_list.append(c)
    

    std = np.std(contours_area)
    grains = 0
    real_contours = []
    contours_area = []
    for i in range(0,len(contours_list),1):
        area = cv2.contourArea(contours_list[i])
        if area >= std:
            grains += 1
            real_contours.append(contours_list[i])
            contours_area.append(cv2.contourArea(contours_list[i]))

    media = np.mean(contours_area)
    media = int(np.floor(media))

    return grains, media, real_contours


# In[ ]:


if __name__ == "__main__":
    #leitura da imagem de entrada
    image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)

    gray, thresh, segmented = segmentation(image)

    # plt.imshow(gray)
    # plt.show()

    # plt.imshow(thresh)
    # plt.show()

    # plt.imshow(segmented)
    # plt.show()

    grains, media, contours = find_segments(thresh)

    cv2.drawContours(segmented , contours , -1 , (0 ,255 , 0) , 2)
    # plt.imshow(segmented)
    # plt.show()
    
    print('Quantidade de GRÃOS encontrdos = ', grains)
    print('Tamanho médio dos grãos encontrados (ÁREA) = ', media)
    output_file = f"{grains}-{media}-output.png"
    cv2.imwrite(output_file, segmented)