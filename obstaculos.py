"""Obstaculos: o alvo e o cano (que pode vir trancado por um portao de energia)."""
import random
import pygame
from config import *
from recursos import IMAGENS


# ======================================================================
# CLASSES ALVO E CANO
# ======================================================================
class Alvo:
    """Alvo que fica antes de um cano trancado. Acertar com o laser abre o cano."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - ALVO_TAMANHO // 2, ALVO_TAMANHO, ALVO_TAMANHO)
        self.vivo = True  # False depois de ser acertado (ou nos canos livres)
        self.tempo = 0  # conta quadros (para as animacoes)

    def desenha(self, tela):
        centro = self.rect.center
        raio = ALVO_TAMANHO // 2
        # o alvo "pulsa" e as cores dos aneis se alternam
        pulso = PULSO[(self.tempo // 8) % 4]
        cor_a = LARANJA
        cor_b = VERMELHO
        if (self.tempo // 15) % 2 == 1:
            cor_a = VERMELHO
            cor_b = LARANJA
        if "alvo" in IMAGENS:
            imagem = IMAGENS["alvo"]
            lado = imagem.get_width() + pulso * 2  # a imagem pulsa
            imagem = pygame.transform.scale(imagem, (lado, lado))
            tela.blit(imagem, (centro[0] - lado // 2, centro[1] - lado // 2))
        else:
            pygame.draw.circle(tela, cor_a, centro, raio + pulso)
            pygame.draw.circle(tela, BRANCO, centro, raio * 2 // 3)
            pygame.draw.circle(tela, cor_b, centro, raio // 3)
        # um anel que se abre chamando atencao para o alvo
        anel = raio + (self.tempo % 30) // 3
        pygame.draw.circle(tela, BRANCO, centro, anel, 1)


def monta_cano(nome, altura):
    """Monta a imagem de um cano com a boca virada para cima.

    A boca fica no topo e o corpo se repete para baixo (uma copia sim, outra
    espelhada, para a emenda nao aparecer). Devolve None se nao houver imagem.
    """
    if "cano_boca_" + nome not in IMAGENS:
        return None
    boca = IMAGENS["cano_boca_" + nome]
    corpo = IMAGENS["cano_corpo_" + nome]
    altura = max(altura, boca.get_height())
    imagem = pygame.Surface((boca.get_width(), altura), pygame.SRCALPHA)
    imagem.blit(boca, (0, 0))
    y = boca.get_height()
    espelha = False
    while y < altura:
        pedaco = corpo
        if espelha:
            pedaco = pygame.transform.flip(corpo, False, True)
        imagem.blit(pedaco, (0, y))
        y += corpo.get_height()
        espelha = not espelha
    return imagem


class Cano:
    """Um par de canos (de cima e de baixo) com um buraco no meio.

    Se for trancado, uma tampa fecha o buraco ate o jogador acertar o alvo.
    """

    def __init__(self, x, indice, trancado):
        buraco = BURACO
        if trancado:
            buraco = BURACO_TRANCADO  # nos canos trancados o espaco e maior
        topo = random.randint(100, CHAO - buraco - 100)
        self.indice = indice  # numero do cano (0, 1, 2...), define o cenario
        self.cima = pygame.Rect(x, 0, LARGURA_CANO, topo)
        self.baixo = pygame.Rect(x, topo + buraco, LARGURA_CANO, CHAO - topo - buraco)
        self.trancado = trancado
        # a tampa so tem altura se o cano for trancado
        self.tampa = pygame.Rect(x, topo, LARGURA_CANO, 0)
        self.alvo = Alvo(x - ALVO_DISTANCIA, topo + buraco // 2)
        self.alvo.vivo = trancado
        if trancado:
            self.tampa.height = buraco
        self.abrindo = False  # True depois que o alvo foi acertado
        self.passou = False  # True depois que a nave passou deste cano
        self.tempo = 0  # conta quadros (para as animacoes)
        # imagens do cano (se existirem): a de baixo tem a boca para cima, a de cima e a mesma de cabeca para baixo
        numero = indice // CANOS_POR_CENARIO
        if numero >= len(CENARIOS):
            numero = len(CENARIOS) - 1
        nome = CENARIOS[numero]["arquivo"]
        self.img_baixo = monta_cano(nome, self.baixo.height)
        self.img_cima = None
        if self.img_baixo is not None:
            self.img_cima = pygame.transform.flip(monta_cano(nome, self.cima.height), False, True)

    def atualiza(self, velocidade):
        """Move o cano (e a tampa e o alvo) para a esquerda e anima a abertura."""
        self.tempo += 1
        self.alvo.tempo += 1
        self.cima.x -= velocidade
        self.baixo.x -= velocidade
        self.tampa.x -= velocidade
        self.alvo.rect.x -= velocidade
        if self.abrindo and self.tampa.height > 0:
            self.tampa.height -= 6  # a tampa vai encolhendo para cima
            if self.tampa.height < 0:
                self.tampa.height = 0

    def acerta_alvo(self, rect_laser):
        """True (e abre o cano) se o laser acertou o alvo."""
        if self.alvo.vivo and rect_laser.colliderect(self.alvo.rect):
            self.alvo.vivo = False
            self.abrindo = True
            return True
        return False

    def bloqueia(self, rect_laser):
        """True se o laser bateu em alguma parte solida do cano."""
        if rect_laser.colliderect(self.cima) or rect_laser.colliderect(self.baixo):
            return True
        return self.tampa.height > 0 and rect_laser.colliderect(self.tampa)

    def bate(self, rect_nave):
        """True se a nave bateu em alguma parte solida do cano."""
        return self.bloqueia(rect_nave)

    def desenha_portao(self, tela):
        """Portao de energia: o corpo se repete e as pontas de metal ficam em cima e embaixo."""
        corpo = IMAGENS["portao_corpo_1"]
        if (self.tempo // 6) % 2 == 1:
            corpo = IMAGENS["portao_corpo_2"]  # as faixas de energia mudam de lugar
        topo = IMAGENS["portao_topo"]
        base = IMAGENS["portao_base"]
        x = self.tampa.centerx - corpo.get_width() // 2
        tela.set_clip(self.tampa)  # o corpo nao pode passar da altura do portao
        y = self.tampa.top
        while y < self.tampa.bottom:
            tela.blit(corpo, (x, y))
            y += corpo.get_height()
        tela.set_clip(None)
        tela.blit(topo, (x, self.tampa.top))
        tela.blit(base, (x, self.tampa.bottom - base.get_height()))

    def desenha(self, tela, cor, cor_borda):
        if self.img_baixo is not None:
            sobra = (self.img_baixo.get_width() - LARGURA_CANO) // 2  # a boca e mais larga que o cano
            tela.blit(self.img_baixo, (self.baixo.x - sobra, self.baixo.top))
            tela.blit(self.img_cima, (self.cima.x - sobra, self.cima.bottom - self.img_cima.get_height()))
        else:
            for parte in (self.cima, self.baixo):
                pygame.draw.rect(tela, cor, parte)
            # "labios" nas pontas dos canos, so para dar acabamento
            pygame.draw.rect(tela, cor_borda, (self.cima.x - 4, self.cima.bottom - 18, LARGURA_CANO + 8, 18))
            pygame.draw.rect(tela, cor_borda, (self.baixo.x - 4, self.baixo.top, LARGURA_CANO + 8, 18))
        if self.tampa.height > 0 and "portao_topo" in IMAGENS:
            self.desenha_portao(tela)
        elif self.tampa.height > 0:
            pygame.draw.rect(tela, (140, 20, 20), self.tampa)
            # faixas de energia subindo pelo portao
            y = self.tampa.bottom - 3 - (self.tempo * 2) % 14
            while y > self.tampa.top:
                pygame.draw.rect(tela, (255, 90, 90), (self.tampa.x, y, LARGURA_CANO, 3))
                y -= 14
            borda = BRANCO
            if (self.tempo // 6) % 2 == 0:
                borda = (255, 170, 170)  # a borda do portao pisca
            pygame.draw.rect(tela, borda, self.tampa, 3)
        if self.alvo.vivo:
            self.alvo.desenha(tela)
