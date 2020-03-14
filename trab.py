import cv2
import sys
import argparse


#def quantization(image, level):
    
    
    #return new_image




def make_histogram(image, height, width):
    histogram = [0]*255
    
    for i in range(height):
        for j in range(width):
            index = image[i,j]
            histogram[index] += 1
            
    for i in histogram:
        print(i)
    
    
    
    return histogram
    
    




def main():
    histogram = []
    ap = argparse.ArgumentParser()
    
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    #ap.add_argument("-a", "--sampling", required = True, help = "Sampling of the image")
    #ap.add_argument("-t", "--technique", required = True, help = "Technique to be performed")
    #ap.add_argument("-q", "--quantization", required = True, help = "Level of quantization")
    
    args = vars(ap.parse_args())
    
    image = cv2.imread(args["image"], 0)
    height, width = image.shape[:2]
    
    #quantization()
    histogram = make_histogram(image, height, width)
    
    
    
    
    
    
    cv2.imshow("Image", image)
    cv2.waitKey(0)




if __name__ == "__main__":
    main()