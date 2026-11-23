# Flappy Falcon

Um jogo de **Flappy Bird inspirado em Star Wars**, feito em Python com PyGame para o projeto final de Design de Software (Insper).

Você pilota a Millennium Falcon por cinco planetas, desvia de obstáculos, abre portões de energia acertando alvos e, no final, enfrenta o chefão **Resina Vader** na Estrela da Morte.

## Autores

- Davi Moreira ([@davirmoreira](https://github.com/davirmoreira))
- Isabela Serra ([@Isabelaserra001](https://github.com/Isabelaserra001))

## Vídeo de demonstração

[**ASSISTIR AO VÍDEO**]
(https://drive.google.com/file/d/1HLfTRhut6TJpImYX-8e-5bdyZG6FFNRu/view?usp=sharing)

## Como rodar

**Requisitos:** Python 3 e a biblioteca PyGame.

### Opção 1: clonar com Git

1. Abra o terminal na pasta onde quer colocar o jogo e rode:
   ```
   git clone https://github.com/davirmoreira/Flappy-Falcon.git
   ```
2. Entre na pasta do jogo:
   ```
   cd Flappy-Falcon
   ```
3. Instale o PyGame (só na primeira vez):
   ```
   pip install pygame
   ```
4. Rode o jogo:
   ```
   python main.py
   ```

### Opção 2: baixar o ZIP (sem precisar do Git)

1. No GitHub, clique no botão verde **Code** e depois em **Download ZIP**.
2. Descompacte o arquivo. Será criada uma pasta chamada `Flappy-Falcon-main`.
3. Abra o terminal **dentro dessa pasta** (a que contém `main.py`, `imagens` e `sons`). Pelo terminal: `cd Flappy-Falcon-main`. Ou abra a pasta no VS Code (Arquivo → Abrir Pasta).
4. Instale o PyGame (só na primeira vez) e rode o jogo:
   ```
   pip install pygame
   python main.py
   ```

> **Importante:** rode o comando **dentro da pasta do projeto**, onde estão `main.py` e as pastas `imagens` e `sons`. Se tiver uma pasta com o mesmo nome dentro da outra depois de descompactar, entre na de dentro. Se o `python` não funcionar, tente `python3 main.py` (e `python3 -m pip install pygame`).

Para jogar sem imagens ou sem sons, mude `USAR_IMAGENS` e `USAR_SONS` para `False` no arquivo `config.py`.

## Como jogar

| Tecla | O que faz |
|---|---|
| **ESPAÇO** | Pular (e avançar nos menus) |
| **R** | Atirar |
| **F** | Liga e desliga a tela cheia |

- Escolha um dos 3 pilotos na tela de seleção:
  - **Davi Skywalker**: cai mais devagar.
  - **Lucasbacca**: começa com 4 vidas.
  - **Enzo Solo**: atira mais rápido.
- Passe pelos canos sem encostar neles nem no chão. Cada batida custa uma vida.
- Alguns canos vêm **trancados por um portão vermelho**: atire (R) no alvo que aparece antes do cano para abrir o portão.
- São 6 canos em cada planeta: **Tatooine, Naboo, Mustafar, Endor e Kamino** (30 canos no total).
- No final, derrote o **Resina Vader** na Estrela da Morte atirando nele enquanto ele se move na plataforma e desvia dos tiros dele.
- Vença o chefão para assistir à cena final e chegar à tela de vitória.

## Estrutura do projeto

| Arquivo | O que tem |
|---|---|
| `main.py` | Laço principal do jogo e troca de telas |
| `config.py` | Constantes, cores, pilotos e cenários (dificuldade) |
| `recursos.py` | Carregamento de imagens e sons |
| `efeitos.py` | Partículas, explosões e enfeites dos cenários |
| `nave.py` | A nave (Millennium Falcon + piloto) e os lasers |
| `obstaculos.py` | O alvo e o cano com portão de energia |
| `chefe.py` | O chefão Resina Vader |
| `logica.py` | Regras do jogo, quadro a quadro |
| `telas.py` | Tudo o que é desenhado (menu, seleção, jogo, fim, cena e vitória) |
| `imagens/` | Imagens do jogo |
| `sons/` | Músicas e efeitos sonoros |

O jogo usa classes (`Nave`, `Laser`, `Alvo`, `Cano`, `Chefe`, `Particula`, `Boom`, `Enfeite`), funções, listas, dicionários e máquina de estados ("menu", "selecao", "jogando", "cena", "fim", "vitoria").

## Uso de IA e créditos

**Ferramentas usadas:** Claude (Anthropic) para o código e ChatGPT (OpenAI) para imagens e sons. O professor autorizou o uso de outras ferramentas de IA além da institucional.

| Parte do projeto | Quanto foi gerado por IA | Histórico |
| --- | --- | --- |
| Código (todos os arquivos `.py`) | Cerca de 100%, a partir de instruções nossas (ideia do jogo, personagens, regras, ajustes e correções). Nós testamos, pedimos mudanças e organizamos o repositório | https://claude.ai/share/03d0d3a3-0888-4053-8c14-9ffa2d48350b |
| Imagens (`imagens/`) | 100% geradas com IA, depois recortadas (fundo verde removido) e redimensionadas por código. As cabeças dos pilotos (`cabeca_*.png`) foram recortadas por nós 
| Sons (`sons/`) | 100% gerados com IA. As músicas foram convertidas de WAV para OGG 

**Como usamos a IA:** pedimos o código aos poucos, testamos o jogo, reportamos erros e pedimos correções. Revisamos o que foi gerado e estudamos todo o código para conseguir explicá-lo.

**Código de terceiros:** não copiamos código da internet nem de colegas.

**Créditos:** Star Wars é marca da Lucasfilm/Disney. Os personagens, planetas e a Millennium Falcon aparecem aqui apenas como inspiração, em um projeto acadêmico sem fins lucrativos.
