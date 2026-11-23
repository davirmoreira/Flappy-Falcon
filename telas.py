"""Telas do jogo: tudo o que e desenhado (cenario, jogo, menu, selecao, fim, cena e vitoria)."""
import random
import pygame
from config import *
from recursos import IMAGENS
from efeitos import *
from nave import *
from obstaculos import *
from chefe import *
from logica import cenario_atual


# ======================================================================
# TELAS (tudo que e desenhado)
# ======================================================================
def escreve(tela, texto, fonte, cor, y, alfa=255):
    """Escreve um texto centralizado na horizontal (alfa < 255 deixa transparente)."""
    imagem = fonte.render(texto, True, cor)
    imagem.set_alpha(alfa)
    contorno = fonte.render(texto, True, PRETO)  # sombra, para ler bem em qualquer fundo
    contorno.set_alpha(alfa)
    x = LARGURA // 2 - imagem.get_width() // 2
    tela.blit(contorno, (x + 2, y + 2))
    tela.blit(imagem, (x, y))


def desenha_coracao(tela, x, y, cor):
    if "coracao_cheio" in IMAGENS:
        imagem = IMAGENS["coracao_cheio"]
        if cor == CINZA:
            imagem = IMAGENS["coracao_vazio"]
        elif cor == BRANCO:
            imagem = IMAGENS["coracao_branco"]
        tela.blit(imagem, (x, y))
        return
    pygame.draw.circle(tela, cor, (x + 8, y + 8), 8)
    pygame.draw.circle(tela, cor, (x + 22, y + 8), 8)
    pygame.draw.polygon(tela, cor, [(x, y + 11), (x + 30, y + 11), (x + 15, y + 28)])


def desenha_enfeites(tela, enfeites, tempo):
    for enfeite in enfeites:
        enfeite.desenha(tela, tempo)


def desenha_cenario(tela, cenario, tempo, chao_x):
    """Fundo do cenario: ceu, astro pulsando, coluna de luzes (Estrela da Morte) e chao andando."""
    fundo = IMAGENS.get("fundo_" + cenario["arquivo"])
    if fundo is not None:
        # fundo desenhado: so as listras do chao andam por cima da faixa escura de baixo
        tela.blit(fundo, (0, 0))
        c = fundo.get_at((400, ALTURA - 6))
        cor_listra = (min(c[0] + 25, 255), min(c[1] + 25, 255), min(c[2] + 25, 255))
        deslocamento = chao_x % 40
        for i in range(LARGURA // 40 + 2):
            x = i * 40 - deslocamento
            pygame.draw.rect(tela, cor_listra, (x, CHAO + 14, 22, 3))
            pygame.draw.rect(tela, cor_listra, (x + 20, CHAO + 30, 22, 3))
        return
    tela.fill(cenario["fundo"])
    if cenario["nome"] == "ESTRELA DA MORTE":
        for i in range(6):  # colunas de metal no fundo
            x = 60 + i * 130
            pygame.draw.rect(tela, (55, 60, 75), (x, 0, 30, CHAO))
            y = (tempo * 2 + i * 70) % CHAO  # uma luz desce por cada coluna
            pygame.draw.rect(tela, (255, 80, 80), (x + 10, y, 10, 20))
    raio = 50 + PULSO[(tempo // 20) % 4]
    pygame.draw.circle(tela, cenario["astro"], (640, 110), raio)
    pygame.draw.circle(tela, cenario["astro"], (640, 110), raio + 10, 2)
    # chao com listras que passam para a esquerda (da sensacao de velocidade)
    pygame.draw.rect(tela, cenario["chao"], (0, CHAO, LARGURA, ALTURA - CHAO))
    c = cenario["chao"]
    cor_listra = (c[0] * 3 // 4, c[1] * 3 // 4, c[2] * 3 // 4)
    pygame.draw.rect(tela, cor_listra, (0, CHAO, LARGURA, 4))
    deslocamento = chao_x % 40
    for i in range(LARGURA // 40 + 2):
        x = i * 40 - deslocamento
        pygame.draw.rect(tela, cor_listra, (x, CHAO + 14, 22, 4))
        pygame.draw.rect(tela, cor_listra, (x + 20, CHAO + 30, 22, 4))


def desenha_jogo(tela, jogo, fonte, fonte_grande):
    nave = jogo["nave"]
    chefe = jogo["chefe"]
    cenario = cenario_atual(jogo)
    desenha_cenario(tela, cenario, jogo["tempo"], jogo["chao_x"])
    desenha_enfeites(tela, jogo["enfeites"], jogo["tempo"])

    for cano in jogo["canos"]:
        # a cor do cano depende do cenario a que ele pertence
        indice = cano.indice // CANOS_POR_CENARIO
        if indice >= len(CENARIOS):
            indice = len(CENARIOS) - 1
        dados = CENARIOS[indice]
        cano.desenha(tela, dados["cano"], dados["borda"])
    if jogo["fase"] == "chefe":
        chefe.desenha(tela)
    for laser in jogo["lasers"]:
        laser.desenha(tela)
    for laser in jogo["lasers_inimigos"]:
        laser.desenha(tela)
    if jogo["resultado"] != "fim":
        nave.desenha(tela)
    for particula in jogo["particulas"]:
        particula.desenha(tela)

    # ---------- painel: vidas, pontos e progresso ----------
    painel = pygame.Surface((nave.vidas_max * 38 + 20, 100), pygame.SRCALPHA)
    painel.fill((0, 0, 0, 110))  # fundo escuro transparente, para o texto aparecer nos fundos claros
    tela.blit(painel, (4, 4))
    for i in range(nave.vidas_max):
        x = 12 + i * 38
        y = 10
        cor = VERMELHO
        if i >= nave.vidas:
            cor = CINZA
            if i == nave.vidas and nave.tempo_dano > 0:
                # o coracao que acabou de ser perdido treme e pisca
                x += random.randint(-3, 3)
                if (nave.tempo_dano // 4) % 2 == 0:
                    cor = BRANCO
        elif nave.vidas == 1 and (jogo["tempo"] // 15) % 2 == 0:
            cor = (255, 120, 120)  # ultima vida: o coracao pulsa
            y = 8
        desenha_coracao(tela, x, y, cor)
    tela.blit(fonte.render(f"Pontos: {jogo['pontos']}", True, BRANCO), (12, 50))
    if jogo["fase"] == "chefe":
        escreve(tela, "RESINA VADER", fonte, BRANCO, 10)
        pygame.draw.rect(tela, CINZA, (250, 38, 300, 16))
        vida = chefe.vida
        if vida < 0:
            vida = 0
        largura_vida = 300 * vida // VIDA_CHEFE
        pygame.draw.rect(tela, VERMELHO, (250, 38, largura_vida, 16))
        pygame.draw.rect(tela, BRANCO, (250, 38, 300, 16), 2)
    else:
        texto_canos = f"Canos: {jogo['canos_passados']}/{TOTAL_CANOS}"
        tela.blit(fonte.render(texto_canos, True, BRANCO), (12, 76))
    if jogo["banner"] > 0:
        alfa = jogo["banner"] * 6  # o nome do cenario some devagar
        if alfa > 255:
            alfa = 255
        escreve(tela, cenario["nome"], fonte_grande, BRANCO, 150, alfa)
        if jogo["fase"] == "chefe":
            escreve(tela, "Derrote o Resina Vader!", fonte, AMARELO, 215, alfa)

    # tremida da tela: desloca a imagem toda um pouquinho
    if jogo["tremor"] > 0:
        forca = jogo["tremor"] // 3
        copia = tela.copy()
        tela.fill(PRETO)
        tela.blit(copia, (random.randint(-forca, forca), random.randint(-forca, forca)))


def desenha_piloto(tela, personagem, x, y, tempo, animado):
    """Desenha o piloto (area de 160x150, a imagem pode passar um pouco para cima).

    Se animado, ele respira (sobe e desce devagar). Sem imagens, usa um retrato de formas.
    """
    if personagem["arquivo"] in IMAGENS:
        imagem = IMAGENS[personagem["arquivo"]]
        balanco = 0
        if animado:
            balanco = BALANCO[(tempo // 8) % 6] // 3
        chao_y = y + 165  # onde ficam os pes
        pygame.draw.ellipse(tela, (20, 22, 50), (x + 35, chao_y - 8, 90, 16))  # sombra
        tela.blit(imagem, (x + 80 - imagem.get_width() // 2, chao_y - imagem.get_height() + balanco))
        return
    estilo = personagem["estilo"]
    cx = x + 80
    balanco = 0
    pisca = False
    if animado:
        balanco = BALANCO[(tempo // 8) % 6] // 3  # a cabeca sobe e desce devagar
        pisca = tempo % 150 < 6  # de vez em quando ele pisca
    cabeca_y = y + 64 + balanco
    corpo_y = y + 102 + balanco
    pygame.draw.rect(tela, (40, 45, 85), (x, y, 160, 150))
    # corpo e roupa de cada piloto
    pygame.draw.rect(tela, personagem["cor"], (cx - 40, corpo_y, 80, 150 - (corpo_y - y)))
    if estilo == "contrabandista":
        pygame.draw.rect(tela, PRETO, (cx - 40, corpo_y, 24, 48))  # colete
        pygame.draw.rect(tela, PRETO, (cx + 16, corpo_y, 24, 48))
        pygame.draw.rect(tela, CINZA, (cx + 30, y + 118, 30, 10))  # blaster
        pygame.draw.rect(tela, CINZA, (cx + 34, y + 126, 8, 14))
    if estilo == "wookiee":
        pygame.draw.line(tela, (60, 35, 15), (cx - 40, corpo_y + 2), (cx + 40, y + 148), 8)  # bandoleira
        pygame.draw.circle(tela, personagem["cabelo"], (cx, cabeca_y), 42)  # pelo em volta do rosto
    if estilo == "jedi":
        if animado and (tempo // 4) % 2 == 0:
            pygame.draw.rect(tela, (40, 100, 170), (cx + 43, y + 28, 16, 88))  # brilho do sabre
        pygame.draw.rect(tela, AZUL_CLARO, (cx + 47, y + 34, 8, 80))
        pygame.draw.rect(tela, BRANCO, (cx + 50, y + 34, 2, 80))
        pygame.draw.rect(tela, CINZA, (cx + 46, y + 114, 10, 16))
    # cabeca, cabelo, olhos e sorriso
    pygame.draw.circle(tela, personagem["pele"], (cx, cabeca_y), 30)
    if estilo != "wookiee":
        pygame.draw.ellipse(tela, personagem["cabelo"], (cx - 30, cabeca_y - 34, 60, 24))
    for lado in (-1, 1):
        ex = cx + lado * 11
        if pisca:
            pygame.draw.line(tela, PRETO, (ex - 5, cabeca_y - 4), (ex + 5, cabeca_y - 4), 2)
        else:
            pygame.draw.circle(tela, BRANCO, (ex, cabeca_y - 4), 5)
            pygame.draw.circle(tela, PRETO, (ex, cabeca_y - 4), 2)
    pygame.draw.arc(tela, PRETO, (cx - 10, cabeca_y + 6, 20, 12), 3.3, 6.1, 2)


def tela_menu(tela, tempo, enfeites, nave_menu, fonte, fonte_grande):
    tela.fill((10, 10, 30))
    desenha_enfeites(tela, enfeites, tempo)
    # o titulo balanca devagar
    if "logo" in IMAGENS:
        logo = IMAGENS["logo"]
        tela.blit(logo, (LARGURA // 2 - logo.get_width() // 2, 60 + BALANCO[(tempo // 8) % 6]))
    else:
        escreve(tela, "FLAPPY FALCON", fonte_grande, AMARELO, 140 + BALANCO[(tempo // 8) % 6])
    escreve(tela, "uma aventura em uma galáxia muito, muito distante", fonte, BRANCO, 215)
    escreve(tela, "ESPAÇO: pular        R: atirar", fonte, BRANCO, 300)
    escreve(tela, "Alguns canos vêm trancados: acerte o alvo para abri-los", fonte, BRANCO, 340)
    escreve(tela, "No fim, derrote o Resina Vader na Estrela da Morte", fonte, BRANCO, 380)
    if (tempo // 30) % 2 == 0:  # o texto pisca
        escreve(tela, "Pressione ESPAÇO para escolher seu piloto", fonte, AMARELO, 470)
    # a Millennium Falcon cruza a tela de um lado ao outro
    x = (tempo * 4) % (LARGURA + 300) - 150
    nave_menu.desenha_modelo(tela, (x, 540 + BALANCO[(tempo // 8) % 6]), 0, 1 + (tempo // 3) % 4)


def tela_selecao(tela, escolhido, tempo, enfeites, fonte, fonte_pequena, fonte_grande):
    tela.fill((10, 10, 30))
    desenha_enfeites(tela, enfeites, tempo)
    escreve(tela, "ESCOLHA SEU PILOTO", fonte_grande, AMARELO, 50)
    for i in range(len(PERSONAGENS)):
        personagem = PERSONAGENS[i]
        x = 60 + i * 250
        y = 140
        pygame.draw.rect(tela, (30, 30, 60), (x, y, 220, 320))
        if i == escolhido:
            cor_borda = AMARELO
            if (tempo // 15) % 2 == 1:
                cor_borda = LARANJA  # a borda do escolhido pisca
            pygame.draw.rect(tela, cor_borda, (x, y, 220, 320), 5)
        else:
            pygame.draw.rect(tela, CINZA, (x, y, 220, 320), 2)
        # so o piloto escolhido se mexe
        desenha_piloto(tela, personagem, x + 30, y + 20, tempo, i == escolhido)
        nome = fonte_pequena.render(personagem["nome"], True, BRANCO)
        tela.blit(nome, (x + 110 - nome.get_width() // 2, y + 190))
        poder = fonte_pequena.render(personagem["poder"], True, AMARELO)
        tela.blit(poder, (x + 110 - poder.get_width() // 2, y + 230))
        vidas = fonte_pequena.render(f"Vidas: {personagem['vidas']}", True, BRANCO)
        tela.blit(vidas, (x + 110 - vidas.get_width() // 2, y + 265))
    escreve(tela, "R: trocar de piloto        ESPAÇO: confirmar", fonte, BRANCO, 510)


def tela_fim(tela, jogo, tempo_estado, fonte, fonte_grande):
    tela.fill((40, 0, 0))
    # o GAME OVER cai do alto da tela
    y = -60 + tempo_estado * 8
    if y > 190:
        y = 190
    escreve(tela, "GAME OVER", fonte_grande, VERMELHO, y)
    escreve(tela, f"Pontos: {jogo['pontos']}", fonte, BRANCO, 280)
    if jogo["fase"] == "chefe":
        vida = jogo["chefe"].vida
        escreve(tela, f"Vida do Resina Vader: {vida}/{VIDA_CHEFE}", fonte, BRANCO, 320)
    else:
        escreve(tela, f"Canos passados: {jogo['canos_passados']}/{TOTAL_CANOS}", fonte, BRANCO, 320)
    if (tempo_estado // 30) % 2 == 0:
        escreve(tela, "Pressione ESPAÇO para tentar de novo", fonte, AMARELO, 420)


def tela_cena(tela, tempo, tempo_estado, enfeites, fonte, fonte_grande):
    """Cena depois de derrotar o chefao: o Resina Vader ajoelhado diz "Eu sou seu pai..."."""
    desenha_cenario(tela, CENARIO_CHEFE, tempo, 0)
    desenha_enfeites(tela, enfeites, tempo)
    sombra = IMAGENS["sombra"]
    sombra.set_alpha(170)
    tela.blit(sombra, (0, 0))  # escurece o fundo para destacar a cena
    if "pai" in IMAGENS:
        # a cada TEMPO_POR_FALA quadros aparece mais um pedaco da frase (4 imagens)
        etapa = tempo_estado // TEMPO_POR_FALA
        if etapa > 3:
            etapa = 3
        imagem = IMAGENS["pai"][etapa]
        alfa = tempo_estado * 8  # a cena aparece aos poucos
        if alfa > 255:
            alfa = 255
        imagem.set_alpha(alfa)
        tela.blit(imagem, (0, 0))
    else:
        # sem imagens: a frase vai sendo "digitada" letra por letra
        frase = "Eu sou seu pai..."
        letras = tempo_estado // 6
        escreve(tela, "RESINA VADER", fonte, AMARELO, 230)
        escreve(tela, frase[:letras], fonte_grande, BRANCO, 280)
    if tempo_estado > 60 and (tempo_estado // 30) % 2 == 0:
        escreve(tela, "Pressione ESPAÇO para continuar", fonte, AMARELO, 560)


def tela_vitoria(tela, jogo, tempo, tempo_estado, enfeites, fonte, fonte_grande):
    tela.fill((10, 10, 30))
    desenha_enfeites(tela, enfeites, tempo)
    y = -60 + tempo_estado * 8  # o titulo cai do alto da tela
    if y > 90:
        y = 90
    escreve(tela, "VOCÊ VENCEU!", fonte_grande, AMARELO, y)
    escreve(tela, "O Resina Vader foi derrotado", fonte, BRANCO, 160)
    escreve(tela, f"{jogo['personagem']['nome']} salvou a galáxia!", fonte, BRANCO, 195)
    escreve(tela, f"Pontos: {jogo['pontos']}", fonte, BRANCO, 235)
    # o piloto comemora dando pulinhos
    salto = SALTOS[(tempo // 6) % 6]
    desenha_piloto(tela, jogo["personagem"], LARGURA // 2 - 80, 300 + salto, tempo, True)
    for particula in jogo["particulas"]:
        particula.desenha(tela)  # confete
    if (tempo_estado // 30) % 2 == 0:
        escreve(tela, "Pressione ESPAÇO para jogar de novo", fonte, AMARELO, 530)
