"""Efeitos visuais: particulas, explosoes (Boom) e enfeites do cenario (poeira, nuvem, chuva...)."""
import random
import pygame
from config import *
from recursos import IMAGENS


# ======================================================================
# FUNCOES AUXILIARES DAS ANIMACOES
# ======================================================================
def sorteia(lista):
    """Devolve um item qualquer da lista."""
    return lista[random.randint(0, len(lista) - 1)]


# ======================================================================
# CLASSE PARTICULA (bolinha que anda, encolhe e some: fogo, explosao, confete)
# ======================================================================
class Particula:
    """Uma bolinha com velocidade, gravidade e tempo de vida."""

    def __init__(self, x, y, vx, vy, cor, vida, raio, gravidade):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.cor = cor
        self.vida = vida  # quadros que ainda faltam para sumir
        self.vida_max = vida
        self.raio = raio
        self.gravidade = gravidade

    def atualiza(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravidade
        self.vida -= 1

    def desenha(self, tela):
        # a bolinha vai encolhendo ate sumir
        raio = self.raio * self.vida // self.vida_max
        if raio < 1:
            raio = 1
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), raio)


class Boom:
    """Explosao desenhada: passa por 5 imagens (faisca, bola de fogo, fumaca...)."""

    def __init__(self, x, y, tamanho):
        self.x = x
        self.y = y
        self.vida = 20  # quadros que ainda faltam para sumir
        self.vida_max = 20
        self.quadros = []
        for imagem in IMAGENS["explosao"]:
            self.quadros.append(pygame.transform.scale(imagem, (tamanho, tamanho)))

    def atualiza(self):
        self.vida -= 1

    def desenha(self, tela):
        indice = (self.vida_max - self.vida) // 4  # troca de imagem a cada 4 quadros
        if indice > 4:
            indice = 4
        quadro = self.quadros[indice]
        tela.blit(quadro, (int(self.x) - quadro.get_width() // 2, int(self.y) - quadro.get_height() // 2))


def explosao(particulas, x, y, quantidade, cores, forca):
    """Joga varias particulas para todos os lados a partir do ponto (x, y)."""
    if quantidade >= 14 and "explosao" in IMAGENS:
        tamanho = 40 + quantidade * 2  # quanto mais particulas, maior a explosao
        if tamanho > 200:
            tamanho = 200
        particulas.append(Boom(x, y, tamanho))
    for i in range(quantidade):
        vx = random.randint(-forca, forca)
        vy = random.randint(-forca, forca)
        raio = random.randint(4, 9)
        particulas.append(Particula(x, y, vx, vy, sorteia(cores), random.randint(20, 40), raio, 0.1))


def atualiza_particulas(particulas):
    """Move todas as particulas e devolve so as que ainda estao vivas."""
    restantes = []
    for particula in particulas:
        particula.atualiza()
        if particula.vida > 0:
            restantes.append(particula)
    return restantes


def solta_confete(particulas):
    """Cria confetes caindo do alto da tela (tela de vitoria)."""
    for i in range(2):
        x = random.randint(0, LARGURA)
        vx = random.randint(-1, 1)
        vy = random.randint(2, 4)
        particulas.append(Particula(x, -10, vx, vy, sorteia(CORES_CONFETE), 200, 5, 0.02))


# ======================================================================
# CLASSE ENFEITE (pecinha do cenario: poeira, nuvem, brasa, chuva, estrela...)
# ======================================================================
class Enfeite:
    """Uma pecinha de fundo que se mexe sozinha. O tipo diz como ela se comporta."""

    def __init__(self, tipo):
        self.tipo = tipo
        self.x = random.randint(0, LARGURA)
        self.y = random.randint(0, CHAO)
        if EFEITOS[tipo]["forma"] == "nuvem":
            self.y = random.randint(30, 260)  # nuvens ficam no alto
        self.fator = random.randint(1, 3)  # quanto maior, mais "perto" e mais rapido
        self.tamanho = random.randint(1, 3)
        self.fase = random.randint(0, 60)  # para nem todas piscarem juntas

    def atualiza(self):
        dados = EFEITOS[self.tipo]
        self.x += dados["vx"] * self.fator
        self.y += dados["vy"] * self.fator
        # quando sai de um lado da tela, volta pelo outro
        if self.x < -130:
            self.x = LARGURA + 20
        if self.y < 0:
            self.y = CHAO
        if self.y > CHAO:
            self.y = 0

    def desenha(self, tela, tempo):
        dados = EFEITOS[self.tipo]
        cor = dados["cor"]
        forma = dados["forma"]
        x = int(self.x)
        y = int(self.y)
        if forma == "risco":  # poeira levada pelo vento
            pygame.draw.line(tela, cor, (x, y), (x + 8 + self.tamanho * 6, y), self.tamanho // 2 + 1)
        elif forma == "risco_diag":  # gota de chuva
            pygame.draw.line(tela, cor, (x, y), (x + 2, y - 10 - self.fator * 3), 1)
        elif forma == "ponto":  # brasa subindo
            pygame.draw.circle(tela, cor, (x, y), self.tamanho)
        elif forma == "pisca":  # estrela ou vagalume piscando
            if ((tempo + self.fase) // 20) % 3 != 0:
                pygame.draw.circle(tela, cor, (x, y), self.tamanho)
        else:  # nuvem
            largura = 40 + self.tamanho * 25
            pygame.draw.ellipse(tela, cor, (x, y, largura, 18 + self.tamanho * 4))
            pygame.draw.ellipse(tela, cor, (x + largura // 4, y - 8, largura // 2, 22))


def cria_enfeites(tipo):
    """Cria a lista de enfeites de um tipo de efeito."""
    enfeites = []
    for i in range(EFEITOS[tipo]["quantidade"]):
        enfeites.append(Enfeite(tipo))
    return enfeites
