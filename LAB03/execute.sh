#!/bin/bash

python3 filtro.py original.png 0.1 0 saida-filter2d.png
python3 filtro.py original.png 0.1 0.1 saida-blur.png
python3 filtro.py original.png 0.1 0.1 saida-GaussianBlur.png
python3 filtro.py original.png 0.1 0.1 saida-boxFilter.png


python3 filtro.py original.png 0.1 1 saida-mediana.png

python3 filtro.py original.png 0.1 2 saida-empilhamento.png

python3 filtro.py original.png 0.1 3 saida-laplace.png

python3 filtro.py original.png 0.1 4 saida-sobel.png



