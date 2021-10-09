# -*- coding: ISO-8859-1 -*-

#ALUNO: Mateus Felipe de Cássio Ferreira
#GRR: 20176123
#------------------------------------------


import cv2
import sys
import argparse
import numpy as np

def media(m_list):
    lenght = len(m_list)
    if (lenght == 0):
        return 0
    
    if (lenght == 1):
        return m_list[0]
    else:
        sum = 0
        for i in range(len(m_list)):
            sum += m_list[i]
        sum = sum/len(m_list)
    
        return int(sum)
#FINALIZADO


def moda(m_list):
    lenght = len(m_list)
    
    if (lenght == 0):
        return 0
    
    if (lenght == 1):
        return m_list[0]
    else:
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
    lenght = len(m_list)
    if (lenght == 0):
        return 0
    
    if (lenght == 1):
        return m_list[0]
    else:
        m_list.sort()
        
        lenght = len(m_list)
        
        #CASO PAR
        if (lenght % 2 == 0):
            l_inf = m_list[int(lenght/2)]
            l_sup = m_list[int(lenght/2 + 1)]
            
            sum = (l_inf + l_sup)/2
            value = int(sum)
            
        #CASO ÍMPAR
        else:
            cut = (lenght - 1)/2
            value = m_list(cut+1)
    
        return value  
#FINALIZADO


def verify_range(limit, x):
    #print('valor = ',x,' > limit = ',limit)
    if (x > limit):
        return limit
    else:
        return x


def values_extraction(image, h, w, x_posic, y_posic, x_factor, y_factor):
    l_inf_x = (x_posic * x_factor)
    l_sup_x = (l_inf_x + x_factor)
    #print('l_sup_x = ',l_sup_x)
    l_sup_x = verify_range(w, l_sup_x)
    
    l_inf_y = y_posic * y_factor
    l_sup_y = l_inf_y + y_factor
    #print('l_sup_y = ',l_sup_y)
    l_sup_y = verify_range(h, l_sup_y)
    
    #print('l_inf_x = ',l_inf_x, ' l_sup_x = ', l_sup_x)
    #print('l_inf_y = ',l_inf_y, ' l_sup_y = ', l_sup_y)
    temp_list = []
    for y in range(l_inf_y, l_sup_y):
        for x in range(l_inf_x, l_sup_x):
            #print('x = ',x,' y = ',y)
            value = image[y,x]
            temp_list.append(value)
    
    return temp_list
#TESTAR        
    

def sampling(image, height, width, percentage, technique):
    if (percentage > 0 and percentage < 100):
        factor = 1-(percentage/100)
        
        new_height = factor * height
        new_height = int(round(new_height))
        #print('height = ',height, 'new_height = ',new_height)
        
        new_width = factor * width
        new_width = int(round(new_width))
        #print('width = ',width, 'new_width = ',new_width)
        
        #criação da nova imagem
        new_image = np.zeros((new_height, new_width), dtype=int)
        
        
        #definição do tamanho da janela padrão e do erro a cada iteração
        x_grid = width / new_width
        x_error = x_grid
        x_grid = int(round(x_grid))
        x_grid_ori = x_grid
        
        
        
        y_grid = height / new_height
        y_error = y_grid
        y_grid = int(round(y_grid))
        y_grid_ori = y_grid
        
        
        x_error = abs(x_grid - x_error)
        x_error_ac = 0.0
        
        y_error = abs(y_grid - y_error)
        y_error_ac = 0.0
        
        #print('x_error = ', x_error, ' y_error', y_error)
        
        temp_list = []
        #INÍCIO DO PROCESSO DE AMOSTRAGEM
        for y in range(new_height):
            for x in range(new_width):
                #print(x)
                temp_list.clear()
                temp_list = values_extraction(image, height, width, x, y, x_grid, y_grid)
                
                if (technique == 'media'):
                    value = media(temp_list)
                    #value = np.mean(temp_list)
                elif (technique == 'moda'):
                    value = moda(temp_list)
                    #value = stats.mode(temp_list)
                    
                elif (technique == 'mediana'):
                    value = mediana(temp_list)
                    #value = int(np.median(temp_list))
                
                new_image[y,x] = value
                #print('new_image[',y,',',x,'] recebeu ',value)
                
                
                
                #tratamento do erro da imagem
                x_error_ac += x_error
                y_error_ac += y_error
                
                if (x_error_ac > 1.0):
                    x_grid += 1
                    x_error_ac -= 1.0
                else:
                    x_grid = x_grid_ori
                
                
                if (y_error_ac > 1):
                    y_grid += 1
                    y_error_ac -= 1.0
                else:
                    y_grid = y_grid_ori
            
    return new_image
#ERRADO, consertar
    

def most_significative(histogram, l_inf, l_sup):
    if (l_inf == l_sup):
        return l_inf
    else:
        bigger = histogram[l_inf]
        
        index = l_inf
        for i in range(l_inf, l_sup+1):
            if (histogram[i] > bigger):
                bigger = histogram[i]
                index = i
    
    return index
#FINALIZADO          
    

def quantization(image, height, width, level):
    
    #imagem binária
    if (level == 2):
        for i in range(height):
            for j in range(width):
                value = image[i,j]
                if (value >= 0 and value <= 127):
                    image[i,j] = 0
                else:
                    image[i,j] = 255
    
    elif (level != 256):
        histogram = build_histogram(image, height, width)
        
        #construção da lista de novos valores a serem modificados
        change_list = [0]*level
        
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
        for i in range(height):
            for j in range(width):
                value = image[i,j]
                
                for k in range(0, level):
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
        image = np.concatenate((original, image), axis=1)
        
        #APRESENTAÇÃO DOS RESULTADOS
        filename = 'outcome_q.png'
        cv2.imwrite(filename, image)
        cv2.imshow("OUTCOME (quantized)", image)
        cv2.waitKey(0)
    
    
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
        new_image = []
        new_image = sampling(image, height, width, percentage, technique)
        new_image = new_image.astype(np.uint8)
        
        #APRESENTAÇÃO DOS RESULTADOS
        filename = 'outcome_a.png'
        cv2.imwrite(filename, new_image)
        cv2.imshow("OUTCOME (sampled)", new_image)
        cv2.waitKey(0)
        
    
    
    #AMOSTRAGEM E QUANTIZAÇÃO
    elif (sys_lenght == 9):
        ap.add_argument("-i", "--image", required = True, help = "Path to the image")
        ap.add_argument("-q", "--quantization", required = True, help = "Level of quantization") 
        ap.add_argument("-a", "--sampling", required = True, help = "Sampling of the image")
        ap.add_argument("-t", "--technique", required = True, help = "Technique to be performed")
        args = vars(ap.parse_args())
        
        #ABERTURA DA IMAGEM
        image = cv2.imread(args["image"], 0)
        original = cv2.imread(args["image"], 0)
        height, width = image.shape[:2]
        
        #amostragem
        percentage = int(args["sampling"])
        technique = args["technique"]
        new_image = []
        new_image = sampling(image, height, width, percentage, technique)
        new_image = new_image.astype(np.uint8)
        h, w = new_image.shape[:2]
        
        
        #quantização
        level = int(args["quantization"]) 
        new_image = quantization(new_image, h, w, level)
        
        
        #APRESENTAÇÃO DOS RESULTADOS
        filename = 'outcome_a_q.png'
        cv2.imwrite(filename, new_image)
        cv2.imshow("OUTCOME (quantized and sampled)", new_image)
        cv2.waitKey(0)
    
    #--------------FIM ROTINA DE TRATAMENTO DA LINHA DE COMANDO--------------#
#FINALIZADO


if __name__ == "__main__":
    main()