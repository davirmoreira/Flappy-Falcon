"""Flappy Falcon - Star Wars + Flappy Bird.

Para jogar, abra o terminal NA PASTA DESTE ARQUIVO (onde estao as pastas imagens e sons)
e rode: python3 main.py

Teclas: ESPACO (pular) e R (atirar). F liga e desliga a tela cheia.
"""
import pygame
from config import *
from recursos import carrega_recursos, toca, toca_musica
from efeitos import *
from nave import *
from obstaculos import *
from chefe import *
from logica import *
from telas import *

# ======================================================================
# PROGRAMA PRINCIPAL
# ======================================================================
pygame.init()
# SCALED estica o jogo (800x600) para a janela/tela sem deformar, o que permite a tela cheia
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.SCALED)
if COMECAR_EM_TELA_CHEIA:
    pygame.display.toggle_fullscreen()
pygame.display.set_caption("Flappy Falcon")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 30)
fonte_pequena = pygame.font.SysFont(None, 26)
fonte_grande = pygame.font.SysFont(None, 60)
carrega_recursos()  # imagens e sons

escolhido = 0  # personagem selecionado na tela de selecao
jogo = novo_jogo(PERSONAGENS[escolhido])
enfeites_menu = cria_enfeites("estrelas")  # estrelas do menu, da selecao e da vitoria
nave_menu = Nave(PERSONAGENS[0])  # so para desenhar a nave passeando no menu
estado = "menu"  # "menu", "selecao", "jogando", "fim" ou "vitoria"
estado_anterior = estado
tempo = 0  # quadros desde que o programa abriu
tempo_estado = 0  # quadros desde que entrou no estado atual
rodando = True

while rodando:
    relogio.tick(FPS)
    tempo += 1
    tempo_estado += 1

    # ---------- eventos: fechar a janela e as teclas ----------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_f or evento.key == pygame.K_F11:  # F (ou F11) liga e desliga a tela cheia
                pygame.display.toggle_fullscreen()
            if estado == "jogando":
                if jogo["resultado"] == "":  # depois do fim, a nave nao responde mais
                    if evento.key == pygame.K_SPACE:
                        jogo["nave"].pula(jogo["particulas"])
                    if evento.key == pygame.K_r:
                        jogo["nave"].atira(jogo["lasers"])
            elif estado == "selecao":
                if evento.key == pygame.K_r:
                    escolhido = (escolhido + 1) % len(PERSONAGENS)
                if evento.key == pygame.K_SPACE:
                    jogo = novo_jogo(PERSONAGENS[escolhido])
                    estado = "jogando"
            elif estado == "cena":
                if evento.key == pygame.K_SPACE and tempo_estado > 60:
                    estado = "vitoria"  # pula a cena (so depois de 1 segundo, para nao pular sem querer)
            elif evento.key == pygame.K_SPACE:
                estado = "selecao"  # do menu, do game over ou da vitoria

    # ---------- atualiza e desenha a tela do estado atual ----------
    if estado == "jogando":
        estado = atualiza(jogo)
        if estado == "vitoria":
            estado = "cena"  # antes da tela de vitoria vem a cena "Eu sou seu pai"
        desenha_jogo(tela, jogo, fonte, fonte_grande)
    else:
        for enfeite in enfeites_menu:
            enfeite.atualiza()
        if estado == "menu":
            tela_menu(tela, tempo, enfeites_menu, nave_menu, fonte, fonte_grande)
        elif estado == "selecao":
            tela_selecao(tela, escolhido, tempo, enfeites_menu, fonte, fonte_pequena, fonte_grande)
        elif estado == "fim":
            tela_fim(tela, jogo, tempo_estado, fonte, fonte_grande)
        elif estado == "cena":
            tela_cena(tela, tempo, tempo_estado, enfeites_menu, fonte, fonte_grande)
            if tempo_estado >= DURACAO_CENA:
                estado = "vitoria"
        else:
            jogo["particulas"] = atualiza_particulas(jogo["particulas"])
            solta_confete(jogo["particulas"])
            tela_vitoria(tela, jogo, tempo, tempo_estado, enfeites_menu, fonte, fonte_grande)

    # ---------- musica de fundo ----------
    if estado == "menu" or estado == "selecao":
        toca_musica("musica_jogo")
    elif estado == "jogando":
        if jogo["fase"] == "chefe":
            toca_musica("musica_chefe")
        else:
            toca_musica("musica_jogo")

    # quando o estado muda, a contagem do estado volta para zero
    if estado != estado_anterior:
        tempo_estado = 0
        if estado == "fim":
            toca_musica("")
            toca("gameover")
        if estado == "cena":
            toca_musica("")  # silencio para a cena
            jogo["particulas"] = []  # apaga o que sobrou das explosoes
        if estado == "vitoria":
            toca("vitoria")
        estado_anterior = estado

    pygame.display.flip()

pygame.quit()
