-------- CABEÇALHO
ALUNO: Mateus Felipe de Cássio Ferreira
GRR: 20176123


-------- SOBRE AS FORMAS DE USO
EXEMPLOS DE FORMAS DE USO:
- Somente quantizar: python3 trab.py -i exemplo.png(imagem) -q 2(nivel de quantizacao)
- Somente amostrar: python3 trab.py -i exemplo.png -a 50(porcentagem de amostragem) -t media(tecnica utilizada)
- Quantizar e amostrar: python3 trab.py -i exemplo.png -q 2 -a 50 -t media

Ou, é possível digitar     python3 trab.py -h     para ajuda




-------- SOBRE O QUE FOI IMPLEMENTADO
-- def quantization(image, height, width, level): essa função recebe como parâmetros a imagem, as suas dimensões e o nível de escala de cinza de saída. Essa função procura no histograma original da imagem a cor mais significativa,
ou seja, aquela cor que mais se repet no conjunto de dados. Sendo assim, essa função pode demorar um pouco a executar quanto mair for o valor de entrada para a escala de cinza.


-- def media(m_list)
-- def moda(m_list)
-- def mediana(m_list)
Funções que recebem como parâmetro uma lista e devolvem um inteiro (de 0 a 255)


-- def sampling(image, height, width, percentage, technique): Função que recebe como parâmetro a imagem, dimensões, percentual de redução e técnica empregada. Essa função calcula as novas dimensões da imagem e o tamanho da janela base, que pode mudar de tamanho conforme o acúmulo de erro. Infelizmente não foi possível implementar a função para valores muito distantes de 50 e muito quebrados.




------- SOBRE A SAÍDA DO PROGRAMA
A saída do programa é mostrada na tela do usuário e um arquivo é salvo no diretório atual no momento da execução.


