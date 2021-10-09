#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np

from glob import glob
import os
from os.path import join
import pandas as pd


# In[ ]:


def list_images():
    cwd = os.getcwd()
    
    files = []
    for ext in ('*.jpg', '*.png'):
        #files.extend(glob(join(cwd, ext)))
        files.extend(glob(ext))
    
    return files


# In[ ]:


def get_class(parse):
    str_list = []

    str_list = parse.split('1')
    str_list = str_list[0].split('2')

    return str_list[0]


# In[ ]:


def verify_hit(class_1, class_2):
    if (class_1 == class_2):
        return 1
    else:
        return 0


# In[ ]:


def compare_hist_colored_images(files):
    df = pd.DataFrame()
    for i in range(0,len(files),1):
        temporary = []
        dic_correl = {}
        dic_chisqr = {}
        dic_intersect = {}
        dic_bhattacharyya = {}
        
        selected_image = cv2.imread(files[i])
        selected_image = cv2.cvtColor(selected_image, cv2.COLOR_BGR2RGB)
        selected_image_class = get_class(files[i])
        

        CORREL_hit, correl_max, CHISQR_hit, chisqr_min, INTERSECT_hit, intersect_max, BHATTACHARYYA_hit, bhattacharyya_min = 0, 0, 0, 0, 0, 0, 0, 0
        for f in range(0,len(files),1):
            if (i != f):
                # print(files[i], files[f])
                compared_image = cv2.imread(files[f])
                compared_image = cv2.cvtColor(compared_image, cv2.COLOR_BGR2RGB)
                
                hist1 = cv2.calcHist([selected_image], [0,1,2], None, [8,8,8], [0,256,0,256,0,256])
                hist2 = cv2.calcHist([compared_image], [0,1,2], None, [8,8,8], [0,256,0,256,0,256])
                cv2.normalize(hist1, hist1, 0, 255, cv2.NORM_MINMAX)
                cv2.normalize(hist2, hist2, 0, 255, cv2.NORM_MINMAX)


                CORREL = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                CHISQR = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
                INTERSECT = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
                BHATTACHARYYA = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)


                # print("CORREL = ", CORREL)
                # print("CHISQR = ", CHISQR)
                # print("INTERSECT = ", INTERSECT)
                # print("BHATTACHARYYA = ", BHATTACHARYYA)
                # print("\n")
                

                dic_correl[files[f]] = CORREL
                dic_chisqr[files[f]] = CHISQR
                dic_intersect[files[f]] = INTERSECT
                dic_bhattacharyya[files[f]] = BHATTACHARYYA

        
        
        correl_max = max(dic_correl, key=dic_correl.get)
        CORREL_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(correl_max))


        chisqr_min = min(dic_chisqr, key=dic_chisqr.get)
        CHISQR_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(chisqr_min))


        intersect_max = max(dic_intersect, key=dic_intersect.get)
        INTERSECT_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(intersect_max))


        bhattacharyya_min = min(dic_bhattacharyya, key=dic_bhattacharyya.get)
        BHATTACHARYYA_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(bhattacharyya_min))


        temporary.append(files[i])
        temporary.append(CORREL_hit)
        temporary.append(CHISQR_hit)
        temporary.append(INTERSECT_hit)
        temporary.append(BHATTACHARYYA_hit)
        # print(temporary)

        temp_df = pd.DataFrame(temporary).transpose()
        df = pd.concat([df, temp_df], axis=0, ignore_index=True)


    df = df.rename(columns=({0:'IMAGE NAME',
                        1:'CORREL hit',
                        2:'CHISQR hit',
                        3:'INTERSECT hit',
                        4:'BHATTACHARYYA hit'}))

    sum_df = pd.DataFrame( [[ 'TOTAL GERAL', sum(df['CORREL hit']), sum(df['CHISQR hit']), sum(df['INTERSECT hit']), sum(df['BHATTACHARYYA hit']) ]], columns=['IMAGE NAME', 'CORREL hit', 'CHISQR hit', 'INTERSECT hit', 'BHATTACHARYYA hit'] )
    df = pd.concat([df, sum_df], axis=0, ignore_index=True)

    df.set_index('IMAGE NAME', inplace=True)
    return df


# In[ ]:


def compare_hist_gray_images(files):
    df = pd.DataFrame()
    for i in range(0,len(files),1):
        temporary = []
        dic_correl = {}
        dic_chisqr = {}
        dic_intersect = {}
        dic_bhattacharyya = {}
        
        selected_image = cv2.imread(files[i],0)
        selected_image_class = get_class(files[i])
        

        CORREL_hit, correl_max, CHISQR_hit, chisqr_min, INTERSECT_hit, intersect_max, BHATTACHARYYA_hit, bhattacharyya_min = 0, 0, 0, 0, 0, 0, 0, 0
        for f in range(0,len(files),1):
            if (i != f):
                # print(files[i], files[f])
                compared_image = cv2.imread(files[f],0)
                
                hist1 = cv2.calcHist([selected_image], [0], None, [256], [0,256])
                hist2 = cv2.calcHist([compared_image], [0], None, [256], [0,256])
                cv2.normalize(hist1, hist1, 0, 255, cv2.NORM_MINMAX)
                cv2.normalize(hist2, hist2, 0, 255, cv2.NORM_MINMAX)


                CORREL = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                CHISQR = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
                INTERSECT = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
                BHATTACHARYYA = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)


                # print("CORREL = ", CORREL)
                # print("CHISQR = ", CHISQR)
                # print("INTERSECT = ", INTERSECT)
                # print("BHATTACHARYYA = ", BHATTACHARYYA)
                # print("\n")
                

                dic_correl[files[f]] = CORREL
                dic_chisqr[files[f]] = CHISQR
                dic_intersect[files[f]] = INTERSECT
                dic_bhattacharyya[files[f]] = BHATTACHARYYA

        
        
        correl_max = max(dic_correl, key=dic_correl.get)
        CORREL_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(correl_max))


        chisqr_min = min(dic_chisqr, key=dic_chisqr.get)
        CHISQR_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(chisqr_min))


        intersect_max = max(dic_intersect, key=dic_intersect.get)
        INTERSECT_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(intersect_max))


        bhattacharyya_min = min(dic_bhattacharyya, key=dic_bhattacharyya.get)
        BHATTACHARYYA_hit = verify_hit( class_1 = selected_image_class, class_2 = get_class(bhattacharyya_min))


        temporary.append(files[i])
        temporary.append(CORREL_hit)
        temporary.append(CHISQR_hit)
        temporary.append(INTERSECT_hit)
        temporary.append(BHATTACHARYYA_hit)
        # print(temporary)

        temp_df = pd.DataFrame(temporary).transpose()
        df = pd.concat([df, temp_df], axis=0, ignore_index=True)


    df = df.rename(columns=({0:'IMAGE NAME',
                        1:'CORREL hit',
                        2:'CHISQR hit',
                        3:'INTERSECT hit',
                        4:'BHATTACHARYYA hit'}))

    sum_df = pd.DataFrame( [[ 'TOTAL GERAL', sum(df['CORREL hit']), sum(df['CHISQR hit']), sum(df['INTERSECT hit']), sum(df['BHATTACHARYYA hit']) ]], columns=['IMAGE NAME', 'CORREL hit', 'CHISQR hit', 'INTERSECT hit', 'BHATTACHARYYA hit'] )
    df = pd.concat([df, sum_df], axis=0, ignore_index=True)

    df.set_index('IMAGE NAME', inplace=True)
    return df


# In[ ]:


if __name__ == "__main__":
    files = list_images()

    df_colored = compare_hist_colored_images(files)
    print("-------------- OUTPUT COMPARISON FOR COLORED IMAGES --------------")
    print(df_colored)

    print("\n\n")

    df_gray = compare_hist_gray_images(files)
    print("-------------- OUTPUT COMPARISON FOR GRAY IMAGES --------------")
    print(df_gray)
    

