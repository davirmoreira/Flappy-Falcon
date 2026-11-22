"""Carrega as imagens e os sons uma vez so e guarda tudo nos dicionarios IMAGENS e SONS."""
import pygame
from config import *


# ======================================================================
# IMAGENS E SONS (sao carregados uma vez, no comeco do programa)
# ======================================================================
IMAGENS = {}  # nome -> imagem (ou lista de imagens, no caso do fogo)
SONS = {}  # nome -> efeito sonoro
AUDIO = {"musica": ""}  # qual musica esta tocando agora ("" = nenhuma)


def carrega_recursos():
    """Le as imagens da pasta imagens e os sons da pasta sons (precisa da janela ja criada)."""
    if USAR_IMAGENS:
        IMAGENS["falcon"] = pygame.image.load("imagens/falcon.png").convert_alpha()
        quadros = []
        for i in range(1, 5):
            quadros.append(pygame.image.load(f"imagens/fogo_{ESTILO_FOGO}_{i}.png").convert_alpha())
        IMAGENS["fogo"] = quadros
        for nome in ("davi", "lucas", "enzo", "vader"):
            IMAGENS[nome] = pygame.image.load(f"imagens/{nome}.png").convert_alpha()
        for nome in ("davi", "lucas", "enzo"):  # cabecas que aparecem para fora da nave
            IMAGENS["cabeca_" + nome] = pygame.image.load(f"imagens/cabeca_{nome}.png").convert_alpha()
        quadros_pai = []  # os 4 quadros da cena "Eu sou seu pai"
        for i in range(1, 5):
            quadros_pai.append(pygame.image.load(f"imagens/pai_{i}.png").convert_alpha())
        IMAGENS["pai"] = quadros_pai
        for cenario in CENARIOS:  # um cano (boca + corpo) e um fundo para cada cenario
            nome = cenario["arquivo"]
            IMAGENS["cano_boca_" + nome] = pygame.image.load(f"imagens/cano_{nome}_boca.png").convert_alpha()
            IMAGENS["cano_corpo_" + nome] = pygame.image.load(f"imagens/cano_{nome}_corpo.png").convert_alpha()
            IMAGENS["fundo_" + nome] = pygame.image.load(f"imagens/fundo_{nome}.png").convert()
        nome = CENARIO_CHEFE["arquivo"]
        IMAGENS["fundo_" + nome] = pygame.image.load(f"imagens/fundo_{nome}.png").convert()
        for nome in ("alvo", "coracao_cheio", "coracao_vazio", "laser_azul", "laser_vermelho",
                     "plataforma", "logo", "portao_topo", "portao_base", "portao_corpo_1", "portao_corpo_2"):
            IMAGENS[nome] = pygame.image.load(f"imagens/{nome}.png").convert_alpha()
        quadros_explosao = []  # os 5 quadros da explosao
        for i in range(1, 6):
            quadros_explosao.append(pygame.image.load(f"imagens/explosao_{i}.png").convert_alpha())
        IMAGENS["explosao"] = quadros_explosao
        # coracao branco: o coracao que acabou de ser perdido pisca
        coracao_branco = IMAGENS["coracao_cheio"].copy()
        coracao_branco.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGB_ADD)
        IMAGENS["coracao_branco"] = coracao_branco
        # versao clarinha do chefao, usada quando ele leva um tiro
        branco = IMAGENS["vader"].copy()
        branco.fill((170, 170, 170, 0), special_flags=pygame.BLEND_RGB_ADD)
        IMAGENS["vader_branco"] = branco
    sombra = pygame.Surface((LARGURA, ALTURA))  # camada preta, usada para escurecer a tela
    sombra.fill(PRETO)
    IMAGENS["sombra"] = sombra
    if USAR_SONS:
        for nome in ("tiro", "pulo", "alvo", "explosao", "dano", "chefe_dano", "chefe_tiro", "vitoria", "gameover"):
            SONS[nome] = pygame.mixer.Sound(f"sons/{nome}.wav")
            SONS[nome].set_volume(VOLUME_EFEITOS)


def toca(nome):
    """Toca um efeito sonoro uma vez (se o jogo estiver com som)."""
    if nome in SONS:
        SONS[nome].play()


def toca_musica(nome):
    """Troca a musica de fundo, so se for diferente da atual. nome = "" para silencio."""
    if not USAR_SONS or AUDIO["musica"] == nome:
        return
    AUDIO["musica"] = nome
    pygame.mixer.music.stop()
    if nome != "":
        pygame.mixer.music.load(f"sons/{nome}.ogg")
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.play(-1)  # -1 = repete para sempre
