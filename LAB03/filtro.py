#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import timeit


# In[ ]:


def sp_noise(image, prob):        
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output


# In[ ]:


def media_meth1(original, image_in, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.float32) / kernel_size*kernel_size
    
    if (original.dtype == 'uint8'):
        image_in = np.array(image_in, dtype=np.float32)
        image_out = cv2.filter2D(src=image_in, ddepth=-1, kernel=kernel)

        #normalização da imagem
        cv2.normalize(image_out, image_out, 0, 255, cv2.NORM_MINMAX)

        result_image = np.array(image_out, dtype=np.uint8)
    else:
        result_image = cv2.filter2D(src=image_in, ddepth=-1, kernel=kernel)

    #cálculo do PSNR
    psnr = cv2.PSNR(original, result_image)
    
    return result_image, psnr


# In[ ]:


def media_meth2(original, image_in, kernel_size):
    image_out = cv2.blur(image_in, (kernel_size, kernel_size))

    #cálculo do PSNR
    psnr = cv2.PSNR(original, image_out)
    
    return image_out, psnr


# In[ ]:


def media_meth3(original, image_in, kernel_size):
    image_out = cv2.GaussianBlur(image_in, (kernel_size, kernel_size), 0)

    #cálculo do PSNR
    psnr = cv2.PSNR(original, image_out)
    
    return image_out, psnr


# In[ ]:


def media_meth4(original, image_in, kernel_size):
    image_out = cv2.boxFilter(noisy_image, 0, (kernel_size,kernel_size))

    #cálculo do PSNR
    psnr = cv2.PSNR(original, image_out)
    
    return image_out, psnr


# In[ ]:


def mediana(original, image_in, kernel_size):
    image_out = cv2.medianBlur(image_in, kernel_size)

    #cálculo do PSNR
    psnr = cv2.PSNR(original, image_out)
    
    return image_out, psnr


# In[ ]:


def empilhamento(original, noise_level, number):
    noisy_images_list = []

    # gera as imagens com ruído a serem empilhadas
    for i in range(0,number,1):
        noise_output = sp_noise(original, noise_level)
        noisy_images_list.append(noise_output)


    result_image = np.array(noisy_images_list[0], dtype=np.uint32)
    for j in range(1,number,1):
        result_image += noisy_images_list[j]

    result_image = result_image // number
    result_image = np.array(result_image, dtype=np.uint8)
    
    #cálculo do PSNR
    psnr = cv2.PSNR(original, result_image)

    return result_image, psnr


# In[ ]:


def laplaciano(original, image_in, kernel_size):
    if (original.dtype == "uint8"):
        laplacian = cv2.Laplacian(image_in, cv2.CV_8U, ksize=kernel_size)
    else:
        laplacian = cv2.Laplacian(image_in, cv2.CV_64F, ksize=kernel_size)

    #cálculo do PSNR
    psnr = cv2.PSNR(original, laplacian)
    
    return laplacian, psnr


# In[ ]:


def sobel(original, image_in, kernel_size):
    if (original.dtype == "uint8"):
        sobelx = cv2.Sobel(noisy_image,cv2.CV_8U,1,0,ksize=kernel_size)  # x
        sobely = cv2.Sobel(noisy_image,cv2.CV_8U,0,1,ksize=kernel_size)  # y
    else:
        sobelx = cv2.Sobel(noisy_image,cv2.CV_64F,1,0,ksize=kernel_size)  # x
        sobely = cv2.Sobel(noisy_image,cv2.CV_64F,0,1,ksize=kernel_size)  # y

    #cálculo do PSNR
    psnrx = cv2.PSNR(original, sobelx)
    psnry = cv2.PSNR(original, sobely)

    if(psnrx >= psnry):
        return sobelx, psnrx
    else:
        return sobely, psnry


# In[ ]:


if __name__ == "__main__":
    #leitura da imagem de entrada
    original_image = cv2.imread(sys.argv[1])


    #leitura do nível de ruído e geração da imagem com ruído
    noise_level = float(sys.argv[2])
    noisy_image = sp_noise(original_image, noise_level)


    #definição da imagem de saída
    output_file = sys.argv[4]


    #definições de alguns parâmetros
    kernel_size = 7
    number = 120


    inicio = timeit.default_timer()
    #filtros
    if sys.argv[3] == "0": ##MÉDIA filter2D
        print("\n---METHOD: MÉDIA filter2D")
        output_image,psnr = media_meth1(original_image, noisy_image, kernel_size)


    elif sys.argv[3] == "0.1": ##MÉDIA blur
        print("\n---METHOD: MÉDIA blur")
        output_image,psnr = media_meth2(original_image, noisy_image, kernel_size)


    elif sys.argv[3] == "0.2": ##MÉDIA GaussianBlur
        print("\n---METHOD: MÉDIA GaussianBlur")
        output_image,psnr = media_meth3(original_image, noisy_image, kernel_size)


    elif sys.argv[3] == "0.3": ##MÉDIA boxFilter
        print("\n---METHOD: MÉDIA boxFilter")
        output_image,psnr = media_meth4(original_image, noisy_image, kernel_size)


    elif sys.argv[3] == "1": ##MEDIANA
        print("\n---METHOD: MEDIANA")
        output_image,psnr = mediana(original_image, noisy_image, kernel_size)


    elif sys.argv[3] == "2": ##EMPILHAMENTO
        print("\n---METHOD: EMPILHAMENTO")
        output_image,psnr = empilhamento(original_image, noise_level, number)


    elif sys.argv[3] == "3": ##LAPLACIANO
        print("\n---METHOD: LAPLACE")
        output_image,psnr = laplaciano(original_image, noisy_image, kernel_size)


    elif sys.argv[3] == "4": ##SOBEL
        print("\n---METHOD: SOBEL")
        output_image,psnr = sobel(original_image, noisy_image, kernel_size)
    
    
    fim = timeit.default_timer()


    print("\nPSNR value = ", str(psnr))
    print("EXECUTION time: %f" % (fim - inicio))
    
    cv2.imwrite(output_file, output_image)

