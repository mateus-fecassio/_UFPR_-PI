-------- CABEÇALHO
ALUNO: Mateus Felipe de Cássio Ferreira
GRR: 20176123

-------- SOBRE A FORMA DE EXECUÇÃO
Para executar basta somente executar o script histograma.py, que vai ler as imagens presentes no mesmo diretório do script.
python3 histograma.py

-------- SOBRE O QUE FOI IMPLEMENTADO
De modo geral, o script histograma.py utiliza uma imagem dentro das treze imagens disponíveis restantes para classificação de um personagem. Existem duas funções principais implementadas para fazer essa classificação, que são:
- compare_hist_colored_images()
- compare_hist_gray_images()


------- SOBRE A SAÍDA DO SCRIPT
A saída do script consiste em três tabelas que são impressas na saída padrão (stdout). O número 1 significa que, para a imagem apresentada de um determinado personagem, determinada métrica conseguiu classificar corretamente o personagem em questão tomando o segundo personagem como referência. O valor zero representa o fato de que determinada métrica não conseguiu classificar corretamente.

RESPOSTAS:
1. Quantas imagens foram classificadas corretamente usando cada uma das distâncias?
-- PARA IMAGENS COLORIDAS (comparação com todos os canais RGB):
CORREL = 10
CHISQR = 10
INTERSECT = 8
BHATTACHARYYA = 14

-- PARA IMAGENS EM NÍVEIS DE CINZA:
CORREL = 7
CHISQR = 7
INTERSECT = 2
BHATTACHARYYA = 8

Em um outro teste feito, antes da comparação e construção do histograma das imagens no nível de cinza, decidi testar o efeito da equalização do histograma de todas as imagens para verificar se o acerto pudesse ser maior. Os resultados foram:
-- PARA IMAGENS EM NÍVEIS DE CINZA (com normalização do histograma):
CORREL = 1
CHISQR = 1
INTERSECT = 3
BHATTACHARYYA = 1

2. O desempenho usando imagens coloridas e em nível de cinza foi o mesmo? Se não, porque?
Não. O desempenho de todos as métricas foi pior em comparação a imagens coloridas. Isso pode ser explicado em função de que a cor entre os personagens é uma característica que contrasta muito bem entre a maioria dos personagens. Uma vez que utilizamos três canais de cores (RGB), a comparação entre os histogramas permite identificar personagens que destoam dos demais, como é o caso do Magneto por exemplo (que conseguiu ser classificado corretamente utilizando todos as métricas). Em alguns casos, em função da mudança de posição (e mudança da luminosidade e, consequentemente, o tom de cor da imagem), alguns personagens não foram classificados corretamente. Além disso, a presença de uma arma na mão, ou a posição dela na imagem, interferiu em alguns personagens para determinadas métricas.
Quando trabalhamos apenas em um canal, com tons de cinza que variam de 0 a 255, a comparação dos histogramas não permitiu uma melhor identificação dos personagens, justamente por não conseguir distinguir muito bem, em tons de cinza, as características marcantes de determinados personagens entre os demais. Essas características foram perdidas ainda mais após a equalização global dos histogramas, que obteve um desempenho inferior ao método sem equalização.


------- REFERÊNCIAS UTILIZADAS
[1] https://www.pyimagesearch.com/2021/01/23/splitting-and-merging-channels-with-opencv/
[2] https://www.pythonpool.com/cv2-normalize/
[3] https://theailearner.com/tag/cv2-comparehist/
[4] https://medium.com/@rndayala/image-histograms-in-opencv-40ee5969a3b7
[5] https://www.pyimagesearch.com/2014/07/14/3-ways-compare-histograms-using-opencv-python/
