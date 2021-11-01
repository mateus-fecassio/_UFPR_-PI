-------- CABEÇALHO
ALUNO: Mateus Felipe de Cássio Ferreira
GRR: 20176123

-------- SOBRE A FORMA DE EXECUÇÃO
O script cafe.py vai ler a imagem passada para fazer a segmentação e contagem dos grãos de café.
Exemplo: python3 cafe.py 70-1.jpg

-------- SOBRE O QUE FOI IMPLEMENTADO
De modo geral, o script cafe.py realiza uma segmentação de imagens com uma função de limiarização, utilizando os parâmetros THRESH_BINARY | cv2.THRESH_OTSU. Essa função está
implementada em def segmentation(image). A outra função implementada, def find_segments(thresh), utiliza um algoritmo de Watershed, um algoritmo clássico usado para segmentação de imagens, especialmente quando os elementos a serem extraídos estão se tocando ou se sobrepondo nas imagens.


------- SOBRE A SAÍDA DO SCRIPT
A saída do script consiste na impressão, na saída padrão, da quantidade de grãos de grãos encontrados e o seu tamanho médio em pixel (a área do grão). Ainda, uma imagem é salva em que o primeiro parâmetro é a quantidade de grãos encontrados seguido da área média dos grãos.
Exemplo: 
70-25691-output.png


------- REFERÊNCIAS UTILIZADAS
[1] https://www.pyimagesearch.com/2015/11/02/watershed-opencv/
[2] https://stackoverflow.com/questions/51009126/opencv-how-to-correctly-apply-morphologyex-operation#comment93355596_51043935
[3] https://www.pythonpool.com/cv2-boundingrect/
[4] https://docs.opencv.org/4.5.3/d4/d73/tutorial_py_contours_begin.html
