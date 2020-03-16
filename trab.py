# -*- coding: ISO-8859-1 -*-

import cv2
import sys
import argparse
import numpy as np

def media(m_list):
    sum = 0
    for i in range(len(m_list)):
        sum += m_list[i]
    sum = sum/len(m_list)
    return int(sum)
#FINALIZADO


def moda(m_list):
    #lista de contadores:
    l_temp = [0]*256
    
    for i in range(len(m_list)):
        index = l_temp[i]
        l_temp[index] += 1
    
    bigger = l_temp[0]
    index = 0
    for i in range(256):
        if (l_temp[i] > bigger):
            index = i
            bigger = l_temp[i]
    
    return index
#FINALIZADO


def mediana(m_list):
    m_list.sort()
    
    lenght = len(m_list)
    
    #CASO PAR
    if (lenght % 2 == 0):
        l_inf = m_list(lenght/2)
        l_sup = m_list(lenght/2 + 1)
        
        sum = (l_inf + l_sup)/2
        value = int(sum)
        
    #CASO ÍMPAR
    else:
        cut = (lenght - 1)/2
        value = m_list(cut+1)
    
    return value  
#FINALIZADO


def sampling(image, height, width, percentage, technique):
    if (percentage > 0 and percentage < 100):
        
        
        
        new_image = np.zeros((4,4), dtype=np.int)
        
        
        
    return new_image
#FAZER
    

def most_significative(histogram, l_inf, l_sup):
    if (l_inf == l_sup):
        return l_inf
    else:
        bigger = histogram[l_inf]
        
        index = 0
        for i in range(l_inf, l_sup+1):
            if (histogram[i] > bigger):
                bigger = histogram[i]
                index = i
    
    return index
#FINALIZADO          
    

def quantization(image, height, width, level):
    
    #imagem binária
    if (level == 2):
        for i in range (height):
            for j in range (width):
                value = image[i,j]
                if (value >= 0 and value <= 127):
                    image[i,j] = 0
                else:
                    image[i,j] = 255
    
    elif (level != 256):
        histogram = build_histogram(image, height, width)
        
        #construção da lista de novos valores a serem modificados
        change_list = [0]*level
        temp_list = []
        
        slice = 256 / level
        slice = int(slice)
        
        index = 0
        for i in range(0, 256, slice):
            l_inf = i
            l_sup = i + slice - 1
            
            #achar o valor mais significativo no intervalo do histograma
            value = most_significative(histogram, l_inf, l_sup)
            
            #inserir na change_list
            change_list[index] = value
            index += 1
        
        #substituição dos valores
        for i in range (height):
            for j in range (width):
                value = image[i,j]
                
                for k in range(level):
                    l_inf = k * slice
                    l_sup = l_inf + slice - 1
                    if (value >= l_inf and value <= l_sup):
                        image[i,j] = change_list[k]
                        break
            
    return image
#FINALIZADO


def build_histogram(image, height, width):
    histogram = [0]*256
    
    for i in range(height):
        for j in range(width):
            index = image[i,j]
            histogram[index] += 1
    
    return histogram
#FINALIZADO
    
    
def usage():
    print('EXEMPLOS DE FORMAS DE USO:')
    print('     - Somente quantizar: python3 trab.py -i exemplo.png(imagem) -q 2(nivel de quantizacao)')
    print('     - Somente amostrar: python3 trab.py -i exemplo.png -a 50(porcentagem de amostragem) -t media(tecnica utilizada)')
    print('     - Quantizar e amostrar: python3 trab.py -i exemplo.png -q 2 -a 50 -t media')
#FINALIZADO


def main():
    histogram = []
    
    ap = argparse.ArgumentParser()
    sys_lenght = len(sys.argv)
    
    #----------------ROTINA DE TRATAMENTO DA LINHA DE COMANDO----------------#
    if (sys_lenght < 3 or sys_lenght > 9):
        usage()
        exit()
    
    #SOMENTE QUANTIZAR
    elif (sys_lenght == 5):
        ap.add_argument("-i", "--image", required = True, help = "Path to the image")
        ap.add_argument("-q", "--quantization", required = True, help = "Level of quantization") 
        args = vars(ap.parse_args())
       
        #ABERTURA DA IMAGEM
        image = cv2.imread(args["image"], 0)
        original = cv2.imread(args["image"], 0)
        height, width = image.shape[:2]
        
        level = int(args["quantization"]) 
        image = quantization(image, height, width, level)
    
    
    #SOMENTE AMOSTRAR
    elif (sys_lenght == 7):
        ap.add_argument("-i", "--image", required = True, help = "Path to the image")
        ap.add_argument("-a", "--sampling", required = True, help = "Sampling of the image")
        ap.add_argument("-t", "--technique", required = True, help = "Technique to be performed")
        args = vars(ap.parse_args())
        
        #ABERTURA DA IMAGEM
        image = cv2.imread(args["image"], 0)
        original = cv2.imread(args["image"], 0)
        height, width = image.shape[:2]
        
        percentage = int(args["sampling"])
        technique = args["technique"]
        image = sampling(image, height, width, percentage, technique)
        
    
    
    #AMOSTRAGEM E QUANTIZAÇÃO
    elif (sys_lenght == 9):
        ap.add_argument("-i", "--image", required = True, help = "Path to the image")
        ap.add_argument("-q", "--quantization", required = True, help = "Level of quantization") 
        ap.add_argument("-a", "--sampling", required = True, help = "Sampling of the image")
        ap.add_argument("-t", "--technique", required = True, help = "Technique to be performed")
        
        #ABERTURA DA IMAGEM
        image = cv2.imread(args["image"], 0)
        original = cv2.imread(args["image"], 0)
        height, width = image.shape[:2]
        
        #amostragem
        percentage = int(args["sampling"])
        technique = args["technique"]
        image = sampling(image, height, width, percentage, technique)
        
        #quantização
        level = int(args["quantization"]) 
        image = quantization(image, height, width, level)
    
    #--------------FIM ROTINA DE TRATAMENTO DA LINHA DE COMANDO--------------#
    
    
    #APRESENTAÇÃO DOS RESULTADOS
    image = np.concatenate((original, image), axis=1)
    cv2.imshow("RESULTADO", image)
    cv2.waitKey(0)
#FINALIZADO(acho)



if __name__ == "__main__":
    main()