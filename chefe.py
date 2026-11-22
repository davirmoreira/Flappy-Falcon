"""O chefao Resina Vader: sobe e desce na plataforma atirando de volta."""
import random
import pygame
from config import *
from recursos import IMAGENS, toca
from nave import Laser


# ======================================================================
# CLASSE CHEFE (Resina Vader)
# ======================================================================
class Chefe:
    """O chefao: sobe e desce na plataforma atirando de volta. Tem VIDA_CHEFE de vida."""

    def __init__(self):
        self.rect = pygame.Rect(LARGURA + 50, 250, 90, 120)
        self.vida = VIDA_CHEFE
        self.direcao = 1  # 1 = descendo, -1 = subindo
        self.entrando = True  # True enquanto ele entra deslizando na tela
        self.tempo_tiro = 60  # quadros ate o proximo tiro
        self.tempo_dano = 0  # quadros tremendo e branco depois de levar um tiro
        self.tempo = 0  # conta quadros (para as animacoes)
        self.sumiu = False  # True no fim da explosao final

    def recebe_dano(self):
        self.vida -= 1
        self.tempo_dano = 8
        toca("chefe_dano")  # grunhido de dor dentro da mascara

    def atualiza(self, lasers_inimigos):
        self.tempo += 1
        if self.tempo_dano > 0:
            self.tempo_dano -= 1
        if self.vida <= 0:
            return  # derrotado: fica parado, so explodindo
        if self.entrando:
            self.rect.x -= 4
            if self.rect.x <= 620:
                self.entrando = False
            return
        # na segunda metade da vida ele fica mais rapido e atira mais
        velocidade = 2
        intervalo = 100
        if self.vida <= VIDA_CHEFE // 2:
            velocidade = 3
            intervalo = 70
        self.rect.y += self.direcao * velocidade
        if self.rect.top < 90:
            self.rect.top = 90
            self.direcao = 1
        if self.rect.top > 420:
            self.rect.top = 420
            self.direcao = -1
        self.tempo_tiro -= 1
        if self.tempo_tiro <= 0:
            laser = Laser(self.rect.left - 30, self.rect.centery, -VELOCIDADE_LASER_CHEFE, VERMELHO, 30)
            lasers_inimigos.append(laser)
            self.tempo_tiro = intervalo
            toca("chefe_tiro")

    def desenha(self, tela):
        r = self.rect
        if self.sumiu:
            return
        if self.vida <= 0 and (self.tempo // 4) % 2 == 0:
            return  # pisca enquanto explode
        # ao levar um tiro ele treme para os lados e fica branco
        dx = 0
        cor = (30, 30, 40)
        if self.tempo_dano > 0:
            dx = random.randint(-3, 3)
            cor = (235, 235, 235)
        x = r.x + dx
        cx = r.centerx + dx
        balanco = BALANCO[(self.tempo // 8) % 6]  # a capa balanca

        if "plataforma" in IMAGENS:
            plataforma = IMAGENS["plataforma"]  # (os propulsores ja fazem parte da imagem)
            tela.blit(plataforma, (cx - plataforma.get_width() // 2, r.bottom - 2))
        else:
            # propulsores embaixo da plataforma (a chama alterna de tamanho)
            altura = 8 + (self.tempo // 3) % 2 * 6
            for px in (x - 5, x + r.width - 19):
                pygame.draw.polygon(tela, LARANJA, [(px, r.bottom + 18), (px + 14, r.bottom + 18),
                                                    (px + 7, r.bottom + 18 + altura)])
                pygame.draw.polygon(tela, AMARELO, [(px + 3, r.bottom + 18), (px + 11, r.bottom + 18),
                                                    (px + 7, r.bottom + 18 + altura // 2)])
            # plataforma com luzes piscando
            pygame.draw.rect(tela, CINZA_CLARO, (x - 25, r.bottom, r.width + 50, 18))
            pygame.draw.rect(tela, CINZA, (x - 25, r.bottom, r.width + 50, 18), 2)
            for i in range(4):
                cor_luz = (255, 60, 60)
                if (self.tempo // 15 + i) % 2 == 0:
                    cor_luz = (90, 20, 20)
                pygame.draw.circle(tela, cor_luz, (x - 10 + i * 36, r.bottom + 9), 3)


        carregando = (not self.entrando) and self.vida > 0 and self.tempo_tiro < 20
        if "vader" in IMAGENS:
            # imagem do chefao (clarinha quando leva tiro), "respirando" sobre a plataforma
            imagem = IMAGENS["vader"]
            if self.tempo_dano > 0:
                imagem = IMAGENS["vader_branco"]
            respira = BALANCO[(self.tempo // 8) % 6] // 3
            tela.blit(imagem, (cx - imagem.get_width() // 2, r.bottom - imagem.get_height() + respira))
        else:
            # sem imagens: capa (a barra de baixo balanca), capacete, olhos, peito e sabre
            pygame.draw.polygon(tela, cor, [(x, r.y + 40), (x + r.width, r.y + 40),
                                            (x + r.width + 10 + balanco, r.bottom),
                                            (x - 10 + balanco, r.bottom)])
            pygame.draw.circle(tela, cor, (cx, r.y + 28), 28)
            cor_olho = VERMELHO
            if carregando:
                cor_olho = (255, 170, 170)
            pygame.draw.rect(tela, cor_olho, (cx - 14, r.y + 22, 10, 6))
            pygame.draw.rect(tela, cor_olho, (cx + 4, r.y + 22, 10, 6))
            cor_painel = VERMELHO
            if (self.tempo // 20) % 2 == 1:
                cor_painel = (120, 30, 30)
            pygame.draw.rect(tela, cor_painel, (cx - 10, r.y + 66, 20, 10))
            if self.tempo % 6 < 3:
                pygame.draw.rect(tela, (140, 30, 30), (x - 26, r.y + 46, 16, 68))
            pygame.draw.rect(tela, VERMELHO, (x - 22, r.y + 50, 8, 60))
            pygame.draw.rect(tela, BRANCO, (x - 19, r.y + 52, 2, 56))
        if carregando:
            # quando esta quase atirando, uma bola de energia cresce na frente dele
            tamanho = (20 - self.tempo_tiro) // 2 + 2
            pygame.draw.circle(tela, VERMELHO, (x - 30, r.centery), tamanho)
            pygame.draw.circle(tela, BRANCO, (x - 30, r.centery), tamanho // 2)
