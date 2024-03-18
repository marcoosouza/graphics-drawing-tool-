# Graphics Drawing Tool

Este projeto é uma implementação em Python de um conjunto de algoritmos de Computação Gráfica. Ele inclui algoritmos para transformações geométricas 2D, rasterização de retas e circunferências, e também, algoritmos de recorte.

# Estrutura do Projeto

* **main.py:** Este é o ponto de entrada principal para o algoritmo. Ele inicia a aplicação.
* **components/:** Esta pasta contém os principais componentes da aplicação, incluindo a janela principal, o canvas de desenho e a janela de transformações
* **assts/:** Aqui estão localizadas as imagens dos ícones usados na interface gráfica.
* **utils/:** Esta pasta contém alguns códigos utilitários adicionais que são usados no projeto.

# Funcionalidades

O projeto possui as seguintes funcionalidades principais:

* **Transformações Geométricas 2D:** Permite ao usuário realizar translação, rotação, escala e reflexões nos objetos desenhados na tela, com fatores de transformação fornecidos interativamente.

* **Rasterização de Retas e Circunferências:** Oferece a capacidade de desenhar retas e circunferências na área de desenho usando os algoritmos DDA e Bresenham.

* **Recorte de Regiões:** Implementa o algoritmo de recorte de Cohen-Sutherland para recortar linhas parcialmente ou totalmente fora da janela de visualização.
Também é implementado o algoritmo de recorte de Liang-Barsky para recortar linhas parcialmente ou totalmente fora da janela de visualização.

# Como Usar:

Para usar esta aplicação, siga estas etapas:

1. Clone o repositório para o seu ambiente local.
2. Certifique-se de ter o Python instalado em sua máquina.
3. Navegue até o diretório 1ue tenha o executável do projeto (graphics-drawing-tool-/computer-graphics/dist)
4. Se tiver no windows clique no main.exe se tiver no linux clique no executável no outro executável.*
5. Use a interface gráfica para interagir com os algoritmos e desenhar objetos na área de desenho.
6. Caso surja alguma dúvida em como utilizar a aplicação veja os videos que estão na pasta videos/

*Caso o programa não rode ao clicar no executável, a alternativa é executar manualmente o arquivo main.py no terminal ou em uma IDE.