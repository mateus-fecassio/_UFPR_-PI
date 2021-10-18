#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

from matplotlib.colors import hsv_to_rgb

from glob import glob
import os
from os.path import join


# In[ ]:


def find_hMax(banana, banana_hsv, start, hMax=255, sMin=130, vMin=130):

    light_yellow = (18,sMin,vMin)
    dark_yellow = (hMax,230,255)
    mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)
    result = cv2.bitwise_and(banana, banana, mask=mask)
    h,s,v = cv2.split(result)
    var_temp = np.array([h,s,v])
    var_new = np.var(var_temp)

    var_ant = var_new
    repetitions = 0
    for i in range(start,256,1):
        light_yellow = (18,sMin,vMin)
        dark_yellow = (i,230,255)

        mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)

        result = cv2.bitwise_and(banana, banana, mask=mask)

        h,s,v = cv2.split(result)

        var_temp = np.array([h,s,v])
        var_new = np.var(var_temp)

        if ( abs( var_new - var_ant ) <= 2.0  ):
            repetitions += 1
            if (repetitions > 1):
                break
        else:
            var_ant = var_new
    # print(f"i:{dark_yellow} -- var_new = {var_new}")
    return i


# In[ ]:


def find_sMin(banana, banana_hsv, start, hMax=255, sMin=20, vMin=130):

    light_yellow = (18,sMin,vMin)
    dark_yellow = (hMax,230,255)
    mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)
    result = cv2.bitwise_and(banana, banana, mask=mask)
    h,s,v = cv2.split(result)
    var_temp = np.array([h,s,v])
    var_new = np.var(var_temp)

    var_ant = var_new
    repetitions = 0
    for i in range(start,256,1):
        light_yellow = (18,i,vMin)
        dark_yellow = (hMax,230,255)

        mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)

        result = cv2.bitwise_and(banana, banana, mask=mask)

        h,s,v = cv2.split(result)

        var_temp = np.array([h,s,v])
        var_new = np.var(var_temp)

        if ( abs( var_new - var_ant ) >= 3.0 ):
            repetitions += 1
            if (repetitions > 2):
                break
        else:
            var_ant = var_new
    # print(f"i:{light_yellow} -- var_new = {var_new}")
    return i


# In[ ]:


def find_vMin(banana, banana_hsv, start, hMax=255, sMin=125, vMin=130):

    light_yellow = (18,sMin,vMin)
    dark_yellow = (hMax,230,255)
    mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)
    result = cv2.bitwise_and(banana, banana, mask=mask)
    h,s,v = cv2.split(result)
    var_temp = np.array([h,s,v])
    var_new = np.var(var_temp)

    var_ant = var_new
    repetitions = 0
    for i in range(start,255,1):
        light_yellow = (18,sMin,i)
        dark_yellow = (hMax,230,255)

        mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)

        result = cv2.bitwise_and(banana, banana, mask=mask)

        h,s,v = cv2.split(result)

        var_temp = np.array([h,s,v])
        var_new = np.var(var_temp)

        if ( abs( var_new - var_ant ) >= 3.0 ):
            repetitions += 1
            if (repetitions > 2):
                break
        else:
            var_ant = var_new
    # print(f"i:{light_yellow} -- var_new = {var_new}")
    return i


# In[ ]:


def segmentation(banana, banana_hsv):

    hMax = find_hMax(banana, banana_hsv, start=19)
    sMin = find_sMin(banana, banana_hsv, start=18, hMax=hMax)
    vMin = find_vMin(banana, banana_hsv, start=18, hMax=hMax, sMin=sMin)

    for i in range(1,12,1):
        for j in range(1,12,1):
            hMax = find_hMax(banana, banana_hsv, start=hMax-1, hMax=hMax, sMin=sMin-5, vMin=vMin)
        sMin = find_sMin(banana, banana_hsv, start=sMin+1, hMax=hMax, sMin=sMin, vMin=vMin-1)
    for j in range(1,12,1):
        vMin = find_vMin(banana, banana_hsv, start=vMin, hMax=hMax, sMin=sMin, vMin=vMin-1)
    
    light_yellow = (16,sMin,vMin)
    dark_yellow = (hMax,245,255)
#     print(light_yellow)
#     print(dark_yellow)
    mask = cv2.inRange(banana_hsv, light_yellow, dark_yellow)

    result = cv2.bitwise_and(banana, banana, mask=mask)

    return result, 16, sMin, vMin, hMax, 245, 255


# In[ ]:


def refine_segmentation(banana, banana_hsv, hMin, sMin, vMin, hMax, sMax, vMax):
    light_yellow = (hMin, sMin, vMin)
    dark_yellow = (hMax, sMax, vMax)
    mask_y = cv2.inRange(banana_hsv, light_yellow, dark_yellow)
    
    
    light_green = (30,85,75)
    dark_green = (90,230,255)
    mask_g = cv2.inRange(banana_hsv, light_green, dark_green)
    result_g = cv2.bitwise_and(banana, banana, mask=mask_g)
    
    
    mask = mask_y + mask_g
    result_all = cv2.bitwise_and(banana, banana, mask=mask)
    
    return result_all - result_g


# In[ ]:


if __name__ == "__main__":
    #leitura da imagem de entrada
    try:
        banana = cv2.imread(sys.argv[1])
    except:
        image_in = sys.argv[1] + '.png'
        banana = cv2.imread(image_in)
    
    #segmentação
    banana = cv2.cvtColor(banana, cv2.COLOR_BGR2RGB)
    banana_hsv = cv2.cvtColor(banana, cv2.COLOR_RGB2HSV)
    image_out, hMin, sMin, vMin, hMax, sMax, vMax = segmentation(banana, banana_hsv)
    #refinamento
    image_out = refine_segmentation(banana, banana_hsv, hMin, sMin, vMin, hMax, sMax, vMax)
    
    #conversão da imagem
    image_out = cv2.cvtColor(image_out, cv2.COLOR_RGB2BGR)
    
    
    #definindo a imagem de saída
    output_list = sys.argv[2].split('.')
    if len(output_list) != 2:
        output_file = sys.argv[2] + '.png'
    else:
        output_file = sys.argv[2]
    
    
    #adicionando um blur
    image_out = cv2.GaussianBlur(image_out, (3, 3), 0)
    
    
    #salvando a imagem
    if len(sys.argv) > 3:
        if sys.argv[3] == "-1":
            original = cv2.cvtColor(banana, cv2.COLOR_RGB2BGR)
            image_out = np.concatenate((original, image_out), axis=1)

    cv2.imwrite(output_file, image_out)

