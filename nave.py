"""A nave (Millennium Falcon com o piloto escolhido) e os lasers."""
import random
import pygame
from config import *
from recursos import IMAGENS, toca
from efeitos import *


# ======================================================================
# CLASSE LASER (serve para os tiros da nave e para os do chefao)
# ======================================================================
class Laser:
    """Um tiro: anda na horizontal com a velocidade dada (negativa = para a esquerda)."""

    def __init__(self, x, y, velocidade, cor, largura):
        self.rect = pygame.Rect(x, y - 4, largura, 8)
        self.velocidade = velocidade
        self.cor = cor

    def atualiza(self):
        self.rect.x += self.velocidade

    def desenha(self, tela):
        chave = "laser_azul"
        if self.velocidade < 0:
            chave = "laser_vermelho"  # o tiro do chefao anda para a esquerda
        if chave in IMAGENS:
            imagem = IMAGENS[chave]
            tela.blit(imagem, (self.rect.centerx - imagem.get_width() // 2,
                               self.rect.centery - imagem.get_height() // 2))
            return
        # brilho (elipse maior), e o miolo branco por cima
        pygame.draw.ellipse(tela, self.cor, self.rect.inflate(8, 8))
        pygame.draw.ellipse(tela, BRANCO, self.rect.inflate(-4, -3))


# ======================================================================
# CLASSE NAVE
# ======================================================================
class Nave:
    """A Millennium Falcon: so pula (como no Flappy Bird), atira e tem vidas."""

    def __init__(self, personagem):
        self.rect = pygame.Rect(150, 280, 64, 30)
        self.vel = 0  # velocidade vertical (negativa = subindo)
        self.gravidade = personagem["gravidade"]  # cada personagem cai de um jeito
        self.vidas_max = personagem["vidas"]
        self.vidas = personagem["vidas"]
        self.espera_max = personagem["espera_tiro"]
        self.tempo_fogo = 0  # quadros restantes do fogo na traseira
        self.tempo_invulneravel = 0  # quadros restantes sem levar dano
        self.espera_tiro = 0  # quadros ate poder atirar de novo
        self.tempo = 0  # conta quadros (para as animacoes)
        self.angulo = 0  # inclinacao da nave (graus): bico para cima ao subir
        self.tempo_dano = 0  # quadros em que o coracao perdido fica tremendo
        self.chave_cabeca = "cabeca_" + personagem["arquivo"]  # imagem da cabeca do piloto
        self.imagem = self.cria_imagem()

    def cria_imagem(self):
        """Monta a nave em uma superficie transparente (com espaco para o fogo atras)."""
        if "falcon" in IMAGENS:
            imagem = pygame.Surface((176, 60), pygame.SRCALPHA)
            imagem.blit(IMAGENS["falcon"], (40, 17))  # o Falcon fica no centro da superficie
            self.fogo_x = 48  # onde o fogo encosta no motor
            self.fogo_y = 34
            return imagem
        # sem imagens: desenha a nave com formas
        self.fogo_x = 22
        self.fogo_y = 25
        imagem = pygame.Surface((104, 50), pygame.SRCALPHA)
        corpo = pygame.Rect(20, 10, 64, 30)
        pygame.draw.polygon(imagem, CINZA, [(70, 14), (92, 18), (92, 22), (70, 25)])  # garra de cima
        pygame.draw.polygon(imagem, CINZA, [(70, 36), (92, 32), (92, 28), (70, 25)])  # garra de baixo
        pygame.draw.ellipse(imagem, CINZA_CLARO, corpo)
        pygame.draw.ellipse(imagem, CINZA, corpo, 2)
        pygame.draw.line(imagem, CINZA, (36, 25), (66, 25), 1)  # detalhe do casco
        pygame.draw.circle(imagem, CINZA, (46, 15), 4)  # antena radar
        pygame.draw.circle(imagem, AZUL, (70, 19), 5)  # cabine
        return imagem

    def desenha_modelo(self, tela, centro, angulo, chama):
        """Desenha a nave com o centro no ponto dado.

        chama: 0 = sem fogo; 1, 2, 3 ou 4 = quadro da animacao do fogo.
        """
        if self.chave_cabeca in IMAGENS and "falcon" in IMAGENS:
            # o piloto com a cabeca para fora: desenhada ANTES da nave, para o casco cobrir o pescoco
            quadro = pygame.Surface(self.imagem.get_size(), pygame.SRCALPHA)
            cabeca = IMAGENS[self.chave_cabeca]
            x_cabeca = 111 - cabeca.get_width() // 2
            if chama > 0:
                x_cabeca -= 2  # com o motor ligado, o vento empurra a cabeca para tras
            y_cabeca = 35 - cabeca.get_height() + BALANCO[(self.tempo // 8) % 6] // 3
            quadro.blit(cabeca, (x_cabeca, y_cabeca))
            quadro.blit(self.imagem, (0, 0))
        else:
            quadro = self.imagem.copy()
        fx = self.fogo_x
        fy = self.fogo_y
        if "fogo" in IMAGENS:
            if chama > 0:
                fogo = IMAGENS["fogo"][chama - 1]
                quadro.blit(fogo, (fx - fogo.get_width(), fy - fogo.get_height() // 2))
        elif chama == 0:
            pygame.draw.circle(quadro, AZUL_CLARO, (fx - 1, fy), 3)
        else:
            comprimento = 20
            if chama % 2 == 0:
                comprimento = 13
            pygame.draw.polygon(quadro, LARANJA, [(fx, fy - 7), (fx, fy + 7), (fx - comprimento, fy)])
            pygame.draw.polygon(quadro, AMARELO, [(fx, fy - 4), (fx, fy + 4), (fx - comprimento * 2 // 3, fy)])
        girada = pygame.transform.rotate(quadro, angulo)
        tela.blit(girada, girada.get_rect(center=centro))

    def pula(self, particulas):
        """ESPACO: sobe de uma vez e solta fogo e faiscas pela traseira."""
        self.vel = FORCA_PULO
        self.tempo_fogo = 8
        toca("pulo")
        for i in range(4):
            y = self.rect.centery + random.randint(-4, 4)
            particulas.append(Particula(self.rect.left, y, random.randint(-4, -1),
                                        random.randint(-1, 2), sorteia(CORES_FOGO), 18, 5, 0.05))

    def atira(self, lasers):
        """R: coloca um laser novo na lista, se a espera do tiro ja acabou."""
        if self.espera_tiro == 0:
            lasers.append(Laser(self.rect.centerx + 40, self.rect.centery, VELOCIDADE_LASER, AZUL_CLARO, 32))
            self.espera_tiro = self.espera_max
            toca("tiro")

    def atualiza(self):
        """Roda uma vez por quadro: gravidade, inclinacao, fogo, tiro e invulnerabilidade."""
        self.tempo += 1
        self.vel += self.gravidade
        self.rect.y += int(self.vel)
        # inclinacao: sobe com o bico para cima, cai com o bico para baixo
        alvo = -self.vel * 4
        if alvo > 28:
            alvo = 28
        if alvo < -35:
            alvo = -35
        self.angulo += (alvo - self.angulo) * 0.25
        if self.tempo_fogo > 0:
            self.tempo_fogo -= 1
        if self.tempo_dano > 0:
            self.tempo_dano -= 1
        if self.espera_tiro > 0:
            self.espera_tiro -= 1
        if self.tempo_invulneravel > 0:
            self.tempo_invulneravel -= 1
            # enquanto esta invulneravel, nao deixa sair da tela
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel = 0
            if self.rect.bottom > CHAO:
                self.rect.bottom = CHAO
                self.vel = 0

    def toca_limite(self):
        """True se tocou no teto ou no chao."""
        return self.rect.top < 0 or self.rect.bottom > CHAO

    def perde_vida(self):
        """Perde um coracao, volta para o meio da tela e fica invulneravel um tempo."""
        self.vidas -= 1
        self.tempo_invulneravel = TEMPO_INVULNERAVEL
        self.tempo_dano = 40
        self.rect.y = 280
        self.vel = 0
        self.angulo = 0

    def desenha(self, tela):
        # piscando enquanto esta invulneravel (some em quadros alternados)
        if self.tempo_invulneravel > 0 and (self.tempo_invulneravel // 6) % 2 == 0:
            return
        chama = 0
        if self.tempo_fogo > 0:
            chama = 1 + (self.tempo // 3) % 4  # passa pelos 4 quadros da chama
        self.desenha_modelo(tela, self.rect.center, self.angulo, chama)
