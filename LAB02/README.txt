-------- CABEÇALHO
ALUNO: Mateus Felipe de Cássio Ferreira
GRR: 20176123

-------- SOBRE A FORMA DE EXECUÇÃO
A execução correta do programa necessita de duas entradas: uma imagem a ser segmentada e a imagem de destino. Um exemplo de execução é semelhante a este:
python3 banana.py banana1.png b1-saida.png
Observação: após inserido a imagem de saída, caso seja passado uma flag -1, a imagem original e a segmentada serão concatenadas na saída final para melhor efeito de comparação.

-------- SOBRE O QUE FOI IMPLEMENTADO
De modo geral, o script banana.py utiliza uma medida de variação dos pontos h, s e v para aproximação dos valores de sMin, vMin e hMax . A ideia é que, ao plotar em um gráfico 3D os valores de h, s, e v de uma imagem segmentada, haverá uma maior concentração dos pontos em uma determinada região do amarelo, em detrimento da imagem original, que tem vários pontos espalhados ao longo das três dimensões.

------- SOBRE A SAÍDA DO SCRIPT
A saída do script consiste em uma imagem segmentada que será salva no segundo parâmetro passado para o script.


------- REFERÊNCIAS UTILIZADAS
[1] https://realpython.com/python-opencv-color-spaces/
[2] https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205
[3] https://www.masterclass.com/articles/how-to-use-hsv-color-model-in-photography#what-is-saturation
[4] https://docs.python.org/3/library/statistics.html

