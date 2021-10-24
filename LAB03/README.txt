O objetivo deste laboratório é testar e comparar diferentes tipos de filtros para a remoção de ruído "salt and pepper". Para isso, utilize a imagem em anexo e crie imagens com diferentes níveis de ruído usando o código em anexo. Use como parâmetros na função sp_noise os seguintes valores: [0.01, 0.02, 0.05, 0.07, 0.1]. Desta forma, você terá 5 imagens ruidosas. 
Teste os seguintes filtros para remover esses ruídos: Media, Mediana e Empilhamento de Images. Os dois primeiros você pode usar as implementações do OpenCV. O método do empilhamento deve ser implementado por você.
Para os filtros da média e mediana, teste diferentes tamanhos de máscara. Para o filtro do empilhamento, teste diferente número de imagens com o mesmo nível de ruído e verifique qual é a quantidade de imagens que devem ser empilhadas para alcançar o melhor resultado.
Para evitar somente uma analise visual, a qual é bastante subjetiva, utilize a métrica PSNR (implementada no openCV  -  cv2.PSNR).  Quanto maior o valor do PSNR, mais similares são as imagens. Ou seja, após a filtragem, o filtro que produzir a imagem com o maior valor de PSNR, quando comparada com a imagem original, é o melhor filtro. 
Se você quiser testar outros filtros, além dos três solicitados, você pode ganhar um bonus na sua nota.
O que deve ser entregue:
•	Programa que possa ser executado na ORVAL.
•	O programa deve se chamar filtro e deve receber como parâmetro a imagem original, nível de ruído, filtro e nome da imagem de saída. Para o parâmetro filtro, utilize [0] pra media, [1] para mediana e [2] para empilhamento. Se você implementar outros filtros, utilize os valores na sequência. 
•	Relatório em PDF reportando seus experimentos, reportando quais foram os melhores filtros para os cinco níveis de ruído. 



ALGUMAS REFERÊNCIAS:
https://learnopencv.com/image-filtering-using-convolution-in-opencv/
https://www.pyimagesearch.com/2021/04/28/opencv-smoothing-and-blurring/
https://en.wikipedia.org/wiki/Kernel_(image_processing)
http://www.gpec.ucdb.br/sibgrapi2008/tutorials/tutorial-2.pdf
